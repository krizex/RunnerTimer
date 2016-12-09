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

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(thread)d - %(levelname)s - %(message)s")

# create console handler and set level to debug
ch = logging.StreamHandler()

fh = logging.FileHandler('rtm.log')

for h in (ch, fh):
    h.setLevel(logging.DEBUG)
    h.setFormatter(formatter)
    logger.addHandler(h)

