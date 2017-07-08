#!/usr/bin/env python3
#
# Copyright (c) 2017, Tomas Hozza
# All rights reserved.
#
# BSD 3-Clause License (see LICENSE file)

import sys
import argparse
import asyncio

from .configuration import read_configuration
from .notifier import SmtpNotifier
from .checker import PingCmdChecker

import logging
import logging.config
logger = logging.getLogger(__name__)


def configure_logging(level=logging.INFO):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': level,
                'propagate': True
            }
        }
    })


def construct_argparser():
    """

    :return:
    """
    parser = argparse.ArgumentParser(
        prog='onliner',
        description='Simple application to check if some destination is online and send notifications if it is not.'
    )
    parser.add_argument(
        '-c',
        '--config',
        default=None,
        help='Path to a configuration file to use.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        default=False,
        action='store_true',
        help='Make the output more verbose.'
    )

    return parser


def main(cli_args=None):
    arg_parser = construct_argparser()
    # parse arguments passed on CLI
    cli_config = arg_parser.parse_args(cli_args)

    if cli_config.verbose:
        configure_logging(logging.DEBUG)
    else:
        configure_logging()

    # read the configuration file
    configuration = read_configuration(cli_config.config)
    logger.debug('cli_config: %s', cli_config)
    logger.debug('configuration: %s', configuration)

    loop = asyncio.get_event_loop()

    notifier_config = configuration['SmtpNotifier']

    notifier = SmtpNotifier(
        login=notifier_config['login'],
        password=notifier_config['password'],
        server=notifier_config['server'],
        use_starttls=notifier_config['use_starttls'],
        loop=loop
    )

    checker_config = configuration['PingCmdChecker']

    checker = PingCmdChecker(
        destination=checker_config['destination']
    )

    resu


if __name__ == '__main__':
    main(sys.argv[1:])
