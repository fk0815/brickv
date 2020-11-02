# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2020-11-02.      #
#                                                           #
# Python Bindings Version 2.1.27                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data

GetDisplayConfiguration = namedtuple('DisplayConfiguration', ['contrast', 'invert'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletOLED128x64(Device):
    """
    3.3cm (1.3") OLED display with 128x64 pixels
    """

    DEVICE_IDENTIFIER = 263
    DEVICE_DISPLAY_NAME = 'OLED 128x64 Bricklet'
    DEVICE_URL_PART = 'oled_128x64' # internal



    FUNCTION_WRITE = 1
    FUNCTION_NEW_WINDOW = 2
    FUNCTION_CLEAR_DISPLAY = 3
    FUNCTION_SET_DISPLAY_CONFIGURATION = 4
    FUNCTION_GET_DISPLAY_CONFIGURATION = 5
    FUNCTION_WRITE_LINE = 6
    FUNCTION_GET_IDENTITY = 255


    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon, BrickletOLED128x64.DEVICE_IDENTIFIER, BrickletOLED128x64.DEVICE_DISPLAY_NAME)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletOLED128x64.FUNCTION_WRITE] = BrickletOLED128x64.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED128x64.FUNCTION_NEW_WINDOW] = BrickletOLED128x64.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED128x64.FUNCTION_CLEAR_DISPLAY] = BrickletOLED128x64.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED128x64.FUNCTION_SET_DISPLAY_CONFIGURATION] = BrickletOLED128x64.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED128x64.FUNCTION_GET_DISPLAY_CONFIGURATION] = BrickletOLED128x64.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletOLED128x64.FUNCTION_WRITE_LINE] = BrickletOLED128x64.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED128x64.FUNCTION_GET_IDENTITY] = BrickletOLED128x64.RESPONSE_EXPECTED_ALWAYS_TRUE


        ipcon.add_device(self)

    def write(self, data):
        """
        Appends 64 byte of data to the window as set by :func:`New Window`.

        Each row has a height of 8 pixels which corresponds to one byte of data.

        Example: if you call :func:`New Window` with column from 0 to 127 and row
        from 0 to 7 (the whole display) each call of :func:`Write` (red arrow) will
        write half of a row.

        .. image:: /Images/Bricklets/bricklet_oled_128x64_display.png
           :scale: 100 %
           :alt: Display pixel order
           :align: center
           :target: ../../_images/Bricklets/bricklet_oled_128x64_display.png

        The LSB (D0) of each data byte is at the top and the MSB (D7) is at the
        bottom of the row.

        The next call of :func:`Write` will write the second half of the row
        and the next two the second row and so on. To fill the whole display
        you need to call :func:`Write` 16 times.
        """
        self.check_validity()

        data = list(map(int, data))

        self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_WRITE, (data,), '64B', 0, '')

    def new_window(self, column_from, column_to, row_from, row_to):
        """
        Sets the window in which you can write with :func:`Write`. One row
        has a height of 8 pixels.
        """
        self.check_validity()

        column_from = int(column_from)
        column_to = int(column_to)
        row_from = int(row_from)
        row_to = int(row_to)

        self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_NEW_WINDOW, (column_from, column_to, row_from, row_to), 'B B B B', 0, '')

    def clear_display(self):
        """
        Clears the current content of the window as set by :func:`New Window`.
        """
        self.check_validity()

        self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_CLEAR_DISPLAY, (), '', 0, '')

    def set_display_configuration(self, contrast, invert):
        """
        Sets the configuration of the display.

        You can set a contrast value from 0 to 255 and you can invert the color
        (black/white) of the display.
        """
        self.check_validity()

        contrast = int(contrast)
        invert = bool(invert)

        self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_SET_DISPLAY_CONFIGURATION, (contrast, invert), 'B !', 0, '')

    def get_display_configuration(self):
        """
        Returns the configuration as set by :func:`Set Display Configuration`.
        """
        self.check_validity()

        return GetDisplayConfiguration(*self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_GET_DISPLAY_CONFIGURATION, (), '', 10, 'B !'))

    def write_line(self, line, position, text):
        """
        Writes text to a specific line with a specific position.
        The text can have a maximum of 26 characters.

        For example: (1, 10, "Hello") will write *Hello* in the middle of the
        second line of the display.

        You can draw to the display with :func:`Write` and then add text to it
        afterwards.

        The display uses a special 5x7 pixel charset. You can view the characters
        of the charset in Brick Viewer.
        """
        self.check_validity()

        line = int(line)
        position = int(position)
        text = create_string(text)

        self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_WRITE_LINE, (line, position, text), 'B B 26s', 0, '')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c', 'd', 'e', 'f', 'g' or 'h' (Bricklet Port).
        A Bricklet connected to an :ref:`Isolator Bricklet <isolator_bricklet>` is always at
        position 'z'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletOLED128x64.FUNCTION_GET_IDENTITY, (), '', 33, '8s 8s c 3B 3B H'))

OLED128x64 = BrickletOLED128x64 # for backward compatibility
