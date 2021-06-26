import logging
from configparser import ConfigParser, ExtendedInterpolation

DEFAULT_CONFIG = ConfigParser(interpolation=ExtendedInterpolation())

DEFAULT_CONFIG['logging'] = {
    'level': str(logging.INFO),
    'filename': "",
    'filemode': 'w',
    "format": logging.BASIC_FORMAT,
}

DEFAULT_CONFIG['window'] = {
    'x': '200',
    'y': '200',
    'width': '1400',
    'height': '700',
    'title': 'AeflotFront'
}

DEFAULT_CONFIG['projections'] = {
    'points color': "",
    'points size': "0.005",
    'stroke color': "",
    'stroke width': "0.005",
    'fill color': '#FFFFFF',
    'use convex hull': 'true',
}

DEFAULT_CONFIG['axonometric'] = {
    'startup camera distance': '1.5',
    'startup camera azimuth': '20',
    'startup camera elevation': '10',
    'startup camera position': '0 0 0',
    'points': 'false',
    'points color': "1 0 0 1",
    'points radius': ".002",
    'plane': 'true',
    'model': 'true',
    'axes': 'true',
    'edges': 'true',
    'shader': '',
    'automatic center': 'true',
    'rotation method': 'quaternion',
    'plane color': "0.4 0.4 0.8 0.5",
}

DEFAULT_CONFIG['model'] = {
    'model formats': '*.obj *.stl',
    'startup model': '',
    'normalize on load': 'true',
    'plane tolerance order': '8',
}
