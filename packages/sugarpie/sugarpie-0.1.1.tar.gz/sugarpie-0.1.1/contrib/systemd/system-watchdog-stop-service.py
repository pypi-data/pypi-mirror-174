"""
This module is meant to be launched by a systemd service.
It turns off the PiSugar system watchdog.
It can be accompanied by its start counterpart which turns the watchdog on.
"""
from sugarpie.sugarpie.pisugar import Pisugar

pisugar = Pisugar()


def stop_system_watchdog():
    """Ask PiSugar to disable the watchdog."""
    pisugar.turn_off_system_watchdog()


if __name__ == "__main__":
    stop_system_watchdog()
