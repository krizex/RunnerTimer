#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from rtm.executor import LoopMaster

__author__ = 'David Qian'

"""
Created on 12/09/2016
@author: David Qian

"""

if __name__ == '__main__':
    cmd = sys.argv[1]
    restart_time = sys.argv[2]
    workdir = sys.argv[3] if len(sys.argv) >=4 else None

    master = LoopMaster(cmd, restart_time, workdir)
    master.run()