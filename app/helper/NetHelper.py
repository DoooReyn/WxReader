# -*- coding: utf-8 -*-

"""
@File    : NetHelper.py
@Time    : 2022/10/10 21:48
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 网络辅助工具
"""
from urllib.request import urlopen
import re

from helper.Signals import Signals
from helper.ThreadRunner import ThreadRunner


class NetHelper:
    """网络辅助工具"""

    @staticmethod
    def httpGet(api: str):
        if not re.match(r'^https?:/{2}\w.+$', api):
            Signals().finished_api_done.emit(False)
            return

        def runner():
            try:
                with urlopen(api):
                    Signals().finished_api_done.emit(True)
            except Exception as e:
                print(e)
                Signals().finished_api_done.emit(False)
            finally:
                ThreadRunner().stop(tid)
        tid = ThreadRunner().start(runner, 30)
