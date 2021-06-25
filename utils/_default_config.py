import logging
from configparser import ConfigParser, ExtendedInterpolation

DEFAULT_CONFIG = ConfigParser(interpolation=ExtendedInterpolation())

DEFAULT_CONFIG['logging'] = {
    'level': str(logging.DEBUG),
    'filename': "",
    'filemode': 'w',
    "format": logging.BASIC_FORMAT,
}
