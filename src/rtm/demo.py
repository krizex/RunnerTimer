#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rtm.executor import LoopMaster

__author__ = 'David Qian'

"""
Created on 02/15/2017
@author: David Qian

"""

if __name__ == '__main__':
    cmd = './test/test.sh'
    restart_time = '0'
    workdir = None

    master = LoopMaster(cmd, restart_time, workdir)
    master.run()
