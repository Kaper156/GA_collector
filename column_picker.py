from collections import OrderedDict


class ColumnPicker:
    _PROMT_WELCOME_ = """
Please write needed columns-numbers in order, which you like with whitespaces between them
(ex. 1 3 2 6)
Leave it blank if you need all columns in order as is in files
    """
    _PROMT_INPUT_ = "Input numbers of columns with whitespace between:\t"
    _PROMT_BAD_INPUT_ = """Something went wrong! 
Please try again, and again, column numbers must be separated with whitespace"""
    _PROMT_BAD_INDEX_ = "Some of entered indexes not a number of column! Try again."

    def __init__(self, headers_row):
        self.specific_columns = self.ask_specific_columns(headers_row)

    def ask_specific_columns(self, headers_row):
        print(self._PROMT_WELCOME_)

        # Show columns and indexes
        for index, col in enumerate(headers_row):
            print(f"{index}\t{col}")

        # Wait user message
        while True:
            try:
                msg = input(self._PROMT_INPUT_).strip()
                # If user leave blank message
                if not msg:
                    return headers_row
                # Convert message to list of indexes
                indexes = map(int, msg.split())
            except ValueError:
                # Try again
                print(self._PROMT_BAD_INPUT_)
            else:
                # User write only numbers goto next step
                break
        # Trying to form specific columns
        headers_type = type(headers_row)  # Careful set iter
        try:
            return headers_type(map(lambda i: headers_row[i], indexes))
        except IndexError as e_ind:
            # Some of indexes not in headers
            print(self._PROMT_BAD_INDEX_)
            return self.ask_specific_columns(headers_row)

    def pick_headers(self):
        return self.specific_columns

    def pick_row_cols(self, row):
        return OrderedDict(map(lambda key: (key, row[key]), self.specific_columns))
