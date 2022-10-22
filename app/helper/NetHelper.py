# -*- coding: utf-8 -*-

"""
@File    : NetHelper.py
@Time    : 2022/10/10 21:48
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : 网络辅助工具
"""
import re
from urllib.request import urlopen

from helper.Signals import gSignals
from helper.ThreadRunner import ThreadRunner


class NetHelper:
    """网络辅助工具"""

    @staticmethod
    def httpGet(api: str):
        """发送 GET 请求"""
        if not re.match(r'^https?:/{2}\w.+$', api):
            gSignals.finished_api_done.emit(False)
            return

        def runner():
            try:
                with urlopen(api):
                    gSignals.finished_api_done.emit(True)
            except Exception as e:
                print(e)
                gSignals.finished_api_done.emit(False)
            finally:
                ThreadRunner().stop(tid)

        tid = ThreadRunner().start(runner, 30)
