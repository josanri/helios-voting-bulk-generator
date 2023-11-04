# Project Name

A uuid generator for Helios Bulk generator system.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

In order to use theis
```bash
pip install -r requirements.txt
```
## Usage
Explain how to use your project. Provide code examples and any additional information that may be helpful to users.

```bash
usage: python main.py [-h] [-i <input_file>] [-o <output_file>] [--disable_warnings]

Adds password and uuid fitting Helios voting system bulk upload requirements.

options:
  -h, --help            show this help message and exit
  -i <input_file>, --input <input_file>
                        .csv filename with format <email>,<username>
  -o <output_file>, --output <output_file>
                        .csv filename with format password,<uuid_generated>,<email>,<username>
  --disable_warnings    Disable warnings messages on email format
```

### Usage example
**emails.csv**
```
bob@gmail.com,bob
```
**Executing the program**
```bash
python -i emails.csv -o result.csv
```
**result.csv**
```
password,b94e0627-72dc-4833-9207-4dea818eb7fe,bob@gmail.com,bob
```
## License
This project is licensed under the MIT License - see the LICENSE file for details
