
# Main unit test definitions. Mimicks python's unittest
from .krtest import *
from . import keys

import unittest

from pprint import pprint
import inspect
from .options import Config
from unittest import TestLoader, TextTestRunner
from xmlrunner import XMLTestRunner
from os import path
import logging
import json

# from selenium.webdriver.common import keys as keys


def main(pattern='test*.py', config=None, argv=None, start_directory='.', config_file=None, config_args=None,
         config_json=None):
    """
    Arguments in main should map to the cli arguments in __main__.py, so that pytonium suites can run via
    cli or python.

    :param pattern: files to match when discovering unit tests.
    :param config: Dict of config options
    :param argv:
    :param start_directory: the start directory to search in, default '.'
    :param config_file: json file to load config options from
    """
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


def resolve_config_arguments():
    config = Config()
    update_config_from_environment_variables(config)


def update_config_from_environment_variables(config: Config):
    config_environment_variables = map(lambda x: f'KR_{x.upper()}', config.DEFAULT_OPTIONS.keys())

    for env in config_environment_variables:
        value = os.environ.get(env)
        if value is not None:
            try:
                key = env.replace('KR_', '').lower()
                Config.DEFAULT_OPTIONS[key] = value
            except KeyError:
                logging.warning(f'KR_WARNING: Config option {key} tried to be set from environment variable {env} but is not a valid option. Skipping.')


def update_config_from_file(file):
    pass

def update_config_form_json(config: Config, jsn: str):
    args = json.loads(jsn)
    update_config_from_dict(args)

def update_config_from_args(config: Config, args: str):
    _args = map(lambda x: x.split(','), args.split('='))
    update_config_from_dict(dict(_args))

def update_config_from_dict(config: Config, dictionary):
    for key, value in dictionary:
        try:
            config.options[key] = value
        except KeyError:
            logging.warning(f'KR_WARNING: Config option {key} tried to be set but is not a valid option. Skipping')