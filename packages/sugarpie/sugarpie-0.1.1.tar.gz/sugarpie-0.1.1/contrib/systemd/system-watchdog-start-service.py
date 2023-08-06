"""
This module is meant to be launched by a systemd service.
It turns the PiSugar system watchdog on and then resets it until it is stopped.
It can be accompanied by its stop counterpart which turns the watchdog off.
"""
import time
from sugarpie.sugarpie.pisugar import Pisugar

pisugar = Pisugar()


def start_system_watchdog():
    """Ask the PiSugar to enable the watchdog and reset it forever."""
    pisugar.turn_on_system_watchdog()

    while True:
        pisugar.reset_system_watchdog()
        time.sleep(1)


if __name__ == "__main__":
    start_system_watchdog()
