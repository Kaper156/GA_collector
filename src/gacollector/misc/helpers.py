import re

from gacollector.settings.constants import reFILE_DUPLICATE


def duplicate_check(filename):
    return bool(re.search(reFILE_DUPLICATE, filename)) or 'копия' in filename or 'copy' in filename
