from collections import OrderedDict


class NotInHeader(Exception):
    pass


class IncorrectPickedColumns(Exception):
    pass


_PROMT_WELCOME_ = """
Please write needed columns in order, which you like with comma between them
(ex. 0,-2,Week,from)
Leave it blank if you need all columns in order as is in files
    """
_PROMT_INPUT_ = "Input comma separated column indexes or column-names or uniq word in column-names. " \
                "Registry is unnecessary\n" \
                "(otherwise first column contain that word will be selected):\t"
_PROMT_BAD_INPUT_ = """Something went wrong! Value <%s> is not valid! 
Please try again, and again, column must be separated with comma"""
_PROMT_BAD_INDEX_ = "Some of entered indexes not a number of column! Try again."


class ColumnPicker:
    def __init__(self, headers_row, picked_columns=None):
        self.__available_headers__ = headers_row
        if picked_columns is None:
            self.ask_user(headers_row)
        else:
            try:
                self.parse_all_columns(picked_columns)
            except IncorrectPickedColumns as exc:
                print(_PROMT_BAD_INPUT_ % exc.args[0])
                self.ask_user(headers_row)

    def ask_user(self, headers_row):
        print(_PROMT_WELCOME_)

        # Show columns and indexes
        for index, col in enumerate(headers_row):
            print(f"{index}\t{col}")

        while True:
            try:
                msg = input(_PROMT_INPUT_).strip()
                self.parse_all_columns(msg)
            except NotInHeader:
                print(_PROMT_BAD_INPUT_ % msg)
                continue
            else:
                break

    def parse_column_name(self, value):
        value = value.strip()
        if value.lower() == 'w':
            value = 'week'
        # TODO add synonyms
        for col_name in self.__available_headers__:
            if value.lower() in col_name.lower():
                return col_name
        raise Exception(f"Not found equivalent for column name -\"{value}\" in {self.__available_headers__}")

    def parse_all_columns(self, columns: str):
        '''
        method of parsing user choice columns
        :param columns: string contain ',' separated names or indexes or word from names
        :return: valid list of column-names
        '''
        picked_headers = list()
        if not type(columns) is str:
            raise IncorrectPickedColumns(columns)
        columns = columns.strip()
        if len(columns) == 0:
            picked_headers = self.__available_headers__
        else:
            for col in columns.split(','):
                try:
                    col_index = int(col)
                    picked_headers.append(self.__available_headers__[col_index])
                except IndexError:
                    raise NotInHeader(f"Selected index {col} greater than headers length")
                except ValueError:
                    picked_headers.append(self.parse_column_name(col))

        self.specific_columns = picked_headers
        return picked_headers

    def pick_headers(self):
        return self.specific_columns

    def pick_row_cols(self, row):
        return OrderedDict(map(lambda key: (key, row[key]), self.specific_columns))


if __name__ == '__main__':
    header = ['Title', 'Indexes', 'Some col', 'Week', 'Date from', 'Date to']
    picked_columns = None
    # picked_columns = 1
    picked_columns = '-1,col,wEEK,0'
    c = ColumnPicker(header, picked_columns)
    print(c.pick_headers())
