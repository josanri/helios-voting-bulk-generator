import os
import re
import csv
import uuid
import argparse
import logging

email_regx = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class EmptyFileException(Exception):
    "Raised when the a file is empty"
    pass

class CSVFormatException(Exception):
    "Raised when the a row does not match the csv structure required"
    def __init__(self, message="Bad format"):
        self.message = message
        super().__init__(self.message)

def generate_password():
    return str(uuid.uuid4())

def generate_bulk(input_file: str, output_file: str):
    """
    Generate passwords and UUIDs for each line in an input CSV file and create a new output CSV file.

    Parameters
    ----------
    input_file : str
        Path to the input CSV file containing email addresses and names.

    output_file : str
        Path to the output CSV file where the processed data with passwords and UUIDs will be saved.

    Returns
    -------
    None
        It doesn't return a value, but it generates an output CSV file with the processed data.
    """
    try:
        input_file_stat = os.stat(input_file)
        if input_file_stat == 0:
            raise EmptyFileException
        with open(input_file, 'r', encoding="utf8") as csv_in, open(output_file, 'w', newline='', encoding="utf8") as csv_out:
            reader = csv.reader(csv_in)
            writer = csv.writer(csv_out)
            row_counter = 0
            for row in reader:
                row_counter += 1
                if len(row) == 0:
                    continue
                if len(row) != 2:
                    raise CSVFormatException(message=f"Bad format at line {row_counter}, expected <email>,<username>, but got {row}")
                email, name = row
                if not re.match(email_regx, email):
                    logging.warning(f"Line {row_counter} seems to have a bad email format: {email}")
                writer.writerow(['password', generate_password(), email, name])
            if row_counter == 0:
                raise EmptyFileException
    except FileNotFoundError:
        logging.error(f"file '{input_file}' was not found")
        exit(1)
    except PermissionError:
        logging.error(f"'{input_file}' cannot be read")
        exit(1)
    except CSVFormatException as msg_error:
        logging.error(f"{msg_error}")
        exit(1)
    except EmptyFileException:
        logging.error(f"file '{input_file}' is empty")
        exit(1)
    except Exception as e:
        logging.error(f"Unknown error, could not process '{input_file}' {e}")
        exit(1)
    logging.info(f"CSV generated on file '{output_file}'")

def configure_logger(disable_warnings: bool):
    logging.basicConfig(format='%(levelname)s - %(message)s')
    if disable_warnings:
        logging.getLogger().setLevel(logging.ERROR)
    else:
        logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='main.py',
                                    description="Adds password and uuid for Helios voting system bulk upload.")
    parser.add_argument("-i", "--input",
                        default="input.csv", type=str, required=False,
                        help=".csv filename with format <email>,<username>")
    parser.add_argument("-o", "--output",
                        default="output.csv", type=str, required=False,
                        help=".csv filename with format password,<uuid_generated>,<email>,<username>")
    parser.add_argument("--disable_warnings", action="store_true", help="Disable warnings messages for email format")

    args = parser.parse_args()
    configure_logger(args.disable_warnings)
    generate_bulk(args.input, args.output)
