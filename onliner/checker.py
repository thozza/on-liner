# Copyright (c) 2017, Tomas Hozza
# All rights reserved.
#
# BSD 3-Clause License (see LICENSE file)

import asyncio
import subprocess

import logging
logger = logging.getLogger(__name__)

# dictionary containing all existing checkers
available_checkers = dict()


class MetaChecker(type):
    """
    Meta class which will register any newly created checker classes.
    """

    def __new__(mcs, name, bases, namespace):
        """
        Method creating new class and registering it to the 'available_checkers' dictionary.
        """
        cls = super(MetaChecker, mcs).__new__(mcs, name, bases, namespace)

        if name != 'CheckerBase':
            try:
                available_checkers[name]
            except KeyError:
                available_checkers[name] = cls
            else:
                raise TypeError("Checker with name '{0}' already exists!".format(name))

        return cls


class CheckerBase(object, metaclass=MetaChecker):
    """
    Base class which does the actual checking if IP or domain is online.
    """

    def __init__(self, destination: str, *args, **kwargs):
        self.destination = destination
        self._last_online = False

    @property
    def last_online(self):
        return self.last_online

    def check(self):
        raise NotImplementedError()


class PingCmdChecker(CheckerBase):
    """
    Checker implementation using ping command.
    """

    CMD = ['ping', '-c 3']

    async def check(self) -> bool:
        logger.debug('Checking availability of %s using ping', self.destination)
        process = await asyncio.create_subprocess_exec(self.CMD + list(self.destination),
                                                       stdin=subprocess.DEVNULL,
                                                       stderr=subprocess.STDOUT,
                                                       stdout=subprocess.DEVNULL)
        await process.wait()
        if process.returncode == 0:
            logger.info('Destination %s is online', self.destination)
            return True
        else:
            logger.info('Destination %s is NOT online', self.destination)
            return False
