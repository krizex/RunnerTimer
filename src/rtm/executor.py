#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import time
from contextlib import contextmanager
from multiprocessing import Process

import signal

from rtm.logger import logger

__author__ = 'David Qian'

"""
Created on 12/08/2016
@author: David Qian

"""


class Executor(object):
    """Executor, communicate with the real runner

    """

    def __init__(self, cmd, workdir):
        self.cmd = cmd
        self.workdir = workdir
        self._process = None

    def terminate(self):
        if self._process:
            logger.info('terminate executer')
            self._process.terminate()
            self._process.join()
            self._process = None

    def start(self):
        if self._process:
            logger.error('executer already started')
            return

        logger.info('start executer')
        self._process = Process(target=self._start_runner)
        self._process.start()

    def _start_runner(self):
        logger.info('now check my pid')
        runner = CmdRunner(self.cmd, self.workdir)
        runner.start()


class CmdRunner(object):
    """Runner, fork subprocess to execute the command

    """

    def __init__(self, cmd, workdir):
        self.cmd = cmd.split()
        self.workdir = workdir
        self.p = None
        self._setup_signal_handler()

    def _setup_signal_handler(self):
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, self._kill_subprocess)

    def _kill_subprocess(self, signum, frame):
        self.terminate()

    def start(self):
        # signal.pause()
        logger.info('start runner')
        self.p = subprocess.Popen(self.cmd, cwd=self.workdir)
        self.p.wait()

    def terminate(self):
        if self.p:
            logger.info('terminate runner')
            self.p.terminate()


class LoopMaster(object):
    """Loop restart executer
    """

    def __init__(self, cmd, restart_time, workdir=None):
        self.restart_time = int(restart_time)
        self._executor = Executor(cmd, workdir)
        self._signals = {
            signal.SIGINT: None,
            signal.SIGTERM: None,
        }
        self._memo_signal_handler()

    def run(self):
        logger.info('start master')
        self.start_executor_with_shield_signal_handler()

        while True:
            time.sleep(5)
            cur_time = time.localtime(time.time())
            if self.restart_time <= cur_time.tm_hour < self.restart_time+1:
                self._executor.terminate()
                self.start_executor_with_shield_signal_handler()

    def terminate(self, signum, frame):
        logger.warn('Receive signal(%d)' % signum)
        self._executor.terminate()
        raise SystemExit()

    def start_executor_with_shield_signal_handler(self):
        with self._shield_signal_handler():
            self._executor.start()

    def _memo_signal_handler(self):
        for signum in self._signals.keys():
            self._signals[signum] = signal.getsignal(signum)

    def _setup_signal_handler(self):
        for signum in self._signals.keys():
            signal.signal(signum, self.terminate)

    @contextmanager
    def _shield_signal_handler(self):
        for signum, sighandler in self._signals.iteritems():
            signal.signal(signum, sighandler)

        yield

        self._setup_signal_handler()


if __name__ == '__main__':
    e = LoopMaster('./x.sh -s', 15, '/home/dqian/temp/20161209')
    e.run()


