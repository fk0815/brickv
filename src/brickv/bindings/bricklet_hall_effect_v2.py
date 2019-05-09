# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2019-05-09.      #
#                                                           #
# Python Bindings Version 2.1.21                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

#### __DEVICE_IS_NOT_RELEASED__ ####

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data

GetMagneticFluxDensityCallbackConfiguration = namedtuple('MagneticFluxDensityCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetCounterConfig = namedtuple('CounterConfig', ['high_threshold', 'low_threshold', 'debounce'])
GetCounterCallbackConfiguration = namedtuple('CounterCallbackConfiguration', ['period', 'value_has_to_change'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletHallEffectV2(Device):
    """
    Measures magnetic flux density between -7mT and +7mT
    """

    DEVICE_IDENTIFIER = 2132
    DEVICE_DISPLAY_NAME = 'Hall Effect Bricklet 2.0'
    DEVICE_URL_PART = 'hall_effect_v2' # internal

    CALLBACK_MAGNETIC_FLUX_DENSITY = 4
    CALLBACK_COUNTER = 10


    FUNCTION_GET_MAGNETIC_FLUX_DENSITY = 1
    FUNCTION_SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION = 3
    FUNCTION_GET_COUNTER = 5
    FUNCTION_SET_COUNTER_CONFIG = 6
    FUNCTION_GET_COUNTER_CONFIG = 7
    FUNCTION_SET_COUNTER_CALLBACK_CONFIGURATION = 8
    FUNCTION_GET_COUNTER_CALLBACK_CONFIGURATION = 9
    FUNCTION_GET_SPITFP_ERROR_COUNT = 234
    FUNCTION_SET_BOOTLOADER_MODE = 235
    FUNCTION_GET_BOOTLOADER_MODE = 236
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_SET_STATUS_LED_CONFIG = 239
    FUNCTION_GET_STATUS_LED_CONFIG = 240
    FUNCTION_GET_CHIP_TEMPERATURE = 242
    FUNCTION_RESET = 243
    FUNCTION_WRITE_UID = 248
    FUNCTION_READ_UID = 249
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'
    BOOTLOADER_MODE_BOOTLOADER = 0
    BOOTLOADER_MODE_FIRMWARE = 1
    BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4
    BOOTLOADER_STATUS_OK = 0
    BOOTLOADER_STATUS_INVALID_MODE = 1
    BOOTLOADER_STATUS_NO_CHANGE = 2
    BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3
    BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4
    BOOTLOADER_STATUS_CRC_MISMATCH = 5
    STATUS_LED_CONFIG_OFF = 0
    STATUS_LED_CONFIG_ON = 1
    STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
    STATUS_LED_CONFIG_SHOW_STATUS = 3

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_MAGNETIC_FLUX_DENSITY] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION] = BrickletHallEffectV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_COUNTER] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_SET_COUNTER_CONFIG] = BrickletHallEffectV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_COUNTER_CONFIG] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_SET_COUNTER_CALLBACK_CONFIGURATION] = BrickletHallEffectV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_COUNTER_CALLBACK_CONFIGURATION] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletHallEffectV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletHallEffectV2.FUNCTION_WRITE_FIRMWARE] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletHallEffectV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_RESET] = BrickletHallEffectV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletHallEffectV2.FUNCTION_WRITE_UID] = BrickletHallEffectV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletHallEffectV2.FUNCTION_READ_UID] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletHallEffectV2.FUNCTION_GET_IDENTITY] = BrickletHallEffectV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletHallEffectV2.CALLBACK_MAGNETIC_FLUX_DENSITY] = 'h'
        self.callback_formats[BrickletHallEffectV2.CALLBACK_COUNTER] = 'I'


    def get_magnetic_flux_density(self):
        """
        Returns the `magnetic flux density (magnetic induction) <https://en.wikipedia.org/wiki/Magnetic_flux>`__
        in `µT (micro Tesla) <https://en.wikipedia.org/wiki/Tesla_(unit)>`__.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Magnetic Flux Density` callback. You can set the callback configuration
        with :func:`Set Magnetic Flux Density Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_MAGNETIC_FLUX_DENSITY, (), '', 'h')

    def set_magnetic_flux_density_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Magnetic Flux Density` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Magnetic Flux Density` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c h h', '')

    def get_magnetic_flux_density_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Magnetic Flux Density Callback Configuration`.
        """
        return GetMagneticFluxDensityCallbackConfiguration(*self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION, (), '', 'I ! c h h'))

    def get_counter(self, reset_counter):
        """
        Returns the current value of the counter.

        You can configure the low/high thresholds in µT and the debounce time
        in us with :func:`Set Counter Config`.

        If you set reset counter to *true*, the count is set back to 0
        directly after it is read.

        If you want to get the count periodically, it is recommended to use the
        :cb:`Counter` callback. You can set the callback configuration
        with :func:`Set Counter Callback Configuration`.
        """
        reset_counter = bool(reset_counter)

        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_COUNTER, (reset_counter,), '!', 'I')

    def set_counter_config(self, high_threshold, low_threshold, debounce):
        """
        Sets a high and a low threshold in µT as well as a debounce time in µs.

        If the measured magnetic flux density goes above the high threshold or
        below the low threshold, the count of the counter is increased by 1.

        The debounce time is the minimum time between two count increments.

        The default values are

        * High Threshold: 2000µT
        * Low Threshold: -2000µT
        * Debounce: 100000µs (100ms)
        """
        high_threshold = int(high_threshold)
        low_threshold = int(low_threshold)
        debounce = int(debounce)

        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_SET_COUNTER_CONFIG, (high_threshold, low_threshold, debounce), 'h h I', '')

    def get_counter_config(self):
        """
        Returns the counter config as set by :func:`Set Counter Config`.
        """
        return GetCounterConfig(*self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_COUNTER_CONFIG, (), '', 'h h I'))

    def set_counter_callback_configuration(self, period, value_has_to_change):
        """
        The period in ms is the period with which the :cb:`Counter`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after at least one of the values has changed. If the values didn't
        change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        The default value is (0, false).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)

        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_SET_COUNTER_CALLBACK_CONFIGURATION, (period, value_has_to_change), 'I !', '')

    def get_counter_callback_configuration(self):
        """
        Returns the callback configuration as set by
        :func:`Set Counter Callback Configuration`.
        """
        return GetCounterCallbackConfiguration(*self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_COUNTER_CALLBACK_CONFIGURATION, (), '', 'I !'))

    def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier and CRC are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        mode = int(mode)

        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        data = list(map(int, data))

        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletHallEffectV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

HallEffectV2 = BrickletHallEffectV2 # for backward compatibility
