import decimal
from _pydecimal import Decimal, DecimalException
from collections import OrderedDict

from gacollector.csv_utils.csv_set import CsvSet
from gacollector.settings.constants import CSV_NULL_VALUES, ADDITIONAL_HEADERS


class RowTypeAggregator:
    @staticmethod
    def col_default(column_value: str):
        if column_value.strip() in CSV_NULL_VALUES:
            return None

        if '$' in column_value or '%' in column_value:
            try:
                Decimal(RowTypeAggregator.str_to_decimal(column_value))
                return Decimal()
            except DecimalException:
                pass
        try:
            int(column_value)
            return int(0)
        except ValueError:
            pass
        try:
            float(column_value)
            return float(0.0)
        except ValueError:
            return str('-')

    # @staticmethod
    # def try_parse_default_values(row: OrderedDict):
    #     if (None in row.values()) or ('-' in row.values()) or ('' in row.values()):
    #         return 'Blank', True
    #     for col in row.keys():
    #         val = row[col]
    #
    #
    # @staticmethod
    # def get_row_default_values(row: OrderedDict):
    #     return OrderedDict(RowTypeAggregator.try_parse_default_values(row))
    #
    @staticmethod
    def get_default_values_in_set(csv_set: CsvSet):
        # ! Work only when all the files have the same headers
        # Result
        row_def = OrderedDict()

        field_names = None
        # For each file in set
        for _, reader in csv_set.get_csv_readers():
            field_names = field_names or reader.fieldnames
            for row in reader:
                for col_name in field_names:
                    col_val = row[col_name]
                    # Skip col if default set
                    if not row_def.get(col_name):
                        default_value = RowTypeAggregator.col_default(col_val)
                        if default_value is not None:
                            # If value set in col
                            row_def[col_name] = default_value
                            if len(reader.fieldnames) == len(row_def):
                                # If all defaults is set
                                return row_def

    @staticmethod
    def str_to_decimal(val):
        return val.replace('$', '').replace(',', '').replace(' ', '').replace('%', '')

    @staticmethod
    def increment_row_by_row(row, row_def):
        for col_name, col_val in row.items():
            # if col_name not in row_def.keys():
            #     continue  # If this col not specified
            if col_name in ADDITIONAL_HEADERS:
                continue
            _type = type(row_def[col_name])
            if _type in (str, None):
                continue
            if col_val in CSV_NULL_VALUES:
                col_val = '0'
            if _type is Decimal:
                col_val = col_val.replace('<$0.01', '0.01')
                col_val = RowTypeAggregator.str_to_decimal(col_val)
            try:
                col_val = _type(col_val)
            except ValueError:
                print(f'Error value <{col_val}> of column \"{col_name}\":{_type} in file : ', row_def)
                col_val = 0
            except decimal.InvalidOperation:
                print(f'Error value <{col_val}> of column \"{col_name}\":{_type} in file : ', row_def)
                col_val = 0
            except Exception as e:
                print(f'Error value <{col_val}> of column \"{col_name}\":{_type} in file : ', row_def)
                raise e
            row_def[col_name] += col_val
        return row_def


if __name__ == '__main__':
    import os

    os.chdir('../../..')
    print(os.path.abspath(os.curdir))
    csv_set = CsvSet(folder_with_csv='out/test', out_file_path='out/result/row_type.csv', picked_columns_str=" ")
    print(RowTypeAggregator.get_default_values_in_set(csv_set))
