"""
Parsing for PiCARD data files.

Use class, Picard, to parse metadata from valid files. See method,
Picard.parse, for expected format and details of functionality.
"""

import re

from enum import IntEnum

from ..metadata import MetadataItem
from .base import BaseParser


class InvalidRowException(Exception):
    pass


class ExcelCellType(IntEnum):
    """
    Cell types from xlrd docs based on Excel types.
    https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Cell
    """
    EMPTY = 0
    TEXT = 1
    NUMBER = 2
    DATE = 3
    BOOLEAN = 4
    ERROR = 5


class Picard(BaseParser):
    """
    A parser tailored to PiCARD test data files.

    Parameters
    ----------
    file_path : str
        A path to a PiCARD test file.
    """

    VALID_EXTENSIONS = {'xls'}

    DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S %p'

    def parse(self):
        """
        Iterate through each row in the "Details" sheet of an .xls
        excel file and parse metadata.

        Expected format:

        column 1            | column 2
        -------------------------------------------------
        Filename	        | example
        Geometry name	    | example
        Procedure name	    | Options
                            | example1
                            | Options
                            | example2
        [Parameters]        |
        Name	            | example
        Instrument type	    | example
        -------------------------------------------------

        Subsections titles (enclosed in brackets with empty column 2)
        are prepended to subsequent keys; there can be 0 to many subsections:
            {
                key='[Parameters]Name',
                value='example',
            }
            {
                key='[Parameters]Instrument type',
                value='example',
            }

        Options (found below a column 2 value of 'Option') are concatenated
        into a single value:
            {
                key='Procedure name'
                value='example1, example2'
            }
        """
        # Import packages locally to avoid polluting global memory.
        import xlrd
        from xlrd import XLRDError

        workbook = xlrd.open_workbook(self.file_path)

        try:
            details_sheet = workbook.sheet_by_name('Details')
        except XLRDError:
            # 'Details' page not found
            self.metadata = []
            return

        # Matches any characters between brackets. E.g. '[Parameters]'
        subsection_pattern = re.compile(r'\[[^\]]*\]')

        subsection = ''
        options = False
        options_key = ''
        options_value = ''
        metadata = []

        for row in details_sheet.get_rows():
            if len(row) != 2:
                raise InvalidRowException(
                    f"Expected 2 cells, found {len(row)}"
                )

            key_cell, value_cell = row
            key_cell_type = ExcelCellType(key_cell.ctype)
            value_cell_type = ExcelCellType(value_cell.ctype)

            # --------------- Key parsing -------------
            # options is true if previous row's value == 'Options'
            if options:
                if key_cell_type == ExcelCellType.EMPTY:
                    if value_cell.value == 'Options':
                        continue

                    options_value += value_cell.value + ', '
                    continue
                else:
                    options = False
                    metadata.append(MetadataItem(
                        key=options_key,
                        value=options_value.strip(', ')
                    ))
                    options_key = ''
                    options_value = ''

            if value_cell.value == 'Options':
                if key_cell_type == ExcelCellType.EMPTY:
                    raise InvalidRowException(
                        "No key found for 'Options' value."
                    )
                options_key = key_cell.value
                options = True
                continue

            subsection_match = subsection_pattern.search(key_cell.value)

            if subsection_match:
                subsection = subsection_match.group()

                if value_cell_type != ExcelCellType.EMPTY:
                    raise InvalidRowException(
                        f"Subsection found with value {value_cell.value}"
                    )
                continue

            # ------------ Value Parsing -----------------
            units = None

            if value_cell_type == ExcelCellType.EMPTY:
                value = ''

            elif value_cell_type == ExcelCellType.TEXT:
                value_split = value_cell.value.split()
                if len(value_split) == 2:
                    try:
                        value = float(value_split[0])
                        units = value_split[1]
                    except ValueError:
                        value = value_cell.value
                else:
                    value = value_cell.value

            elif value_cell_type == ExcelCellType.NUMBER:
                value = value_cell.value

            elif value_cell_type == ExcelCellType.DATE:
                value = xlrd.xldate_as_datetime(
                    value_cell.value, 0
                    ).strftime(self.DATETIME_FORMAT)

            elif value_cell_type == ExcelCellType.BOOLEAN:
                if value_cell.value == 0:
                    value = 'False',
                elif value_cell.value == 1:
                    value = 'True'
                else:
                    raise ValueError(
                        f"BOOLEAN must be 0 or 1. "
                        "Found {value_cell.value}")

            elif value_cell_type == ExcelCellType.ERROR:
                # Convert to Excel error text
                value = xlrd.error_text_from_code[value_cell.value]

            metadata.append(MetadataItem(
                key=(subsection + key_cell.value),
                value=value,
                units=units
            ))

        if options:
                options = False
                metadata.append(MetadataItem(
                    key=options_key,
                    value=options_value.strip(', ')
                ))
                options_key = ''
                options_value = ''

        self.metadata = metadata
