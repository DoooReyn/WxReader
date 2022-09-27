# -*- coding: utf-8 -*-

"""
@File    : thread_runner.py
@Time    : 2022/9/27 17:22
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 线程任务
"""
from threading import Event, Thread
from time import sleep
from typing import Callable, Dict

from helper.cmm import Cmm
from helper.signals import Signals


class ThreadNotFound(Exception):
    """异常：未知的线程ID"""

    def __init__(self, tid: str):
        super(ThreadNotFound, self).__init__()
        self.tid = tid


class StatefulThread(Thread):
    """拥有状态的线程，可暂停和恢复"""

    def __init__(self, **kwargs):
        super(StatefulThread, self).__init__(**kwargs)
        self._stop_event = Event()
        self._pause_event = Event()

    def pause(self):
        self._pause_event.set()

    def resume(self):
        self._pause_event.clear()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def paused(self):
        return self._pause_event.is_set()

    def running(self):
        return (not self.stopped()) and (not self.paused())

    def start(self):
        super(StatefulThread, self).start()


@Cmm.Decorator.Singleton
class ThreadRunner:
    """线程任务"""
    def __init__(self):
        print('--- thread_runner', id(self))
        self._threads: Dict[str, StatefulThread] = dict()

    def start(self, runner: Callable, interval: float = 0.015, stop_on_error: bool = False):
        interval = max(0.015, interval)

        def on_error(err: str):
            if stop_on_error:
                Signals().logger_error.emit(err)
            else:
                if thread:
                    thread.stop()

        def _runner():
            while True:
                if thread is None or thread.stopped():
                    break
                if thread.running():
                    sleep(interval)
                    Cmm.trace(runner, on_error)

        thread = StatefulThread(target=_runner, daemon=True)
        thread.name = str(id(thread))
        thread.start()

        self._threads.setdefault(thread.name, thread)
        return thread.name

    def _call(self, tid: str, method: str, fn: Callable = None):
        thread = self._threads.get(tid)
        if thread is not None:
            m = getattr(thread, method, None)
            if m is not None:
                if fn is not None:
                    fn()
                return m()
        raise ThreadNotFound(tid)

    def pause(self, tid: str):
        self._call(tid, 'pause')

    def resume(self, tid: str):
        self._call(tid, 'resume')

    def stop(self, tid: str):
        self._call(tid, 'stop', lambda: self._threads.pop(tid))

    def paused(self, tid: str):
        return self._call(tid, 'paused')

    def running(self, tid: str):
        return self._call(tid, 'running')

    def stopped(self, tid: str):
        return self._call(tid, 'stopped')
