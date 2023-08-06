"""Module for the class that implements the controller for the PiSugar."""
import logging

from .constants import Constants
from .helpers import connection_to_i2c, pisugar_set_bit

constants = Constants


class Pisugar:
    """Implements the various controls of the PiSugar."""

    def _set_system_watchdog_timeout(self, timeout=30):
        """Set the system watchdog timeout in seconds."""
        timeout //= 2  # the pisugar needs timeout divided by 2

        with connection_to_i2c() as i2c:
            i2c.write_byte_data(
                constants.PISUGAR_I2C_ADDRESS,
                constants.WATCHDOG_TIMEOUT_ADDRESS,
                timeout,
            )

    def turn_on_system_watchdog(self):
        """
        Set the system watchdog timeout
        and then the bit of the system watchdog to on.
        """
        self._set_system_watchdog_timeout()
        pisugar_set_bit(
            constants.WATCHDOG_ADDRESS, constants.WATCHDOG_SWITCH_BIT_INDEX, "on"
        )

    def reset_system_watchdog(self):
        """Set the system watchdog reset bit to on."""
        try:
            pisugar_set_bit(
                constants.WATCHDOG_ADDRESS,
                constants.WATCHDOG_RESET_BIT_INDEX,
                "on",
            )
        except OSError:
            logging.error("This error is expected.", exc_info=True)

    def turn_off_system_watchdog(self):
        """Set the bit of the system watchdog to off."""
        pisugar_set_bit(
            constants.WATCHDOG_ADDRESS, constants.WATCHDOG_SWITCH_BIT_INDEX, "off"
        )
