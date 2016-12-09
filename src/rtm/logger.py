#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

__author__ = 'David Qian'

"""
Created on 12/09/2016
@author: David Qian

"""


# create logger
logger = logging.getLogger('rtm')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

