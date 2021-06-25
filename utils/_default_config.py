import logging
from configparser import ConfigParser, ExtendedInterpolation

DEFAULT_CONFIG = ConfigParser(interpolation=ExtendedInterpolation())

DEFAULT_CONFIG['logging'] = {
    'level': str(logging.DEBUG),
    'filename': "",
    'filemode': 'w',
    "format": logging.BASIC_FORMAT,
}

DEFAULT_CONFIG['window'] = {
    'x': '200',
    'y': '200',
    'width': '1600',
    'height': '700',
    'title': 'AeflotFront'
}
