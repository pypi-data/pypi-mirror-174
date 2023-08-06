# Have a piece of SugarPie

SugarPie is a Python library to drive the PiSugar UPS / Battery (https://github.com/PiSugar).

The main motivations to create this library are:
- The official driver takes the form of a web server, which is not always practical.
- The official driver does not support all the features of the product (eg: the watchdog).

This library is based upon the official documentation for the PiSugar 3 Series: https://github.com/PiSugar/PiSugar/wiki/PiSugar-3-Series

Support for other versions of the product may be added later.

## Usage
You can find some examples in the contrib directory with some `systemd` services and corresponding
Python scripts that use the library.

Basically in your code you just have to import and instanciate the `Pisugar` class and then use
the methods you need:  
`from sugarpie.pisugar import Pisugar`  
`pisugar = Pisugar()`  
`pisugar.turn_on_system_watchdog()`  
`pisugar.turn_off_system_watchdog()`  

(Be careful if you run the example above, when you turn on the system watchdog you need to reset it
regularly or the PiSugar will restart the power! You can find a complete example in the
contrib/systemd folder.)

## Supported Features
The goal is to support all the features advertised officially in the PiSugar documentation. Here
is a list of the currently supported features.  
You can find more details within the `src/pisugar.py` module where each feature should have its
corresponding method with a well described docstring.

- Sytem Watchdog: turn on, turn off and reset the watchdog.

## How it works
Everything happens over the i2c bus by setting bits at specific addresses. It depends on the SMBus
library.

## Contributing
Contributions are welcome. The project is organized such as it should be simple to just add
new support, withtout having to modify the current structure (*trying* to respect the SOLID principles).  
When contributing, please format your code with [Black](https://github.com/psf/black), or the CI
will break.

## License
MIT License.
