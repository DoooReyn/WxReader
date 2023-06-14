import argparse
import os
import platform
import sys
from hashlib import sha256
from json import loads, JSONDecodeError
from os import remove, listdir, system, walk, sep
from os.path import exists, dirname, abspath, join, isfile, isdir
from shutil import rmtree
from subprocess import Popen
from zipfile import ZipFile, ZIP_DEFLATED

from PyInstaller.compat import is_win, is_darwin, is_linux

from cmm import cache, logger

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# 动态库扩展名
DYNAMIC_LIBRARY_EXT = ".dll" if is_win else ".so"

# 可执行文件扩展名
EXE_EXT = ".exe" if is_win else (".app" if is_darwin else "")

# 冗余资源
RES_REDUNDANCIES = [
    "cefpython3/",
    "locales/",
    "PySide6/translations/",
    "PySide6/plugins/generic/"
    "PySide6/plugins/multimedia/"
    "devtools_resources.pak",
    "PySide6/plugins/generic/qtuiotouchplugin" + DYNAMIC_LIBRARY_EXT,
    "PySide6/plugins/multimedia/ffmpegmediaplugin" + DYNAMIC_LIBRARY_EXT,
    "PySide6/plugins/multimedia/windowsmediaplugin" + DYNAMIC_LIBRARY_EXT,
    "PySide6/Qt6Pdf" + DYNAMIC_LIBRARY_EXT,
    "PySide6/Qt6Qml" + DYNAMIC_LIBRARY_EXT,
    "PySide6/Qt6QmlModels" + DYNAMIC_LIBRARY_EXT,
    "PySide6/Qt6Quick" + DYNAMIC_LIBRARY_EXT,
]

# 保留资源
RES_RESERVES = ["zh-CN.pak"]

# cefpython.pyd
py_ver = "".join(map(str, sys.version_info[:2]))
cef_ver = f"cefpython_py{py_ver}.pyd"
RES_RESERVES.append(cef_ver)


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------


def checkPlatform():
    support = is_win or is_darwin or is_linux
    if support is False:
        quitCLI(f"打包程序不支持 {platform.system()}！")


def checkCommandArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--debug", action="store_true", help="开启调试模式")
    parser.add_argument("-U", "--upx", action="store_true", help="使用 UPX 压缩包体")
    parser.add_argument("-C", "--disable-cache", action="store_true", help="不使用缓存")
    parser.add_argument("-V", "--version", type=str, help="设置软件版本号")
    args = parser.parse_args()
    cache.setDebug(True if args.debug else False)
    cache.setUpx(True if args.upx else False)
    cache.setVersion(checkVersion(args.version))
    cache.setDisableCache(True if args.disable_cache else False)
    logger.info(f'调试模式: {"是" if cache.debug else "否"}')
    logger.info(f'禁用缓存: {"是" if cache.disable_cache else "否"}')
    logger.info(f'UPX压缩: {"是" if cache.upx else "否"}')
    logger.info(f'软件版本: {cache.display_version}')


def rmdir(fdir):
    """安全删除目录"""
    if exists(fdir):
        logger.info(f"清理缓存目录 {fdir}")
        rmtree(fdir)


def quitCLI(tip: str):
    sys.exit(tip)


def checkVersion(version: str):
    """检查版本号"""
    if version is None:
        quitCLI("必须传入版本号！")
    
    sections = version.split('.')
    if len(sections) != 4:
        quitCLI('版本号格式错误！请遵循如下格式: a.b.c.d')
    
    versions = []
    for sec in sections:
        try:
            versions.append(str(int(sec)))
        except ValueError:
            quitCLI('版本号格式错误！每个部分只允许使用数字！')
    
    return versions


def readProjectConfiguration():
    try:
        with open('./package.json', encoding='utf-8') as f:
            cache.setManifest(loads(f.read()))
    except JSONDecodeError:
        quitCLI('项目配置读取失败，请检查配置是否有误！')
    logger.info('项目配置已读取！')


def generateBundleConfiguration(config, encoding):
    """生成打包配置"""
    with open(f'./template/{config}', 'r', encoding=encoding) as reader:
        content = reader.read()
        for key, value in cache.manifest.items():
            content = content.replace("#{%s}" % key, value, -1)
        with open(f'./{config}', 'w', encoding=encoding) as writer:
            writer.write(content)
        logger.info(f'打包配置 {config} 已生成！')


def generateExecutableProgram():
    """生成可执行程序"""
    
    # 运行 pyinstaller
    command = ["pyinstaller", "pyinstaller.spec"]
    if cache.upx:
        command.append("--upx-dir=./upx")
    if cache.disable_cache:
        command.append("--clean")
    sub = Popen(command, env=cache.env)
    sub.communicate()
    rcode = sub.returncode
    if rcode != 0:
        if cache.disable_cache:
            rmdir("build/")
            rmdir("dist/")
        quitCLI(f"Error: PyInstaller 任务执行失败, code={rcode}")
    
    # 删除冗余文件
    removeRedundancies()
    
    # 校验程序
    curdir = dirname(abspath(__file__))
    cefapp_dir = join(curdir, "dist", cache.manifest.get('app_name'))
    executable = join(cefapp_dir, cache.manifest.get('app_name') + EXE_EXT)
    if not exists(executable):
        quitCLI(f"Error: PyInstaller failed, main executable is missing: {executable}")
    
    logger.info(f"程序已生成 {executable}!")


def removeFile(filepath):
    """删除冗余文件"""
    remove(filepath)
    logger.info(f'清理冗余资源: {filepath}')


def removeRedundancies():
    """删除所有冗余文件"""
    curdir = dirname(abspath(__file__))
    cefapp_dir = join(curdir, "dist", cache.manifest.get('app_name'))
    for entry in RES_REDUNDANCIES:
        filepath = join(cefapp_dir, entry)
        if isfile(filepath):
            removeFile(filepath)
        elif isdir(filepath):
            for sub_entry in listdir(filepath):
                if sub_entry not in RES_RESERVES:
                    removeFile(join(filepath, sub_entry))


def testExecutableProgram():
    """测试可执行程序"""
    curdir = dirname(abspath(__file__))
    cefapp_dir = join(curdir, "dist", cache.manifest.get('app_name'))
    executable = join(cefapp_dir, cache.manifest.get('app_name') + EXE_EXT)
    if is_win:
        if cache.debug:
            # 测试程序
            system("start cmd /k \"%s\"" % executable)
        else:
            # 打开可执行程序目录
            system("%s/explorer.exe /n,/e,%s" % (cache.getEnv("SYSTEMROOT"), cefapp_dir))


# noinspection PyTypeChecker
def packExecutableProgram():
    """生成便携版和安装包"""
    curdir = dirname(abspath(__file__))
    app_name = cache.manifest.get('app_name')
    cefapp_dir = join(curdir, "dist", app_name)
    portable = f'./{app_name}_v{cache.display_version}_Portable.zip'
    logger.info(f'正在制作便携版！ > {portable}')
    z = ZipFile(portable, 'w', ZIP_DEFLATED)
    for dir_path, dirs, files in walk(cefapp_dir):
        fpath = dir_path.replace(cefapp_dir, '')
        fpath = fpath and (fpath + sep) or ''
        for filename in files:
            z.write(join(dir_path, filename), fpath + filename)
    z.close()
    logger.info(f'便携版已生成！ > {portable}')
    generateSha256(portable)
    
    # 生成安装包
    generateInstaller()
    if is_win:
        installer = f'./{app_name}_v{cache.display_version}_Installer.exe'
        logger.info(f'安装包已生成！ > {installer}')
        generateSha256(installer)


def generateInstaller():
    """生成安装包"""
    if cache.debug is False:
        system("makensis package.nsi")


def generateSha256(filepath):
    """生成文件的SHA256"""
    if not exists(filepath):
        return
    
    block_size = 65536
    h = sha256()
    with open(filepath, 'rb') as fh:
        while True:
            file_buffer = fh.read(block_size)
            if len(file_buffer) == 0:
                break
            h.update(file_buffer)
    logger.info(f"{filepath} <SHA256: {h.hexdigest()}>")


def main():
    # 检查支持平台
    checkPlatform()
    
    # 检查命令行参数
    checkCommandArgs()
    
    # 读取项目配置
    readProjectConfiguration()
    
    # 根据模板生成 pyinstaller.spec / package.nsi
    generateBundleConfiguration('pyinstaller.spec', 'utf-8')
    generateBundleConfiguration('package.nsi', 'utf-8-sig')
    
    # 更新项目配置
    cache.saveManifest()
    
    # 清空缓存
    if cache.disable_cache:
        rmdir("build/")
        rmdir("dist/")
    
    # 生成可执行程序（同步）
    generateExecutableProgram()
    
    # 校验可执行程序
    testExecutableProgram()
    
    # 生成便携版和安装包
    packExecutableProgram()
    
    # 删除配置
    os.remove('pyinstaller.spec')
    os.remove('package.nsi')
    
    # 打包全部完成
    logger.info('恭喜！打包完成！')


if __name__ == '__main__':
    main()
