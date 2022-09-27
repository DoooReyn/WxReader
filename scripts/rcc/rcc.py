# -*- coding: utf-8 -*-

"""
@File    : rcc.py
@Date    : 2022/9/27 11:47
@Author  : DoooReyn<jl88744653@gmail.com>
@Desc    : qrc资源文件生成及映射工具
  - 输出文件：
    - ./resources.qrc
    - {project_dir}/app/conf/resources.py
    - {project_dir}/app/conf/res_map.py
"""

from os import listdir, sep, walk
from os.path import basename, dirname, isdir, isfile, join, relpath, splitext
from subprocess import Popen


class Config:
    """
    配置

    - 规范和约定
        - 资源名称分隔符使用下划线，例如： icon_app.ico, icon_help.svg
        - 资源前缀只会采用一级目录名称，后续将全部展平到一级目录下
    """

    # 当前目录
    PROGRAM_AT = dirname(__file__)

    # 资源目录
    RESOURCES_AT = join(PROGRAM_AT, '..', '..', 'resources')

    # qrc文件
    QRC_RAW_AT = join(PROGRAM_AT, 'resources.qrc')
    QRC_PY_AT = join(PROGRAM_AT, '..', '..', 'app', 'conf', 'resources.py')

    # 资源映射文件
    RES_MAP_AT = join(PROGRAM_AT, '..', '..', 'app', 'conf', 'res_map.py')

    # qrc 转换

    # 文件编码
    ENCODING = 'utf-8'


class Qrc:
    """ qrc文件生成及映射工具 """

    def __init__(self):
        self._lines = []
        self._map = []

    def _append_line(self, line: str):
        self._lines.append(line)

    def open(self):
        self._append_line('<!DOCTYPE RCC>')
        self._append_line('<RCC version="1.0">')
        self._map.append('class ResMap:')

    def open_prefix(self, prefix: str = None):
        if prefix is not None:
            self._append_line('    <qresource prefix="%s">' % prefix)
        else:
            self._append_line('    <qresource>')

    def append_file(self, prefix: str, file_path: str):
        file_alias = splitext(basename(file_path))[0].replace('-', '_', -1)
        self._append_line('        <file alias="%s">%s</file>' % (file_alias, file_path))
        if prefix == '':
            self._map.append('    %s = ":%s"' % (file_alias, '/'.join([file_alias])))
        else:
            self._map.append('    %s_%s = ":%s"' % (prefix, file_alias, '/'.join([prefix, file_alias])))

    def close_prefix(self):
        self._append_line('    </qresource>')

    def close(self):
        self._append_line('</RCC>')
        self.qrc()
        self.map()

    def qrc(self):
        self.save_file(Config.QRC_RAW_AT, '\n'.join(self._lines) + '\n')

    def map(self):
        self.save_file(Config.RES_MAP_AT, '\n'.join(self._map) + '\n')

    @staticmethod
    def save_file(where: str, content: str):
        with open(where, 'w', encoding=Config.ENCODING) as sf:
            sf.write(content)

    @staticmethod
    def format_res(where: str):
        return relpath(where, Config.PROGRAM_AT).replace(sep, '/')


if __name__ == '__main__':
    root = Config.RESOURCES_AT
    rel = join('..', root)
    plain_files = []

    # 生成 qrc、资源映射 文件
    qrc = Qrc()
    qrc.open()

    for entry in listdir(root):
        file_at = join(root, entry)
        if isdir(file_at):
            # 添加二级资源
            qrc.open_prefix(entry)
            for sub, dirs, files in walk(file_at):
                for sub_entry in files:
                    qrc.append_file(entry, qrc.format_res(join(sub, sub_entry)))
            qrc.close_prefix()
        elif isfile(file_at):
            # 缓存一级资源，等待二级资源完成后再添加
            plain_files.append(file_at)

    if len(plain_files) > 0:
        # 添加一级资源
        qrc.open_prefix()
        [qrc.append_file('', qrc.format_res(p)) for p in plain_files]
        qrc.close_prefix()

    qrc.close()

    # qrc 转 py
    with open(Config.QRC_PY_AT, 'w', encoding=Config.ENCODING):
        cmd = 'pyrcc5 %s -o %s' % (Config.QRC_RAW_AT, Config.QRC_PY_AT)
        Popen(cmd, cwd=Config.PROGRAM_AT)
