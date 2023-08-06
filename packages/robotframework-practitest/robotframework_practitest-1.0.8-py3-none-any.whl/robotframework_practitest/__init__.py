import os
from . import utils
from .listener import PractiTestReportService
from robotframework_practitest.version import VERSION


__author__ = 'Dmitry Oguz'
__author_email__ = 'doguz2509@gmail.com'
__version__ = VERSION
__url__ = r'https://github.com/doguz2509/robotframework_practitest'
__package_name__ = __name__


__all__ = [
    '__author__',
    '__author_email__',
    '__version__',
    '__url__',
    '__package_name__',
    'utils',
    'PractiTestReportService'
]

