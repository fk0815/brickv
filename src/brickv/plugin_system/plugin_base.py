# -*- coding: utf-8 -*-
"""
brickv (Brick Viewer)
Copyright (C) 2009-2012 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014-2015 Matthias Bolte <matthias@tinkerforge.com>

plugin_base.py: Base class for all Brick Viewer Plugins

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

import sys

from PyQt5.QtWidgets import QWidget, QTabBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtBoundSignal

from brickv.bindings.ip_connection import IPConnection
from brickv.bindings.bricklet_unknown import BrickletUnknown
from brickv.bindings.tng_unknown import TNGUnknown
from brickv.utils import get_main_window
from brickv.tab_window import IconButton
from brickv.load_pixmap import load_pixmap
from brickv.infos import get_version_string, inventory

class PluginBase(QWidget):
    PLUGIN_STATE_STOPPED = 0
    PLUGIN_STATE_RUNNING = 1
    PLUGIN_STATE_PAUSED = 2

    def __init__(self, device_class, ipcon, device_info, override_base_name=None):
        super().__init__()

        self.has_comcu = False # Will be overwritten if plugin has comcu
        self.is_tng = False # Will be overwritten if plugin is tng
        self.plugin_state = PluginBase.PLUGIN_STATE_STOPPED
        self.label_timeouts_title = None
        self.label_timeouts = None
        self.label_version = None
        self.button_parent = None
        self.label_position = None
        self.device_class = device_class
        self.ipcon = ipcon
        self.device_info = device_info
        self.uid = device_info.uid
        self.hardware_version = device_info.hardware_version
        self.firmware_version = device_info.firmware_version_installed
        self.error_count = 0
        self.configs = []
        self.actions = []

        if device_class is not None:
            self.base_name = self.device_class.DEVICE_DISPLAY_NAME
            self.device = self.device_class(self.uid, self.ipcon)
        else:
            self.base_name = 'Unnamed'
            self.device = None

        if override_base_name != None:
            self.base_name = override_base_name

            if override_base_name == 'Unknown':
                if str(self.device_info.device_identifier).startswith('20'):
                    self.device = TNGUnknown(self.uid, self.ipcon)
                else:
                    self.device = BrickletUnknown(self.uid, self.ipcon)

        if self.is_hardware_version_relevant():
            self.name = '{0} {1}.{2}'.format(self.base_name,
                                             self.hardware_version[0],
                                             self.hardware_version[1])
        else:
            self.name = self.base_name

        self.device_info.plugin = self
        self.device_info.name = self.name
        self.device_info.url_part = self.get_url_part()

        inventory.info_changed.connect(self.device_info_changed)

    def device_info_changed(self, uid):
        if uid != self.device_info.uid:
            return

        if self.device_info.tab_window is None:
            return

        if self.device_info.firmware_version_installed < self.device_info.firmware_version_latest:
            self.show_update()
        else:
            self.hide_update()

        self.hardware_version = self.device_info.hardware_version
        self.firmware_version = self.device_info.firmware_version_installed
        self.label_version.setText(get_version_string(self.firmware_version))

        if self.button_parent is not None:
            self.button_parent.setText(self.device_info.connected_uid)
            self.button_parent.clicked.connect(lambda: get_main_window().show_plugin(self.device_info.connected_uid))

        if self.label_position is not None:
            self.label_position.setText(self.device_info.position.title())

    def show_update(self):
        self.device_info.tab_window.button_update.show()

        if self.device_info.flashable_like_bricklet:
            clicked = lambda: get_main_window().show_bricklet_update(self.device_info.connected_uid, self.device_info.position)
        elif self.device_info.kind == 'brick':
            clicked = lambda: get_main_window().show_brick_update(self.device_info.url_part)

        self.device_info.tab_window.show_update_tab_button('Update available', clicked)

    def hide_update(self):
        self.device_info.tab_window.button_update.hide()
        self.device_info.tab_window.hide_update_tab_button()

    def start_plugin(self):
        # only consider starting the plugin, if it's stopped
        if self.plugin_state == PluginBase.PLUGIN_STATE_STOPPED:
            if self.ipcon.get_connection_state() == IPConnection.CONNECTION_STATE_PENDING:
                # if connection is pending, the just mark it as paused. it'll
                # started later then
                self.plugin_state = PluginBase.PLUGIN_STATE_PAUSED
            else:
                # otherwise start now
                try:
                    if hasattr(self, 'start_comcu'):
                        self.start_comcu()
                    else:
                        self.start()
                except:
                    # Report the exception without unwinding the call stack.
                    sys.excepthook(*sys.exc_info())

                self.plugin_state = PluginBase.PLUGIN_STATE_RUNNING

                # Ensure that the update button is shown when the plugin is untabbed and tabbed again.
                self.device_info.tab_window.add_callback_post_tab(lambda tab_window, tab_index: self.device_info_changed(self.device_info.uid), 'plugin_base_device_info_changed')

    def stop_plugin(self):
        # only stop the plugin, if it's running
        if self.plugin_state == PluginBase.PLUGIN_STATE_RUNNING:
            try:
                if hasattr(self, 'stop_comcu'):
                    self.stop_comcu()
                else:
                    self.stop()
            except:
                # Report the exception without unwinding the call stack.
                sys.excepthook(*sys.exc_info())

        # set the state to stopped even it the plugin was not actually
        # running. this stops a paused plugin from being restarted after
        # it got stopped
        self.plugin_state = PluginBase.PLUGIN_STATE_STOPPED

    def pause_plugin(self):
        if self.plugin_state == PluginBase.PLUGIN_STATE_RUNNING:
            try:
                if hasattr(self, 'stop_comcu'):
                    self.stop_comcu()
                else:
                    self.stop()
            except:
                # Report the exception without unwinding the call stack.
                sys.excepthook(*sys.exc_info())

            self.plugin_state = PluginBase.PLUGIN_STATE_PAUSED

    def resume_plugin(self):
        if self.plugin_state == PluginBase.PLUGIN_STATE_PAUSED:
            try:
                if hasattr(self, 'start_comcu'):
                    self.start_comcu()
                else:
                    self.start()
            except:
                # Report the exception without unwinding the call stack.
                sys.excepthook(*sys.exc_info())

            self.plugin_state = PluginBase.PLUGIN_STATE_RUNNING

    def destroy_plugin(self):
        # destroy plugin first, then cleanup the UI stuff

        try:
            self.destroy()
        except:
            # Report the exception without unwinding the call stack.
            sys.excepthook(*sys.exc_info())

        # before destroying the widgets ensure that all callbacks are
        # unregistered. callbacks a typically bound to Qt slots. the plugin
        # tab might already be gone but the actual device object might still
        # be alive as gets callbacks delivered to it. this callback will then
        # try to call non-existing Qt slots and trigger a segfault
        if self.device is not None:
            self.device.registered_callbacks = {}

        # Disconnect from infos_changed before destroying the widgets, because
        # self.device_infos_changed accesses the widgets.
        inventory.info_changed.disconnect(self.device_info_changed)

        # disconnect all signals to ensure that callbacks that already emitted
        # a signal don't get delivered anymore after this point
        try:
            self.disconnect()
        except TypeError:
            # fallback for PyQt versions that miss parameterless disconnect()
            for member in dir(self):
                # FIXME: filtering by name prefix is not so robust
                if member.startswith('qtcb_'):
                    obj = getattr(self, member)

                    if isinstance(obj, pyqtBoundSignal):
                        try:
                            obj.disconnect()
                        except:
                            pass

        # If the plugin's tab is detached, we need to close the containing toplevel
        # window explicitly, or else all widgets are removed, but the window stays open.
        if self.device_info.tab_window.toplevel_window is not None:
            self.device_info.tab_window.toplevel_window.close()

        # ensure that the widgets gets correctly destroyed. otherwise QWidgets
        # tend to leak as Python is not able to collect their PyQt object
        """for member in dir(self):
            print "Current member = " + member
            obj = getattr(self, member)

            if isinstance(obj, QWidget):
                obj.hide()
                obj.setParent(None)

                setattr(self, member, None)"""

    def increase_error_count(self):
        self.error_count += 1

        # as this function might be called after the plugin tab is
        # already destroyed this can raise a
        #
        # RuntimeError: underlying C/C++ object has been deleted
        #
        # therefore, wrap all Qt calls into try/except blocks
        if self.label_timeouts_title != None:
            try:
                self.label_timeouts_title.setStyleSheet('QLabel { color: red; font: bold; }')
            except:
                pass

        if self.label_timeouts != None:
            try:
                self.label_timeouts.setStyleSheet('QLabel { color: red; font: bold; }')
                self.label_timeouts.setText('{0}'.format(self.error_count))
            except:
                pass

    def set_configs(self, configs):
        self.configs = configs

    def get_configs(self):
        return self.configs

    def set_actions(self, actions):
        self.actions = actions

    def get_actions(self):
        return self.actions

    def get_url_part(self):
        if self.device_class != None:
            return self.device_class.DEVICE_URL_PART

        return 'unknown'

    @staticmethod
    def has_device_identifier(_device_identifier):
        return False

    # All below to be overridden by inheriting class
    def stop(self):
        pass

    def start(self):
        pass

    def destroy(self):
        pass

    def has_custom_version(self, _label_version_name, _label_version):
        return False

    def is_hardware_version_relevant(self):
        return False

    def get_health_metric_names(self):
        if self.device_info.kind == 'brick':
            return ['SPITFP ACK Checksum Errors', 'SPITFP Message Checksum Errors', 'SPITFP Frame Errors', 'SPITFP Overflow Errors']

        return []

    def get_health_metric_values(self):
        if self.device_info.kind == 'brick':
            spitfp_ack_checksum_errors = []
            spitfp_message_checksum_errors = []
            spitfp_frame_errors = []
            spitfp_overflow_errors = []

            for bricklet_port in self.device_info.bricklet_ports:
                spitfp_error_count = self.device.get_spitfp_error_count(bricklet_port)

                spitfp_ack_checksum_errors.append('{0}: {1}'.format(bricklet_port.upper(), spitfp_error_count.error_count_ack_checksum))
                spitfp_message_checksum_errors.append('{0}: {1}'.format(bricklet_port.upper(), spitfp_error_count.error_count_message_checksum))
                spitfp_frame_errors.append('{0}: {1}'.format(bricklet_port.upper(), spitfp_error_count.error_count_frame))
                spitfp_overflow_errors.append('{0}: {1}'.format(bricklet_port.upper(), spitfp_error_count.error_count_overflow))

            return {
                'SPITFP ACK Checksum Errors': ', '.join(spitfp_ack_checksum_errors),
                'SPITFP Message Checksum Errors': ', '.join(spitfp_message_checksum_errors),
                'SPITFP Frame Errors': ', '.join(spitfp_frame_errors),
                'SPITFP Overflow Errors': ', '.join(spitfp_overflow_errors)
            }

        return {}
