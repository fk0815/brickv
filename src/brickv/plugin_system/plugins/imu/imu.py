# -*- coding: utf-8 -*-
"""
IMU Plugin
Copyright (C) 2010-2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2016 Matthias Bolte <matthias@tinkerforge.com>

imu.py: IMU Plugin implementation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QSizePolicy, QAction

from brickv.plugin_system.plugin_base import PluginBase
from brickv.plugin_system.plugins.imu.imu_3d_widget import IMU3DWidget
from brickv.plugin_system.plugins.imu.ui_imu import Ui_IMU
from brickv.plugin_system.plugins.imu.calibrate_window import CalibrateWindow
from brickv.bindings.brick_imu import BrickIMU
from brickv.async_call import async_call
from brickv.plot_widget import PlotWidget, CurveValueWrapper
from brickv.callback_emulator import CallbackEmulator

class IMU(PluginBase, Ui_IMU):
    def __init__(self, *args):
        PluginBase.__init__(self, BrickIMU, *args)

        self.setupUi(self)

        self.imu = self.device

        # the firmware version of a Brick can (under common circumstances) not
        # change during the lifetime of a Brick plugin. therefore, it's okay to
        # make final decisions based on it here
        self.has_status_led = self.firmware_version >= (2, 3, 1)

        self.acc_x = CurveValueWrapper()
        self.acc_y = CurveValueWrapper()
        self.acc_z = CurveValueWrapper()
        self.mag_x = CurveValueWrapper()
        self.mag_y = CurveValueWrapper()
        self.mag_z = CurveValueWrapper()
        self.gyr_x = CurveValueWrapper()
        self.gyr_y = CurveValueWrapper()
        self.gyr_z = CurveValueWrapper()
        self.temp  = CurveValueWrapper()
        self.roll  = None
        self.pitch = None
        self.yaw   = None
        self.qua_x = None
        self.qua_y = None
        self.qua_z = None
        self.qua_w = None

        self.all_data_valid = False
        self.quaternion_valid = False
        self.orientation_valid = False

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_data)

        self.cbe_all_data = CallbackEmulator(self,
                                             self.imu.get_all_data,
                                             None,
                                             self.cb_all_data,
                                             self.increase_error_count,
                                             expand_result_tuple_for_callback=True,
                                             use_result_signal=False)
        self.cbe_orientation = CallbackEmulator(self,
                                                self.imu.get_orientation,
                                                None,
                                                self.cb_orientation,
                                                self.increase_error_count,
                                                expand_result_tuple_for_callback=True,
                                                use_result_signal=False)
        self.cbe_quaternion = CallbackEmulator(self,
                                               self.imu.get_quaternion,
                                               None,
                                               self.cb_quaternion,
                                               self.increase_error_count,
                                               expand_result_tuple_for_callback=True,
                                               use_result_signal=False)

        self.imu_gl = IMU3DWidget(self)
        self.imu_gl.setMinimumSize(150, 150)
        self.imu_gl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update_counter = 0

        self.mag_plot_widget = PlotWidget("Magnetic Field [µT]",
                                          [("X", Qt.red, self.mag_x, str),
                                           ("Y", Qt.darkGreen, self.mag_y, str),
                                           ("Z", Qt.blue, self.mag_z, str)],
                                          clear_button=self.clear_graphs,
                                          key='right-no-icon', y_resolution=5)
        self.acc_plot_widget = PlotWidget("Acceleration [mg]",
                                          [("X", Qt.red, self.acc_x, str),
                                           ("Y", Qt.darkGreen, self.acc_y, str),
                                           ("Z", Qt.blue, self.acc_z, str)],
                                          clear_button=self.clear_graphs,
                                          key='right-no-icon', y_resolution=5)
        self.gyr_plot_widget = PlotWidget("Angular Velocity [°/s]",
                                          [("X", Qt.red, self.gyr_x, str),
                                           ("Y", Qt.darkGreen, self.gyr_y, str),
                                           ("Z", Qt.blue, self.gyr_z, str)],
                                          clear_button=self.clear_graphs,
                                          key='right-no-icon', y_resolution=0.05)
        self.temp_plot_widget = PlotWidget("Temperature [°C]",
                                           [("t", Qt.red, self.temp, str)],
                                           clear_button=self.clear_graphs,
                                           key=None, y_resolution=0.01)

        self.mag_plot_widget.setMinimumSize(250, 250)
        self.acc_plot_widget.setMinimumSize(250, 250)
        self.gyr_plot_widget.setMinimumSize(250, 250)
        self.temp_plot_widget.setMinimumSize(250, 250)

        self.orientation_label = QLabel('Position your IMU Brick as shown in the image above, then press "Save Orientation".')
        self.orientation_label.setWordWrap(True)
        self.orientation_label.setAlignment(Qt.AlignHCenter)
        self.gl_layout = QVBoxLayout()
        self.gl_layout.addWidget(self.imu_gl)
        self.gl_layout.addWidget(self.orientation_label)

        self.layout_top.addWidget(self.gyr_plot_widget)
        self.layout_top.addWidget(self.acc_plot_widget)
        self.layout_top.addWidget(self.mag_plot_widget)
        self.layout_bottom.addLayout(self.gl_layout)
        self.layout_bottom.addWidget(self.temp_plot_widget)

        self.save_orientation.clicked.connect(self.save_orientation_clicked)
        self.calibrate.clicked.connect(self.calibrate_clicked)
        self.led_button.clicked.connect(self.led_clicked)
        self.speed_spinbox.editingFinished.connect(self.speed_finished)

        width = QFontMetrics(self.gyr_x_label.font()).boundingRect('-XXXX.X').width()

        self.gyr_x_label.setMinimumWidth(width)
        self.gyr_y_label.setMinimumWidth(width)
        self.gyr_z_label.setMinimumWidth(width)

        self.calibrate = None
        self.alive = True

        if self.has_status_led:
            self.status_led_action = QAction('Status LED', self)
            self.status_led_action.setCheckable(True)
            self.status_led_action.toggled.connect(lambda checked: self.imu.enable_status_led() if checked else self.imu.disable_status_led())
            self.set_configs([(0, None, [self.status_led_action])])
        else:
            self.status_led_action = None

        reset = QAction('Reset', self)
        reset.triggered.connect(self.imu.reset)
        self.set_actions([(0, None, [reset])])

    def save_orientation_clicked(self):
        self.imu_gl.save_orientation()
        self.orientation_label.hide()

    def cleanup_gl(self):
        self.state = self.imu_gl.get_state()
        self.imu_gl.hide()
        self.imu_gl.cleanup()

    def restart_gl(self):
        self.imu_gl = IMU3DWidget()

        self.imu_gl.setMinimumSize(150, 150)
        self.imu_gl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gl_layout.addWidget(self.imu_gl)
        self.imu_gl.show()

        self.save_orientation.clicked.connect(self.save_orientation_clicked)
        self.imu_gl.set_state(self.state)

    def start(self):
        if not self.alive:
            return

        if self.has_status_led:
            async_call(self.imu.is_status_led_enabled, None, self.status_led_action.setChecked, self.increase_error_count)

        self.parent().add_callback_pre_tab(lambda tab_window: self.cleanup_gl(), 'imu_cleanup_pre_tab')
        self.parent().add_callback_post_tab(lambda tab_window, tab_index: self.restart_gl(), 'imu_restart_post_tab')
        self.parent().add_callback_pre_untab(lambda tab_window, tab_index: self.cleanup_gl(), 'imu_cleanup_pre_untab')
        self.parent().add_callback_post_untab(lambda tab_window: self.restart_gl(), 'imu_restart_post_untab')

        self.gl_layout.activate()
        self.cbe_all_data.set_period(100)
        self.cbe_orientation.set_period(100)
        self.cbe_quaternion.set_period(50)
        self.update_timer.start(50)

        async_call(self.imu.get_convergence_speed, None, self.speed_spinbox.setValue, self.increase_error_count)

        self.mag_plot_widget.stop = False
        self.acc_plot_widget.stop = False
        self.gyr_plot_widget.stop = False
        self.temp_plot_widget.stop = False

    def stop(self):
        self.mag_plot_widget.stop = True
        self.acc_plot_widget.stop = True
        self.gyr_plot_widget.stop = True
        self.temp_plot_widget.stop = True

        self.update_timer.stop()
        self.cbe_all_data.set_period(0)
        self.cbe_orientation.set_period(0)
        self.cbe_quaternion.set_period(0)

    def destroy(self):
        self.alive = False
        self.cleanup_gl()
        if self.calibrate:
            self.calibrate.close()

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickIMU.DEVICE_IDENTIFIER

    def cb_all_data(self, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, gyr_x, gyr_y, gyr_z, temp):
        self.acc_x.value = acc_x
        self.acc_y.value = acc_y
        self.acc_z.value = acc_z
        self.mag_x.value = mag_x / 10
        self.mag_y.value = mag_y / 10
        self.mag_z.value = mag_z / 10
        self.gyr_x.value = gyr_x / 14.375
        self.gyr_y.value = gyr_y / 14.375
        self.gyr_z.value = gyr_z / 14.375
        self.temp.value  = temp / 100.0

        self.all_data_valid = True

    def cb_quaternion(self, x, y, z, w):
        self.qua_x = x
        self.qua_y = y
        self.qua_z = z
        self.qua_w = w

        self.quaternion_valid = True

    def cb_orientation(self, roll, pitch, yaw):
        self.roll = roll / 100.0
        self.pitch = pitch / 100.0
        self.yaw = yaw / 100.0

        self.orientation_valid = True

    def led_clicked(self):
        if 'On' in self.led_button.text().replace('&', ''):
            self.led_button.setText('Turn LEDs Off')
            self.imu.leds_on()
        elif 'Off' in self.led_button.text().replace('&', ''):
            self.led_button.setText('Turn LEDs On')
            self.imu.leds_off()

    def update_data(self):
        self.update_counter += 1

        if self.quaternion_valid:
            self.imu_gl.update_orientation(self.qua_w, self.qua_x, self.qua_y, self.qua_z)

        if self.update_counter == 2:
            self.update_counter = 0

            if self.all_data_valid and self.orientation_valid:
                self.acceleration_update(self.acc_x.value, self.acc_y.value, self.acc_z.value)
                self.magnetometer_update(self.mag_x.value, self.mag_y.value, self.mag_z.value)
                self.gyroscope_update(self.gyr_x.value, self.gyr_y.value, self.gyr_z.value)
                self.orientation_update(self.roll, self.pitch, self.yaw)
                self.temperature_update(self.temp.value)

    def acceleration_update(self, x, y, z):
        self.acc_y_label.setText(format(x, '.1f'))
        self.acc_x_label.setText(format(y, '.1f'))
        self.acc_z_label.setText(format(z, '.1f'))

    def magnetometer_update(self, x, y, z):
        # Earth magnetic field: 0.5 Gauss
        self.mag_x_label.setText(format(x, '.1f'))
        self.mag_y_label.setText(format(y, '.1f'))
        self.mag_z_label.setText(format(z, '.1f'))

    def gyroscope_update(self, x, y, z):
        self.gyr_x_label.setText(format(x, '.1f'))
        self.gyr_y_label.setText(format(y, '.1f'))
        self.gyr_z_label.setText(format(z, '.1f'))

    def orientation_update(self, r, p, y):
        self.roll_label.setText(format(r, '.1f'))
        self.pitch_label.setText(format(p, '.1f'))
        self.yaw_label.setText(format(y, '.1f'))

    def temperature_update(self, t):
        self.tem_label.setText(format(t, '.1f'))

    def calibrate_clicked(self):
        self.stop()

        if self.calibrate is None:
            self.calibrate = CalibrateWindow(self)

        self.calibrate.refresh_values()
        self.calibrate.show()

    def speed_finished(self):
        speed = self.speed_spinbox.value()
        self.imu.set_convergence_speed(speed)
