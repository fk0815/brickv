# -*- coding: utf-8 -*-
"""
RED Plugin
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2014 Matthias Bolte <matthias@tinkerforge.com>

program_page_octave.py: Program Wizard Octave Page

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

from PyQt4.QtCore import QVariant
from brickv.plugin_system.plugins.red.program_page import ProgramPage
from brickv.plugin_system.plugins.red.program_utils import *
from brickv.plugin_system.plugins.red.ui_program_page_octave import Ui_ProgramPageOctave

def get_octave_versions(script_manager, callback):
    def cb_versions(result):
        if result != None:
            try:
                version = result.stdout.split('\n')[0].split(' ')[-1]
                callback([ExecutableVersion('/usr/bin/octave', version)])
                return
            except:
                pass

        # Could not get versions, we assume that some version of octave 3.6 is installed
        callback([ExecutableVersion('/usr/bin/octave', '3.6')])

    script_manager.execute_script('octave_versions', cb_versions)


class ProgramPageOctave(ProgramPage, Ui_ProgramPageOctave):
    def __init__(self, title_prefix='', *args, **kwargs):
        ProgramPage.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.language = Constants.LANGUAGE_OCTAVE

        self.setTitle('{0}{1} Configuration'.format(title_prefix, Constants.language_display_names[self.language]))

        self.registerField('octave.version', self.combo_version)
        self.registerField('octave.start_mode', self.combo_start_mode)
        self.registerField('octave.script_file', self.combo_script_file, 'currentText')
        self.registerField('octave.working_directory', self.combo_working_directory, 'currentText')

        self.combo_start_mode.currentIndexChanged.connect(self.update_ui_state)
        self.combo_start_mode.currentIndexChanged.connect(self.completeChanged.emit)
        self.check_show_advanced_options.stateChanged.connect(self.update_ui_state)
        self.label_spacer.setText('')

        self.combo_script_file_selector       = MandatoryTypedFileSelector(self,
                                                                           self.label_script_file,
                                                                           self.combo_script_file,
                                                                           self.label_script_file_type,
                                                                           self.combo_script_file_type,
                                                                           self.label_script_file_help)
        self.combo_working_directory_selector = MandatoryDirectorySelector(self,
                                                                           self.label_working_directory,
                                                                           self.combo_working_directory)
        self.option_list_editor               = ListWidgetEditor(self.label_options,
                                                                 self.list_options,
                                                                 self.label_options_help,
                                                                 self.button_add_option,
                                                                 self.button_remove_option,
                                                                 self.button_up_option,
                                                                 self.button_down_option,
                                                                 '<new Octave option {0}>')

    # overrides QWizardPage.initializePage
    def initializePage(self):
        self.set_formatted_sub_title(u'Specify how the {language} program [{name}] should be executed.')

        self.update_combo_version('octave', self.combo_version)

        self.combo_start_mode.setCurrentIndex(Constants.DEFAULT_OCTAVE_START_MODE)
        self.combo_script_file_selector.reset()
        self.check_show_advanced_options.setCheckState(Qt.Unchecked)
        self.combo_working_directory_selector.reset()
        self.option_list_editor.reset()
        self.option_list_editor.add_item(unicode('--silent'))

        self.is_full_image = 'full' in self.wizard().image_version_ref[0]

        if not self.is_full_image:
            self.option_list_editor.add_item(unicode('--no-window-system'))

        # if a program exists then this page is used in an edit wizard
        if self.wizard().program != None:
            program = self.wizard().program

            # start mode
            start_mode_api_name = program.cast_custom_option_value('octave.start_mode', unicode, '<unknown>')
            start_mode          = Constants.get_octave_start_mode(start_mode_api_name)

            self.combo_start_mode.setCurrentIndex(start_mode)

            # script file
            self.combo_script_file_selector.set_current_text(program.cast_custom_option_value('octave.script_file', unicode, ''))

            # working directory
            self.combo_working_directory_selector.set_current_text(unicode(program.working_directory))

            # options
            self.option_list_editor.clear()

            for option in program.cast_custom_option_value_list('octave.options', unicode, []):
                self.option_list_editor.add_item(option)

        self.update_ui_state()

    # overrides QWizardPage.isComplete
    def isComplete(self):
        executable = self.get_executable()
        start_mode = self.get_field('octave.start_mode').toInt()[0]

        if len(executable) == 0:
            return False

        if start_mode == Constants.OCTAVE_START_MODE_SCRIPT_FILE and \
           not self.combo_script_file_selector.complete:
            return False

        return self.combo_working_directory_selector.complete and ProgramPage.isComplete(self)

    # overrides ProgramPage.update_ui_state
    def update_ui_state(self):
        start_mode             = self.get_field('octave.start_mode').toInt()[0]
        start_mode_script_file = start_mode == Constants.OCTAVE_START_MODE_SCRIPT_FILE
        show_advanced_options  = self.check_show_advanced_options.checkState() == Qt.Checked

        self.combo_script_file_selector.set_visible(start_mode_script_file)
        self.combo_working_directory_selector.set_visible(show_advanced_options)
        self.option_list_editor.set_visible(show_advanced_options)
        self.label_spacer.setVisible(not show_advanced_options)

        self.option_list_editor.update_ui_state()

    def get_executable(self):
        return unicode(self.combo_version.itemData(self.get_field('octave.version').toInt()[0]).toString())

    def get_html_summary(self):
        version           = self.get_field('octave.version').toInt()[0]
        start_mode        = self.get_field('octave.start_mode').toInt()[0]
        script_file       = self.get_field('octave.script_file').toString()
        working_directory = self.get_field('octave.working_directory').toString()
        options           = ' '.join(self.option_list_editor.get_items())

        html  = u'Octave Version: {0}<br/>'.format(Qt.escape(self.combo_version.itemText(version)))
        html += u'Start Mode: {0}<br/>'.format(Qt.escape(Constants.octave_start_mode_display_names[start_mode]))

        if start_mode == Constants.OCTAVE_START_MODE_SCRIPT_FILE:
            html += u'Script File: {0}<br/>'.format(Qt.escape(script_file))

        html += u'Working Directory: {0}<br/>'.format(Qt.escape(working_directory))
        html += u'Octave Options: {0}<br/>'.format(Qt.escape(options))

        return html

    def get_custom_options(self):
        return {
            'octave.start_mode':  Constants.octave_start_mode_api_names[self.get_field('octave.start_mode').toInt()[0]],
            'octave.script_file': unicode(self.get_field('octave.script_file').toString()),
            'octave.options':     self.option_list_editor.get_items()
        }

    def get_command(self):
        executable  = self.get_executable()
        arguments   = self.option_list_editor.get_items()
        environment = []
        start_mode  = self.get_field('octave.start_mode').toInt()[0]

        if self.is_full_image:
            environment.append(unicode('DISPLAY=:0'))

        if start_mode == Constants.OCTAVE_START_MODE_SCRIPT_FILE:
            arguments.append(unicode(self.get_field('octave.script_file').toString()))

        working_directory = unicode(self.get_field('octave.working_directory').toString())

        return executable, arguments, environment, working_directory

    def apply_program_changes(self):
        self.apply_program_custom_options_and_command_changes()
