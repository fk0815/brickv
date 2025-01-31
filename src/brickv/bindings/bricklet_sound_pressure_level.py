# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2021-05-11.      #
#                                                           #
# Python Bindings Version 2.1.29                            #
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

GetDecibelCallbackConfiguration = namedtuple('DecibelCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetSpectrumLowLevel = namedtuple('SpectrumLowLevel', ['spectrum_length', 'spectrum_chunk_offset', 'spectrum_chunk_data'])
GetConfiguration = namedtuple('Configuration', ['fft_size', 'weighting'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletSoundPressureLevel(Device):
    """
    Measures Sound Pressure Level in dB(A/B/C/D/Z)
    """

    DEVICE_IDENTIFIER = 290
    DEVICE_DISPLAY_NAME = 'Sound Pressure Level Bricklet'
    DEVICE_URL_PART = 'sound_pressure_level' # internal

    CALLBACK_DECIBEL = 4
    CALLBACK_SPECTRUM_LOW_LEVEL = 8

    CALLBACK_SPECTRUM = -8

    FUNCTION_GET_DECIBEL = 1
    FUNCTION_SET_DECIBEL_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_DECIBEL_CALLBACK_CONFIGURATION = 3
    FUNCTION_GET_SPECTRUM_LOW_LEVEL = 5
    FUNCTION_SET_SPECTRUM_CALLBACK_CONFIGURATION = 6
    FUNCTION_GET_SPECTRUM_CALLBACK_CONFIGURATION = 7
    FUNCTION_SET_CONFIGURATION = 9
    FUNCTION_GET_CONFIGURATION = 10
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
    FFT_SIZE_128 = 0
    FFT_SIZE_256 = 1
    FFT_SIZE_512 = 2
    FFT_SIZE_1024 = 3
    WEIGHTING_A = 0
    WEIGHTING_B = 1
    WEIGHTING_C = 2
    WEIGHTING_D = 3
    WEIGHTING_Z = 4
    WEIGHTING_ITU_R_468 = 5
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
        Device.__init__(self, uid, ipcon, BrickletSoundPressureLevel.DEVICE_IDENTIFIER, BrickletSoundPressureLevel.DEVICE_DISPLAY_NAME)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_DECIBEL] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_SET_DECIBEL_CALLBACK_CONFIGURATION] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_DECIBEL_CALLBACK_CONFIGURATION] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_SPECTRUM_LOW_LEVEL] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_SET_SPECTRUM_CALLBACK_CONFIGURATION] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_SPECTRUM_CALLBACK_CONFIGURATION] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_SET_CONFIGURATION] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_CONFIGURATION] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_SET_BOOTLOADER_MODE] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_BOOTLOADER_MODE] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_WRITE_FIRMWARE] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_RESET] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_WRITE_UID] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_READ_UID] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletSoundPressureLevel.FUNCTION_GET_IDENTITY] = BrickletSoundPressureLevel.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletSoundPressureLevel.CALLBACK_DECIBEL] = (10, 'H')
        self.callback_formats[BrickletSoundPressureLevel.CALLBACK_SPECTRUM_LOW_LEVEL] = (72, 'H H 30H')

        self.high_level_callbacks[BrickletSoundPressureLevel.CALLBACK_SPECTRUM] = [('stream_length', 'stream_chunk_offset', 'stream_chunk_data'), {'fixed_length': None, 'single_chunk': False}, None]
        ipcon.add_device(self)

    def get_decibel(self):
        """
        Returns the measured sound pressure in decibels.

        The Bricklet supports the weighting standards dB(A), dB(B), dB(C), dB(D),
        dB(Z) and ITU-R 468. You can configure the weighting with :func:`Set Configuration`.

        By default dB(A) will be used.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Decibel` callback. You can set the callback configuration
        with :func:`Set Decibel Callback Configuration`.
        """
        self.check_validity()

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_DECIBEL, (), '', 10, 'H')

    def set_decibel_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period is the period with which the :cb:`Decibel` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Decibel` callback.

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
        """
        self.check_validity()

        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_SET_DECIBEL_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c H H', 0, '')

    def get_decibel_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Decibel Callback Configuration`.
        """
        self.check_validity()

        return GetDecibelCallbackConfiguration(*self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_DECIBEL_CALLBACK_CONFIGURATION, (), '', 18, 'I ! c H H'))

    def get_spectrum_low_level(self):
        """
        Returns the frequency spectrum. The length of the spectrum is between
        512 (FFT size 1024) and 64 (FFT size 128). See :func:`Set Configuration`.

        Each array element is one bin of the FFT. The first bin is always the
        DC offset and the other bins have a size between 40Hz (FFT size 1024) and
        320Hz (FFT size 128).

        In sum the frequency of the spectrum always has a range from 0 to
        20480Hz (the FFT is applied to samples with a frequency of 40960Hz).

        The returned data is already equalized, which means that the microphone
        frequency response is compensated and the weighting function is applied
        (see :func:`Set Configuration` for the available weighting standards). Use
        dB(Z) if you need the unaltered spectrum.

        The values are not in dB form yet. If you want a proper dB scale of the
        spectrum you have to apply the formula f(x) = 20*log10(max(1, x/sqrt(2)))
        on each value.
        """
        self.check_validity()

        return GetSpectrumLowLevel(*self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_SPECTRUM_LOW_LEVEL, (), '', 72, 'H H 30H'))

    def set_spectrum_callback_configuration(self, period):
        """
        The period is the period with which the :cb:`Spectrum` callback is
        triggered periodically. A value of 0 turns the callback off.

        Every new measured spectrum will be send at most once. Set the period to 1 to
        make sure that you get every spectrum.
        """
        self.check_validity()

        period = int(period)

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_SET_SPECTRUM_CALLBACK_CONFIGURATION, (period,), 'I', 0, '')

    def get_spectrum_callback_configuration(self):
        """
        Returns the callback configuration as set by
        :func:`Get Spectrum Callback Configuration`.
        """
        self.check_validity()

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_SPECTRUM_CALLBACK_CONFIGURATION, (), '', 12, 'I')

    def set_configuration(self, fft_size, weighting):
        """
        Sets the Sound Pressure Level Bricklet configuration.

        With different FFT sizes the Bricklet has a different
        amount of samples per second and the size of the FFT bins
        changes. The higher the FFT size the more precise is the result
        of the dB(X) calculation.

        Available FFT sizes are:

        * 1024: 512 bins, 10 samples per second, each bin has size 40Hz
        * 512: 256 bins, 20 samples per second, each bin has size 80Hz
        * 256: 128 bins, 40 samples per second, each bin has size 160Hz
        * 128: 64 bins, 80 samples per second, each bin has size 320Hz

        The Bricklet supports different weighting functions. You can choose
        between dB(A), dB(B), dB(C), dB(D), dB(Z) and ITU-R 468.

        dB(A/B/C/D) are the standard dB weighting curves. dB(A) is
        often used to measure volumes at concerts etc. dB(Z) has a
        flat response, no weighting is applied. ITU-R 468 is an ITU
        weighting standard mostly used in the UK and Europe.
        """
        self.check_validity()

        fft_size = int(fft_size)
        weighting = int(weighting)

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_SET_CONFIGURATION, (fft_size, weighting), 'B B', 0, '')

    def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        self.check_validity()

        return GetConfiguration(*self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_CONFIGURATION, (), '', 10, 'B B'))

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
        self.check_validity()

        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 24, 'I I I I'))

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
        self.check_validity()

        mode = int(mode)

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 9, 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        self.check_validity()

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_BOOTLOADER_MODE, (), '', 9, 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        self.check_validity()

        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', 0, '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        self.check_validity()

        data = list(map(int, data))

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 9, 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        self.check_validity()

        config = int(config)

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', 0, '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        self.check_validity()

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 9, 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        self.check_validity()

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 10, 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.check_validity()

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_RESET, (), '', 0, '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        self.check_validity()

        uid = int(uid)

        self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_WRITE_UID, (uid,), 'I', 0, '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        self.check_validity()

        return self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_READ_UID, (), '', 12, 'I')

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
        return GetIdentity(*self.ipcon.send_request(self, BrickletSoundPressureLevel.FUNCTION_GET_IDENTITY, (), '', 33, '8s 8s c 3B 3B H'))

    def get_spectrum(self):
        """
        Returns the frequency spectrum. The length of the spectrum is between
        512 (FFT size 1024) and 64 (FFT size 128). See :func:`Set Configuration`.

        Each array element is one bin of the FFT. The first bin is always the
        DC offset and the other bins have a size between 40Hz (FFT size 1024) and
        320Hz (FFT size 128).

        In sum the frequency of the spectrum always has a range from 0 to
        20480Hz (the FFT is applied to samples with a frequency of 40960Hz).

        The returned data is already equalized, which means that the microphone
        frequency response is compensated and the weighting function is applied
        (see :func:`Set Configuration` for the available weighting standards). Use
        dB(Z) if you need the unaltered spectrum.

        The values are not in dB form yet. If you want a proper dB scale of the
        spectrum you have to apply the formula f(x) = 20*log10(max(1, x/sqrt(2)))
        on each value.
        """
        with self.stream_lock:
            ret = self.get_spectrum_low_level()
            spectrum_length = ret.spectrum_length
            spectrum_out_of_sync = ret.spectrum_chunk_offset != 0
            spectrum_data = ret.spectrum_chunk_data

            while not spectrum_out_of_sync and len(spectrum_data) < spectrum_length:
                ret = self.get_spectrum_low_level()
                spectrum_length = ret.spectrum_length
                spectrum_out_of_sync = ret.spectrum_chunk_offset != len(spectrum_data)
                spectrum_data += ret.spectrum_chunk_data

            if spectrum_out_of_sync: # discard remaining stream to bring it back in-sync
                while ret.spectrum_chunk_offset + 30 < spectrum_length:
                    ret = self.get_spectrum_low_level()
                    spectrum_length = ret.spectrum_length

                raise Error(Error.STREAM_OUT_OF_SYNC, 'Spectrum stream is out-of-sync')

        return spectrum_data[:spectrum_length]

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

SoundPressureLevel = BrickletSoundPressureLevel # for backward compatibility
