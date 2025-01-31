# -*- coding: utf-8 -*-
"""
Barometer Plugin
Copyright (C) 2011-2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2012, 2014-2016 Matthias Bolte <matthias@tinkerforge.com>

barometer.py: Barometer Plugin Implementation

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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
                        QSpinBox, QFrame, QDoubleSpinBox

from brickv.plugin_system.plugin_base import PluginBase
from brickv.bindings.bricklet_barometer import BrickletBarometer
from brickv.plot_widget import PlotWidget, CurveValueWrapper
from brickv.async_call import async_call
from brickv.callback_emulator import CallbackEmulator

class ChipTemperatureLabel(QLabel):
    def setText(self, text):
        text = "Chip Temperature: " + text + " %cC" % 0xB0
        super().setText(text)

METER_TO_FEET_DIVISOR = 0.3048

class Barometer(PluginBase):
    def __init__(self, *args):
        super().__init__(BrickletBarometer, *args)

        self.barometer = self.device

        # the firmware version of a EEPROM Bricklet can (under common circumstances)
        # not change during the lifetime of an EEPROM Bricklet plugin. therefore,
        # it's okay to make final decisions based on it here
        self.has_averaging = self.firmware_version >= (2, 0, 2)

        self.moving_average_pressure = 25
        self.average_pressure = 10
        self.average_temperature = 10

        self.cbe_air_pressure = CallbackEmulator(self,
                                                 self.barometer.get_air_pressure,
                                                 None,
                                                 self.cb_air_pressure,
                                                 self.increase_error_count)
        self.cbe_altitude = CallbackEmulator(self,
                                             self.barometer.get_altitude,
                                             None,
                                             self.cb_altitude,
                                             self.increase_error_count)
        self.cbe_chip_temperature = CallbackEmulator(self,
                                                     self.barometer.get_chip_temperature,
                                                     None,
                                                     self.cb_chip_temperature,
                                                     self.increase_error_count)

        self.chip_temperature_label = ChipTemperatureLabel()

        self.current_air_pressure = CurveValueWrapper() # float, hPa
        self.current_altitude = CurveValueWrapper() # float, m

        self.clear_graphs_button = QPushButton('Clear Graphs')

        plots = [('Air Pressure', Qt.red, self.current_air_pressure, '{:.3f} hPa (QFE)'.format)]
        self.air_pressure_plot_widget = PlotWidget('Air Pressure [hPa]', plots, self.clear_graphs_button, y_resolution=0.001)

        plots = [('Altitude', Qt.darkGreen, self.current_altitude, lambda value: '{:.2f} m ({:.2f} ft)'.format(value, value / METER_TO_FEET_DIVISOR))]
        self.altitude_plot_widget = PlotWidget('Altitude [m]', plots, self.clear_graphs_button, y_resolution=0.01)

        self.reference_label = QLabel('Reference Air Pressure [hPa]:')

        self.reference_box = QDoubleSpinBox()
        self.reference_box.setMinimum(10)
        self.reference_box.setMaximum(1200)
        self.reference_box.setDecimals(3)
        self.reference_box.setValue(1013.25)
        self.reference_box.editingFinished.connect(self.reference_box_finished)

        self.use_current_button = QPushButton('Use Current')
        self.use_current_button.clicked.connect(self.use_current_clicked)

        if self.has_averaging:
            self.avg_pressure_box = QSpinBox()
            self.avg_pressure_box.setMinimum(0)
            self.avg_pressure_box.setMaximum(10)
            self.avg_pressure_box.setSingleStep(1)
            self.avg_pressure_box.setValue(10)
            self.avg_pressure_box.editingFinished.connect(self.avg_pressure_box_finished)

            self.avg_temperature_box = QSpinBox()
            self.avg_temperature_box.setMinimum(0)
            self.avg_temperature_box.setMaximum(255)
            self.avg_temperature_box.setSingleStep(1)
            self.avg_temperature_box.setValue(10)
            self.avg_temperature_box.editingFinished.connect(self.avg_temperature_box_finished)

            self.avg_moving_pressure_box = QSpinBox()
            self.avg_moving_pressure_box.setMinimum(0)
            self.avg_moving_pressure_box.setMaximum(25)
            self.avg_moving_pressure_box.setSingleStep(1)
            self.avg_moving_pressure_box.setValue(25)
            self.avg_moving_pressure_box.editingFinished.connect(self.avg_moving_pressure_box_finished)

        layout_h1 = QHBoxLayout()
        layout_h1.addWidget(self.air_pressure_plot_widget)
        layout_h1.addWidget(self.altitude_plot_widget)

        layout = QVBoxLayout(self)
        layout.addLayout(layout_h1)

        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        layout.addWidget(line)

        layout_h2 = QHBoxLayout()
        layout_h2.addWidget(self.reference_label)
        layout_h2.addWidget(self.reference_box)
        layout_h2.addWidget(self.use_current_button)
        layout_h2.addStretch()
        layout_h2.addWidget(self.chip_temperature_label)
        layout_h2.addStretch()
        layout_h2.addWidget(self.clear_graphs_button)

        layout.addLayout(layout_h2)

        if self.has_averaging:
            layout_h3 = QHBoxLayout()
            layout_h3.addWidget(QLabel('Air Pressure Moving Average Length:'))
            layout_h3.addWidget(self.avg_moving_pressure_box)
            layout_h3.addStretch()
            layout_h3.addWidget(QLabel('Air Pressure Average Length:'))
            layout_h3.addWidget(self.avg_pressure_box)
            layout_h3.addStretch()
            layout_h3.addWidget(QLabel('Temperate Average Length:'))
            layout_h3.addWidget(self.avg_temperature_box)

            layout.addLayout(layout_h3)

    def start(self):
        if self.has_averaging:
            async_call(self.barometer.get_averaging, None, self.get_averaging_async, self.increase_error_count)

        async_call(self.barometer.get_reference_air_pressure, None, self.get_reference_air_pressure_async, self.increase_error_count)

        self.cbe_air_pressure.set_period(100)
        self.cbe_altitude.set_period(100)
        self.cbe_chip_temperature.set_period(100)

        self.air_pressure_plot_widget.stop = False
        self.altitude_plot_widget.stop = False

    def stop(self):
        self.cbe_air_pressure.set_period(0)
        self.cbe_altitude.set_period(0)
        self.cbe_chip_temperature.set_period(0)

        self.air_pressure_plot_widget.stop = True
        self.altitude_plot_widget.stop = True

    def destroy(self):
        pass

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletBarometer.DEVICE_IDENTIFIER

    def get_averaging_async(self, avg):
        moving_average_pressure, average_pressure, average_temperature = avg
        self.moving_average_pressure = moving_average_pressure
        self.average_pressure = average_pressure
        self.average_temperature = average_temperature

        self.avg_moving_pressure_box.setValue(moving_average_pressure)
        self.avg_pressure_box.setValue(average_pressure)
        self.avg_temperature_box.setValue(average_temperature)

    def avg_pressure_box_finished(self):
        self.average_pressure = self.avg_pressure_box.value()
        self.save_new_averaging()

    def avg_temperature_box_finished(self):
        self.average_temperature = self.avg_temperature_box.value()
        self.save_new_averaging()

    def avg_moving_pressure_box_finished(self):
        self.moving_average_pressure = self.avg_moving_pressure_box.value()
        self.save_new_averaging()

    def save_new_averaging(self):
        self.barometer.set_averaging(self.moving_average_pressure, self.average_pressure, self.average_temperature)

    def get_reference_air_pressure_async(self, reference):
        self.reference_box.setValue(reference / 1000.0)

    def use_current_clicked(self):
        self.barometer.set_reference_air_pressure(0)
        async_call(self.barometer.get_reference_air_pressure, None, self.get_reference_air_pressure_async, self.increase_error_count)

    def reference_box_finished(self):
        self.barometer.set_reference_air_pressure(self.reference_box.value() * 1000.0)

    def cb_air_pressure(self, air_pressure):
        self.current_air_pressure.value = air_pressure / 1000.0

    def cb_altitude(self, altitude):
        self.current_altitude.value = altitude / 100.0

    def cb_chip_temperature(self, temperature):
        self.chip_temperature_label.setText('{:.2f}'.format(temperature / 100.0))
