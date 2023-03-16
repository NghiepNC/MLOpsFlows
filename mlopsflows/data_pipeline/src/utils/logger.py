#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   logger.py
@Time    :   2023/03/15 13:29:34
@Author  :   Duy Nam
@Version :   0.1
@Contact :   nam.nd.00@gmail.com
@Desc    :   MLOps Flows
'''

import logging
import sys
from typing import Any
import os
from pathlib import Path

BASE_DIR = os.path.dirname(Path(__file__).parent.parent)
LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


class Logging:
    """The Logging instance"""
    _LOG_FILE = os.path.join(LOG_DIR, 'info.log')
    _LOG_LEVEL = logging.DEBUG
    _LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def __init__(self, level: Any = None):
        """Initialize logging

        Args:
            level (logging): the logging level
        """
        self.level = level if level is not None else Logging._LOG_LEVEL

    def get_logger(self):
        """Get the logger
        """
        logger = logging.getLogger(__name__)
        logger_format = logging.Formatter(Logging._LOG_FORMAT)
        stream_handler = logging.StreamHandler(sys.stdout)
        output_logger = logging.FileHandler(Logging._LOG_FILE)

        stream_handler.setFormatter(logger_format)
        output_logger.setFormatter(logger_format)

        logger.addHandler(stream_handler)
        logger.addHandler(output_logger)
        logger.setLevel(self.level)

        return logger

    def __str__(self) -> str:
        return "Logging instance"
