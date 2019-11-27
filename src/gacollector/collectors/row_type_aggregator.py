import csv
import decimal
from _pydecimal import Decimal, DecimalException

from gacollector.settings.constants import CSV_NULL_VALUES


class RowTypeAggregator:
    @staticmethod
    def try_parse_default_values(row: csv.OrderedDict):
        if (None in row.values()) | ('-' in row.values()):
            return None
        for col in row.keys():
            val = row[col]
            if '$' in val:
                try:
                    Decimal(RowTypeAggregator.str_to_decimal(val))
                    yield col, Decimal()
                    continue
                except DecimalException:
                    pass
            try:
                int(val)
                yield col, int(0)
                continue
            except ValueError:
                pass
            try:
                float(val)
                yield col, float(0.0)
                continue
            except ValueError:
                yield col, str('-')

    @staticmethod
    def get_row_default_values(row: csv.OrderedDict):
        return csv.OrderedDict(RowTypeAggregator.try_parse_default_values(row))

    @staticmethod
    def str_to_decimal(val):
        return val.replace('$', '').replace(',', '').replace(' ', '')

    @staticmethod
    def increment_row_by_row(row, row_def):
        for col_name, col_val in row.items():
            if col_name not in row_def.keys():
                continue  # If this col not specified
            _type = type(row_def[col_name])
            if _type in (str, None):
                continue
            if col_val in CSV_NULL_VALUES:
                col_val = '0'
            if _type is Decimal:
                col_val = RowTypeAggregator.str_to_decimal(col_val)
                col_val = col_val.replace('<$0.01', '0.01')
            try:
                col_val = _type(col_val)
            except ValueError:
                print(f'Error value={col_val} in file : ', row_def)
                col_val = 0
            except decimal.InvalidOperation:
                print(f'Error value={col_val} in file : ', row_def)
                col_val = 0
            row_def[col_name] += col_val
        return row_def
