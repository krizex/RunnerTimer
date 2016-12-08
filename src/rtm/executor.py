#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

__author__ = 'David Qian'

"""
Created on 12/08/2016
@author: David Qian

"""


class LoopRestart(object):
    def __init__(self, cmd, restart_time):
        self.cmd = cmd
        self.restart_time = restart_time

    def run(self):
        pid = self._run_subprocess()

        while True:
            time.sleep(3600)
            cur_time = time.localtime(time.time())
            if self.restart_time <= cur_time.tm_hour < self.restart_time+1:
                pass


    def _run_subprocess(self):
        pass

