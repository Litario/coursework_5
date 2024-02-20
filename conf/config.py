from configparser import ConfigParser

from common_functions.funcs_1 import colprint
from sup.adress import DATABASE_INI_PATH


def config(filename=DATABASE_INI_PATH, section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))

    return db

## _______________________________________ TestCase 1

# c = config()
# print(c)
# colprint(c)
