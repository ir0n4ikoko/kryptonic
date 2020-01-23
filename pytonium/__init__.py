
from .krtest import *
from . import keys

from pprint import pprint
import inspect
from .options import Config
from unittest import TestLoader, TextTestRunner
from xmlrunner import XMLTestRunner
from os import path

# from selenium.webdriver.common import keys as keys


def main(pattern='test*.py', config=None, argv=None):
    #FIXME:
    if config is None:
        config = {}

    _CALLEE__FILE__ = inspect.getmodule(inspect.stack()[1][0]).__file__  # https://stackoverflow.com/a/13699329
    config_options = Config()
    config_options.__init__(**config)

    test_loader = TestLoader()
    runner = XMLTestRunner(output='test-reports') #FIXME conditional to switch to TextRunner IF config_options.options.get('test-runner', '') (see unlocked/test/UI/discover.py:22
    tests = test_loader.discover(f'{path.dirname(path.abspath(_CALLEE__FILE__))}/scenarios', pattern=pattern)
    runner.run(tests)

    pprint(config_options.options)

