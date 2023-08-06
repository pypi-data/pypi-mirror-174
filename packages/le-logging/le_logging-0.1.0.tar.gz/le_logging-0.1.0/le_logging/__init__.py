import os
import sys
from enum import IntEnum
from logging import Formatter, getLogger
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Union


class Level(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class RotatingLog:
    """Create a Rotating LOG with default LogLevel INFO
    Attributes

    name: str
        Name of the logger
    level: int
        Log Level defined by logging.level.
    path: str
        Path for the LogFiles. By default, this leads to the script path
    max_size: int
        Maximum logfile size in megabytes before rotating files. By default, this is 32 MB
    max_backups: int
        Maximum amount of files that will be stored before overwriting old files. By default, this is 14.
    """

    def __init__(self,
                 name: str,
                 level: Union[int, Level] = 20,
                 path: str = os.path.dirname(sys.argv[0]),
                 max_size: int = 32,
                 max_backups=14
                 ):
        # Attributes
        self.name = name or "Log"
        self.level = level
        self.max_size = max_size * 1048576
        self.max_backups = max_backups
        self.path = f"{path}{name}.log" if path.endswith("/") else f"{path}\\{name}.log"

        # defining handler
        self.handler = RotatingFileHandler(
            self.path,
            maxBytes=self.max_size,
            backupCount=self.max_backups,
            encoding="utf-8",
            delay=False
        )

        """
        Define Log Format as:
        [%Y-%m-%d %H:%M:%S] LEVEL [Filename:Linenumber] Log message
        """
        self.handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
                      '%Y-%m-%d %H:%M:%S'))

        # final initialization!
        self._log = getLogger(__name__ or self.name)
        self._log.setLevel(self.level)
        self._log.addHandler(self.handler)

    @property
    def info(self):
        """write a logmessage with the loglevel info"""
        return self._log.info

    @property
    def warn(self):
        """write a logmessage with the loglevel warn"""
        return self._log.warning

    @property
    def error(self):
        """write a logmessage with the loglevel error"""
        return self._log.error

    @property
    def debug(self):
        """write a logmessage with the loglevel debug"""
        return self._log.debug

    @property
    def critical(self):
        """write a logmessage with the loglevel critical"""
        return self._log.critical


class TimedRotatingLog:
    """Create a timed rotating LOG with default LogLevel INFO
    Attributes

    name: str
        Name of the logger
    level: int
        Log Level defined by logging.level.
    path: str
        Path for the LogFiles. By default, this leads to the script path
    timer: int
        maximum time before rotating the logfine in minutes
    max_backups: int
        Maximum amount of files that will be stored before overwriting old files. By default, this is 14.
    """

    def __init__(self,
                 name: str,
                 level: Union[int, Level] = 20,
                 path: str = os.path.dirname(sys.argv[0]),
                 timer: int = 1440,
                 max_backups=14
                 ):
        # Attributes
        self.name = name or "Log"
        self.level = level
        self.timer = timer
        self.max_backups = max_backups
        """Define file path and name as PATH/Name-%Y-%m-%d_%H-%M.log"""
        self.path = Path(f"{path}{name}.log" if path.endswith("/") else f"{path}\\{name}.log")

        # defining handler
        self.handler = TimedRotatingFileHandler(
            filename=self.path,
            when="M",
            interval=timer,
            backupCount=self.max_backups,
            encoding="utf-8",
            delay=False
        )

        """
        Define Log Format as:
        [%Y-%m-%d %H:%M:%S] LEVEL [Filename:Linenumber] Log message
        """
        self.handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
                      '%Y-%m-%d %H:%M:%S'))
        self.handler.suffix = "%Y-%m-%d_%H-%M.log"

        # final initialization!
        self._log = getLogger(__name__ or self.name)
        self._log.setLevel(self.level)
        self._log.addHandler(self.handler)

    @property
    def info(self):
        """write a logmessage with the loglevel info"""
        return self._log.info

    @property
    def warn(self):
        """write a logmessage with the loglevel warn"""
        return self._log.warning

    @property
    def error(self):
        """write a logmessage with the loglevel error"""
        return self._log.error

    @property
    def debug(self):
        """write a logmessage with the loglevel debug"""
        return self._log.debug

    @property
    def critical(self):
        """write a logmessage with the loglevel critical"""
        return self._log.critical
