# -*- coding: utf-8 -*-
"""
Remote Switch V2 Plugin
Copyright (C) 2017 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

remote_switch_v2.py: Remote Switch V2 Plugin Implementation

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

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QTextCursor

from brickv.plugin_system.comcu_plugin_base import COMCUPluginBase
from brickv.plugin_system.plugins.remote_switch_v2.ui_remote_switch_v2 import Ui_RemoteSwitchV2
from brickv.bindings.bricklet_remote_switch_v2 import BrickletRemoteSwitchV2

REMOTE_TYPE_A = 1
REMOTE_TYPE_B = 2
REMOTE_TYPE_C = 3

class RemoteSwitchV2(COMCUPluginBase, Ui_RemoteSwitchV2):
    qtcb_switching_done = pyqtSignal()
    qtcb_update_remote_input = pyqtSignal(str)

    def __init__(self, *args):
        COMCUPluginBase.__init__(self, BrickletRemoteSwitchV2, *args)

        self.setupUi(self)

        self.rs2 = self.device

        self.qtcb_switching_done.connect(self.cb_switching_done)
        self.rs2.register_callback(self.rs2.CALLBACK_SWITCHING_DONE,
                                   self.qtcb_switching_done.emit)

        self.qtcb_update_remote_input.connect(self.cb_update_remote_input)

        self.h_check = (self.h_check_a,
                        self.h_check_b,
                        self.h_check_c,
                        self.h_check_d,
                        self.h_check_e)

        self.r_check = (self.r_check_a,
                        self.r_check_b,
                        self.r_check_c,
                        self.r_check_d,
                        self.r_check_e)

        for h in self.h_check:
            h.stateChanged.connect(self.h_check_state_changed)

        for r in self.r_check:
            r.stateChanged.connect(self.r_check_state_changed)

        self.checkbox_switchall.stateChanged.connect(self.switchall_state_changed)
        self.spinbox_house.valueChanged.connect(self.house_value_changed)
        self.spinbox_receiver.valueChanged.connect(self.receiver_value_changed)
        self.combo_type.currentIndexChanged.connect(self.type_index_changed)

        self.spinbox_dim_value.valueChanged.connect(self.spinbox_dim_value_changed)
        self.slider_dim_value.valueChanged.connect(self.slider_dim_value_changed)

        self.button_switch_on.clicked.connect(lambda: self.button_clicked(1))
        self.button_switch_off.clicked.connect(lambda: self.button_clicked(0))
        self.button_dim.clicked.connect(self.dim_clicked)

        self.combo_remote_type.currentIndexChanged.connect(self.remote_type_changed)
        self.spinbox_remote_minimum_repeats.valueChanged.connect(lambda value: self.remote_type_changed(self.combo_remote_type.currentIndex()))
        self.button_remote_input_clear.clicked.connect(self.plaintextedit_remote_input.clear)

        self.type_a_widgets = [self.label_house_code,
                               self.h_check_a,
                               self.h_check_b,
                               self.h_check_c,
                               self.h_check_d,
                               self.h_check_e,
                               self.spinbox_house,
                               self.label_receiver_code,
                               self.r_check_a,
                               self.r_check_b,
                               self.r_check_c,
                               self.r_check_d,
                               self.r_check_e,
                               self.spinbox_receiver,
                               self.button_switch_on,
                               self.button_switch_off]

        self.type_b_widgets = [self.label_address,
                               self.spinbox_address,
                               self.label_unit,
                               self.spinbox_unit,
                               self.checkbox_switchall,
                               self.button_switch_on,
                               self.button_switch_off]

        self.type_b_dim_widgets = [self.label_address,
                                   self.spinbox_address,
                                   self.label_unit,
                                   self.spinbox_unit,
                                   self.checkbox_switchall,
                                   self.label_dim,
                                   self.spinbox_dim_value,
                                   self.slider_dim_value,
                                   self.button_dim]

        self.type_c_widgets = [self.label_system_code,
                               self.combo_system_code,
                               self.label_device_code,
                               self.spinbox_device_code,
                               self.button_switch_on,
                               self.button_switch_off]

        self.type_widgets = (self.type_a_widgets,
                             self.type_b_widgets,
                             self.type_b_dim_widgets,
                             self.type_c_widgets)

        self.type_index_changed(0)
        self.remote_type_changed(0)

    def spinbox_dim_value_changed(self, value):
        self.slider_dim_value.setValue(value)

    def slider_dim_value_changed(self, value):
        self.spinbox_dim_value.setValue(value)

    def type_index_changed(self, index):
        for i in range(len(self.type_widgets)):
            if i != index:
                for w in self.type_widgets[i]:
                    w.setVisible(False)

        for w in self.type_widgets[index]:
            w.setVisible(True)

    def house_value_changed(self, state):
        for i in range(5):
            if state & (1 << i):
                self.h_check[i].setChecked(True)
            else:
                self.h_check[i].setChecked(False)

    def receiver_value_changed(self, state):
        for i in range(5):
            if state & (1 << i):
                self.r_check[i].setChecked(True)
            else:
                self.r_check[i].setChecked(False)

    def switchall_state_changed(self, state):
        if self.checkbox_switchall.isChecked():
            self.spinbox_address.setEnabled(False)
            self.spinbox_unit.setEnabled(False)
        else:
            self.spinbox_address.setEnabled(True)
            self.spinbox_unit.setEnabled(True)

    def h_check_state_changed(self, state):
        house_code = 0
        for i in range(5):
            if self.h_check[i].isChecked():
                house_code |= (1 << i)

        self.spinbox_house.setValue(house_code)

    def r_check_state_changed(self, state):
        receiver_code = 0
        for i in range(5):
            if self.r_check[i].isChecked():
                receiver_code |= (1 << i)

        self.spinbox_receiver.setValue(receiver_code)

    def start(self):
        pass

    def stop(self):
        pass

    def destroy(self):
        pass

    def dim_clicked(self):
        self.button_dim.setEnabled(False)
        self.button_dim.setText("Dimming...")

        repeats = self.spinbox_repeats.value()
        self.rs2.set_repeats(repeats)

        if self.combo_type.currentIndex() == 2:
            address = self.spinbox_address.value()
            unit = self.spinbox_unit.value()
            if self.checkbox_switchall.isChecked():
                address = 0
                unit = 255

            dim_value = self.spinbox_dim_value.value()

            self.rs2.dim_socket_b(address, unit, dim_value)

    def cb_remote_status_a(self, house_code, receiver_code, switch_to, repeats):
        remote_input = "[Remote Type - A]\n" + \
                       "House Code = " + \
                       str(house_code) + \
                       ", Receiver Code = " + \
                       str(receiver_code) + \
                       ", Switch To = " + \
                       str(switch_to) + \
                       ", Repeats = " + \
                       str(repeats) + \
                       "\n"

        self.qtcb_update_remote_input.emit(remote_input)

    def cb_remote_status_b(self, address, unit, switch_to, dim_value, repeats):
        remote_input = "[Remote Type - B]\n" + \
                       "Address = " + \
                       str(address) + \
                       ", Unit = " + \
                       str(unit) + \
                       ", Switch To = " + \
                       str(switch_to) + \
                       ", Dim Value = " + \
                       str(dim_value) + \
                       ", Repeats = " + \
                       str(repeats) + \
                       "\n"

        self.qtcb_update_remote_input.emit(remote_input)

    def cb_remote_status_c(self, system_code, device_code, switch_to, repeats):
        remote_input = "[Remote Type - C]\n" + \
                       "System Code = " + \
                       str(system_code) + \
                       ", Device Code = " + \
                       str(device_code) + \
                       ", Switch To = " + \
                       str(switch_to) + \
                       ", Repeats = " + \
                       str(repeats) + \
                       "\n"

        self.qtcb_update_remote_input.emit(remote_input)

    def remote_type_changed(self, index):
        if index + 1 == REMOTE_TYPE_A:
            self.rs2.set_remote_configuration(self.rs2.REMOTE_TYPE_A,
                                              self.spinbox_remote_minimum_repeats.value(),
                                              True)

            self.rs2.register_callback(self.rs2.CALLBACK_REMOTE_STATUS_A,
                                       self.cb_remote_status_a)

        elif index + 1 == REMOTE_TYPE_B:
            self.rs2.set_remote_configuration(self.rs2.REMOTE_TYPE_B,
                                              self.spinbox_remote_minimum_repeats.value(),
                                              True)

            self.rs2.register_callback(self.rs2.CALLBACK_REMOTE_STATUS_B,
                                       self.cb_remote_status_b)

        elif index + 1 == REMOTE_TYPE_C:
            self.rs2.set_remote_configuration(self.rs2.REMOTE_TYPE_C,
                                              self.spinbox_remote_minimum_repeats.value(),
                                              True)

            self.rs2.register_callback(self.rs2.CALLBACK_REMOTE_STATUS_C,
                                       self.cb_remote_status_c)

    def button_clicked(self, switch_to):
        self.button_switch_on.setEnabled(False)
        self.button_switch_on.setText("Switching...")
        self.button_switch_off.setEnabled(False)
        self.button_switch_off.setText("Switching...")

        repeats = self.spinbox_repeats.value()
        self.rs2.set_repeats(repeats)

        if self.combo_type.currentText() == 'A Switch':
            house_code = self.spinbox_house.value()
            receiver_code = self.spinbox_receiver.value()
            self.rs2.switch_socket_a(house_code, receiver_code, switch_to)
        elif self.combo_type.currentText() == 'B Switch':
            address = self.spinbox_address.value()
            unit = self.spinbox_unit.value()

            if self.checkbox_switchall.isChecked():
                address = 0
                unit = 255

            self.rs2.switch_socket_b(address, unit, switch_to)
        elif self.combo_type.currentText() == 'C Switch':
            system_code = self.combo_system_code.currentText()[0]
            device_code = self.spinbox_device_code.value()
            self.rs2.switch_socket_c(system_code, device_code, switch_to)

    def cb_switching_done(self):
        self.button_switch_on.setEnabled(True)
        self.button_switch_on.setText("Switch On")
        self.button_switch_off.setEnabled(True)
        self.button_switch_off.setText("Switch Off")
        self.button_dim.setEnabled(True)
        self.button_dim.setText("Dim")

    def cb_update_remote_input(self, remote_input):
        self.plaintextedit_remote_input.appendPlainText(remote_input)
        self.plaintextedit_remote_input.moveCursor(QTextCursor.End)

    def get_url_part(self):
        return 'remote_switch_v2'

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletRemoteSwitchV2.DEVICE_IDENTIFIER
