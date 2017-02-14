#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.config
import os
from EmeraldAI.Logic.Modules import Global
from EmeraldAI.Logic.Singleton import Singleton


class Logger(object):
    logger = None

    def __init__(self, loggerName):
        logging.config.fileConfig(Global.EmeraldPath + "Config" + os.sep + "logging.config")
        self.logger = logging.getLogger(loggerName)

    def Debug(self, data):
        self.logger.debug(data)

    def Info(self, data):
        self.logger.info(data)

    def Warn(self, data):
        self.logger.warn(data)

    def Error(self, data):
        self.logger.error(data)

    def Critical(self, data):
        self.logger.critical(data)


class FileLogger(Logger):
    __metaclass__ = Singleton

    logger = None

    def __init__(self):
        logging.config.fileConfig(Global.EmeraldPath + "Config" + os.sep + "logging.config")
        self.logger = logging.getLogger("FileLogger")


class ConsoleLogger(Logger):
    __metaclass__ = Singleton

    logger = None

    def __init__(self):
        logging.config.fileConfig(Global.EmeraldPath + "Config" + os.sep + "logging.config")
        self.logger = logging.getLogger("ConsoleLogger")

class BaseLogger(Logger):
    __metaclass__ = Singleton

    logger = None

    def __init__(self):
        logging.config.fileConfig(Global.EmeraldPath + "Config" + os.sep + "logging.config")
        self.logger = logging.getLogger("root")


"""
TODO

Config:
[handler_rotateFileHandler]
class=handlers.RotatingFileHandler
level=DEBUG
formatter=simpleFormatter
args=('rotated.log', 'a', 100000, 1, 'utf8')

"""
