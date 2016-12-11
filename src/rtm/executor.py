#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import time
import signal
from threading import Thread, Event

from rtm.logger import logger

__author__ = 'David Qian'

"""
Created on 12/08/2016
@author: David Qian

"""


class ExecutorThread(Thread):
    """Executor thread, communicate with the real runner

    """

    def __init__(self, cmd, workdir):
        super(ExecutorThread, self).__init__()
        self._runner = CmdRunner(cmd, workdir)
        self._event = Event()
        self._terminate = False

    def run(self):
        logger.info('start executor thread')
        while not self._terminate:
            self._runner.start()
            self._wait_and_clear_event()
            if self._terminate:
                break

            self._runner.terminate()

        self._runner.terminate()
        logger.info('terminate executor thread')

    def _wait_and_clear_event(self):
        while True:
            if self._event.is_set() or not self._runner.is_alive():
                logger.info('Need restart runner')
                break

            time.sleep(5)

        self._event.clear()

    def restart_runner(self):
        self._event.set()

    def terminate(self):
        self._terminate = True
        self._event.set()


class CmdRunner(object):
    """Runner, fork subprocess to execute the command

    """

    def __init__(self, cmd, workdir):
        self.cmd = cmd.split()
        self.workdir = workdir
        self.p = None

    def start(self):
        logger.info('start runner')
        self.p = subprocess.Popen(self.cmd, cwd=self.workdir)
        logger.info('Runner pid is %d' % self.p.pid)

    def terminate(self):
        if self.p:
            logger.info('terminate runner')
            try:
                self.p.terminate()
            except OSError:
                pass
            self.p.wait()
            self.p = None

    def is_alive(self):
        if not self.p:
            return False

        if self.p.poll() is None:
            return True

        return False



class LoopMaster(object):
    """Loop restart executer
    """

    def __init__(self, cmd, restart_time, workdir=None):
        # hour of the restart time, e.g. 0~23
        self.restart_time = int(restart_time)
        self._executor = ExecutorThread(cmd, workdir)
        self._signals = [
            signal.SIGINT,
            signal.SIGTERM,
        ]
        self._setup_signal_handler()

    def run(self):
        logger.info('start master')
        self._executor.start()

        while True:
            time.sleep(3600)
            cur_time = time.localtime(time.time())
            if self.restart_time <= cur_time.tm_hour < self.restart_time+1:
                self._executor.restart_runner()

    def terminate(self, signum, frame):
        logger.warn('receive signal(%d)' % signum)
        self._executor.terminate()
        self._executor.join()
        raise SystemExit()

    def _setup_signal_handler(self):
        for signum in self._signals:
            signal.signal(signum, self.terminate)


if __name__ == '__main__':
    e = LoopMaster('python -m SimpleHTTPServer', 21)
    e.run()


