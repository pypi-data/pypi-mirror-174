"""Helper functions for the controller."""
from contextlib import contextmanager

from smbus import SMBus

from .constants import Constants

constants = Constants()


@contextmanager
def connection_to_i2c():
    """Context manager to establish the connection with i2c."""
    i2c = SMBus(constants.RPI_I2C_BUS)
    yield i2c
    i2c.close()


def _set_bit(byte, index):
    return byte | (1 << index)


def _clear_bit(byte, index):
    return byte & ~(1 << index)


def pisugar_set_bit(address: int, index: int, state: str) -> None:
    """
    Set a specific bit on a given address of the PiSugar.

    Examples:
        >>> pisugar_set_bit(0x06, 7, 'on')
        >>> pisugar_set_bit(0x06, 7, 'off')

    Args:
        address: The address to set the bits to.
        index: The index of the bit to set within the byte, starting with 0
        on the least significant bit and ending with 7 on the most significant
        bit.
        state: A string, on or off, to specify the desired bit state.
    """
    if state not in ["on", "off"]:
        raise TypeError("State needs to be on or off")

    with connection_to_i2c() as i2c:
        current_byte_value = i2c.read_byte_data(constants.PISUGAR_I2C_ADDRESS, address)

        if state == "on":
            new_byte_value = _set_bit(current_byte_value, index)
        elif state == "off":
            new_byte_value = _clear_bit(current_byte_value, index)

        i2c.write_byte_data(constants.PISUGAR_I2C_ADDRESS, address, new_byte_value)
