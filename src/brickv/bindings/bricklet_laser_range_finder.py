# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2015-03-06.      #
#                                                           #
# Bindings Version 2.1.4                                    #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################

try:
    from collections import namedtuple
except ImportError:
    try:
        from .ip_connection import namedtuple
    except ValueError:
        from ip_connection import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error
except ValueError:
    from ip_connection import Device, IPConnection, Error

GetDistanceCallbackThreshold = namedtuple('DistanceCallbackThreshold', ['option', 'min', 'max'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletLaserRangeFinder(Device):
    """
    Device that measures distance with a laser range finder
    """

    DEVICE_IDENTIFIER = 255
    DEVICE_DISPLAY_NAME = 'Laser Range Finder Bricklet'

    CALLBACK_DISTANCE = 8
    CALLBACK_DISTANCE_REACHED = 9

    FUNCTION_GET_DISTANCE_VALUE = 1
    FUNCTION_SET_DISTANCE_CALLBACK_PERIOD = 2
    FUNCTION_GET_DISTANCE_CALLBACK_PERIOD = 3
    FUNCTION_SET_DISTANCE_CALLBACK_THRESHOLD = 4
    FUNCTION_GET_DISTANCE_CALLBACK_THRESHOLD = 5
    FUNCTION_SET_DEBOUNCE_PERIOD = 6
    FUNCTION_GET_DEBOUNCE_PERIOD = 7
    FUNCTION_SET_MOVING_AVERAGE = 10
    FUNCTION_GET_MOVING_AVERAGE = 11
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_VALUE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_THRESHOLD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_THRESHOLD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_DEBOUNCE_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_DEBOUNCE_PERIOD] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.CALLBACK_DISTANCE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletLaserRangeFinder.CALLBACK_DISTANCE_REACHED] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_SET_MOVING_AVERAGE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_MOVING_AVERAGE] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLaserRangeFinder.FUNCTION_GET_IDENTITY] = BrickletLaserRangeFinder.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletLaserRangeFinder.CALLBACK_DISTANCE] = 'H'
        self.callback_formats[BrickletLaserRangeFinder.CALLBACK_DISTANCE_REACHED] = 'H'

    def get_distance_value(self):
        """
        TODO
        
        If you want to get the distance value periodically, it is recommended to
        use the callback :func:`Distance` and set the period with 
        :func:`SetDistanceCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_VALUE, (), '', 'H')

    def set_distance_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Distance` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Distance` is only triggered if the distance value has changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_PERIOD, (period,), 'I', '')

    def get_distance_callback_period(self):
        """
        Returns the period as set by :func:`SetDistanceCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_PERIOD, (), '', 'I')

    def set_distance_callback_threshold(self, option, min, max):
        """
        Sets the thresholds for the :func:`DistanceReached` callback. 
        
        The following options are possible:
        
        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100
        
         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"
        
        The default value is ('x', 0, 0).
        """
        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_DISTANCE_CALLBACK_THRESHOLD, (option, min, max), 'c h h', '')

    def get_distance_callback_threshold(self):
        """
        Returns the threshold as set by :func:`SetDistanceCallbackThreshold`.
        """
        return GetDistanceCallbackThreshold(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DISTANCE_CALLBACK_THRESHOLD, (), '', 'c h h'))

    def set_debounce_period(self, debounce):
        """
        Sets the period in ms with which the threshold callbacks
        
        * :func:`DistanceReached`,
        
        are triggered, if the thresholds
        
        * :func:`SetDistanceCallbackThreshold`,
        
        keep being reached.
        
        The default value is 100.
        """
        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_DEBOUNCE_PERIOD, (debounce,), 'I', '')

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`SetDebouncePeriod`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_DEBOUNCE_PERIOD, (), '', 'I')

    def set_moving_average(self, length):
        """
        Sets the length of a `moving averaging <http://en.wikipedia.org/wiki/Moving_average>`__ 
        for the distance.
        
        Setting the length to 0 will turn the averaging completely off. With less
        averaging, there is more noise on the data.
        
        The range for the averaging is 0-50.
        
        The default value is 20.
        """
        self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_SET_MOVING_AVERAGE, (length,), 'B', '')

    def get_moving_average(self):
        """
        Returns the length moving average as set by :func:`SetMovingAverage`.
        """
        return self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_MOVING_AVERAGE, (), '', 'B')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletLaserRangeFinder.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

LaserRangeFinder = BrickletLaserRangeFinder # for backward compatibility
