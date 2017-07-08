# Copyright (c) 2017, Tomas Hozza
# All rights reserved.
#
# BSD 3-Clause License (see LICENSE file)

import os
import yaml

from typing import Dict


DEFAULT_CONFIG_NAME = 'onliner.yml'

config_preference = [
    os.path.join(os.getcwd(), DEFAULT_CONFIG_NAME),
    os.path.expanduser(os.path.join('~', DEFAULT_CONFIG_NAME)),
    os.path.join('etc', DEFAULT_CONFIG_NAME)
]


def get_config_path(cfg_path=None):
    """
    Returns path to the configuration file to be used. Unless some path is passed and it exists, this function will
    try to find configuration file in locations specified in 'config_preference' list.

    :param cfg_path: Path to configuration file to be used.
    :return: Path to an existing configuration file or None if no configuration file has been found.
    """
    if cfg_path is not None and os.path.exists(cfg_path):
        return cfg_path
    else:
        for path in config_preference:
            if os.path.exists(path):
                return path
        return None


def read_configuration(path=None) -> Dict:
    """
    Loads the configuration from specified configuration file if it exists and returns a dictionary with the
    configuration. If the specified file does not exist or if no file has been specified, it tries to find the
    configuration in several predefined locations.

    :param path: Path to configuration file to be used.
    :type path: str
    :return: Dictionary with values read from the configuration.
    :rtype: dict
    :raises RuntimeError: If no configuration file has been found (not the passed one nor in predefined locations).
    """
    cfg_path = get_config_path(path)
    if cfg_path is None:
        raise RuntimeError('No configuration file has been found.')
    with open(cfg_path) as configuration_file:
        configuration = yaml.safe_load(configuration_file)
    return configuration
