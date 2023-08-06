# BE Modbus Wrapper

[![Downloads](https://pepy.tech/badge/be-modbus-wrapper)](https://pepy.tech/project/be-modbus-wrapper)
![Release](https://img.shields.io/github/v/release/brainelectronics/be-modbus-wrapper?include_prereleases&color=success)
![Python](https://img.shields.io/badge/python3-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/github/brainelectronics/be-modbus-wrapper/branch/main/graph/badge.svg)](https://app.codecov.io/github/brainelectronics/be-modbus-wrapper)

Custom brainelectronics python modbus wrapper

---------------

## General

Custom brainelectronics specific python modbus wrapper.

<!-- MarkdownTOC -->

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
	- [Unittests](#unittests)
- [Credits](#credits)

<!-- /MarkdownTOC -->


## Installation

```bash
pip install be-modbus-wrapper
```

## Usage

```python
from be_modbus_wrapper import ModbusWrapper
```

## Contributing

### Unittests

Run the unittests locally with the following command after installing this
package in a virtual environment

```bash
# run all tests
nose2 --config tests/unittest.cfg

# run only one specific tests
nose2 tests.test_modbus_wrapper.TestModbusWrapper.test_load_modbus_registers_file
```

Generate the coverage files with

```bash
python create_report_dirs.py
coverage html
```

The coverage report is placed at `be-modbus-wrapper/reports/coverage/html/index.html`

## Credits

Based on the [PyPa sample project][ref-pypa-sample].

<!-- Links -->
[ref-pypa-sample]: https://github.com/pypa/sampleproject
