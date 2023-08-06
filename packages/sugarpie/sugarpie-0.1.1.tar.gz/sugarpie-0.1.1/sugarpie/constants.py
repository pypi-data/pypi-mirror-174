"This modules defines the PiSugar constants."
from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    RPI_I2C_BUS = 1
    PISUGAR_I2C_ADDRESS = 0x57
    WATCHDOG_ADDRESS = 0x06
    WATCHDOG_SWITCH_BIT_INDEX = 7
    WATCHDOG_RESET_BIT_INDEX = 5
    WATCHDOG_TIMEOUT_ADDRESS = 0x07
