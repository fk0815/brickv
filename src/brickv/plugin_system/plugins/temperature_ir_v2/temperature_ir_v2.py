# -*- coding: utf-8 -*-
"""
Temperature IR V2 Plugin
Copyright (C) 2017 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

temperature_ir_v2.py: Temperature-IR V2 Plugin Implementation

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
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QFrame

from brickv.plugin_system.comcu_plugin_base import COMCUPluginBase
from brickv.bindings.bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
from brickv.plot_widget import PlotWidget, CurveValueWrapper
from brickv.async_call import async_call
from brickv.callback_emulator import CallbackEmulator

class TemperatureIRV2(COMCUPluginBase):
    def __init__(self, *args):
        super().__init__(BrickletTemperatureIRV2, *args)

        self.tir = self.device

        self.cbe_ambient_temperature = CallbackEmulator(self,
                                                        self.tir.get_ambient_temperature,
                                                        None,
                                                        self.cb_ambient_temperature,
                                                        self.increase_error_count)
        self.cbe_object_temperature = CallbackEmulator(self,
                                                       self.tir.get_object_temperature,
                                                       None,
                                                       self.cb_object_temperature,
                                                       self.increase_error_count)

        self.current_ambient = CurveValueWrapper() # float, °C
        self.current_object = CurveValueWrapper() # float, °C

        plots = [('Ambient', Qt.blue, self.current_ambient, '{} °C'.format),
                 ('Object', Qt.red, self.current_object, '{} °C'.format)]
        self.plot_widget = PlotWidget('Temperature [°C]', plots, y_resolution=0.1)

        self.spin_emissivity = QSpinBox()
        self.spin_emissivity.setMinimum(6553)
        self.spin_emissivity.setMaximum(65535)
        self.spin_emissivity.setValue(65535)
        self.spin_emissivity.editingFinished.connect(self.spin_emissivity_finished)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel('Emissivity:'))
        hlayout.addWidget(self.spin_emissivity)
        hlayout.addStretch()

        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)
        layout.addWidget(line)
        layout.addLayout(hlayout)

    def start(self):
        async_call(self.tir.get_emissivity, None, self.get_emissivity_async, self.increase_error_count)

        self.cbe_ambient_temperature.set_period(250)
        self.cbe_object_temperature.set_period(250)

        self.plot_widget.stop = False

    def stop(self):
        self.cbe_ambient_temperature.set_period(0)
        self.cbe_object_temperature.set_period(0)

        self.plot_widget.stop = True

    def destroy(self):
        pass

    @staticmethod
    def has_device_identifier(device_identifier):
        return device_identifier == BrickletTemperatureIRV2.DEVICE_IDENTIFIER

    def cb_object_temperature(self, temperature):
        self.current_object.value = temperature / 10.0

    def cb_ambient_temperature(self, temperature):
        self.current_ambient.value = temperature / 10.0

    def get_emissivity_async(self, emissivity):
        self.spin_emissivity.setValue(emissivity)

    def spin_emissivity_finished(self):
        self.tir.set_emissivity(self.spin_emissivity.value())
