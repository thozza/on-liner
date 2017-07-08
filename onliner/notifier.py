# Copyright (c) 2017, Tomas Hozza
# All rights reserved.
#
# BSD 3-Clause License (see LICENSE file)

import asyncio
import aiosmtplib

from email.mime.text import MIMEText

import logging
logger = logging.getLogger(__name__)

# dictionary containing all existing notifiers
available_notifiers = dict()


class MetaNotifier(type):
    """
    Meta class which will register any newly defined Notifier classes.
    """

    def __new__(mcs, name, bases, namespace):
        """
        Method creating new class and registering it to the 'available_checkers' dictionary.
        """
        cls = super(MetaNotifier, mcs).__new__(mcs, name, bases, namespace)

        if name != 'CheckerBase':
            try:
                available_notifiers[name]
            except KeyError:
                available_notifiers[name] = cls
            else:
                raise TypeError("Notifier with name '{0}' already exists!".format(name))

        return cls


class NotifierBase(object, metaclass=MetaNotifier):
    """
    Base class which does the notification
    """

    def notify(self, *args, **kwargs):
        raise NotImplementedError()


class SmtpNotifier(NotifierBase):
    """
    Notifier implementation using SMTP protocol to send email
    """

    SMTP_PORT = 587

    def __init__(self, login, password, server='smtp.gmail.com', use_starttls=True, loop=asyncio.get_event_loop()):
        self.server_address = server
        self.use_starttls = use_starttls
        self.login = login
        self.password = password
        self.loop = loop

    async def _init_connection(self):
        logger.debug('Initializing SMTP connection to %s:d', self.server_address, self.SMTP_PORT)
        if self.use_starttls:
            connection = aiosmtplib.SMTP(hostname=self.server_address, port=self.SMTP_PORT, loop=self.loop,
                                         use_tls=False)
            logger.debug('Using STARTTLS')
        else:
            connection = aiosmtplib.SMTP(hostname=self.server_address, port=self.SMTP_PORT, loop=self.loop)
            logger.debug('Using SSL/TLS')
        await connection.connect()
        if self.use_starttls:
            await connection.starttls()
        await connection.login(self.login, password=self.password)
        logger.debug('Logged in as %s', self.login)
        return connection

    async def send_message(self, from_addr, to_addr, message, subject):
        message = MIMEText(message)
        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = subject

        connection = await self._init_connection()
        await connection.send_message(message=message)
        logger.debug('Sent message. to=%s; from=%s; msg=%s; subj=%s', to_addr, from_addr, message, subject)
        self.loop.call_soon(connection.close(), connection)

    def notify(self, message):
        pass
