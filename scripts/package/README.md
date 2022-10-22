# 打包

## 整理可以删除的文件

- devtools_resources.pak
- locales/*
  - 保留 zh-CN.pak
- cefpython3/*.dll
- PySide6/
    - translations/*
    - Qt6Qml.dll
    - Qt6QmlModels.dll
    - Qt6Quick.dll

## 制作便携版

存在配置文件的情况下，直接运行：`pyinstaller WxReader.spec`；

否则，使用如下命令：

```shell
cd ${project_dir}
pyinstaller -w -i ./resources/icon/app.ico --paths ./app --clean -n WxReader -d imports -y --noconfirm ./app/Application.py
```

可以使用 [UPX](https://upx.github.io/) 进一步压缩，只需要在上面命令后面添加 `--upx-dir path/to/upx`。

## 制作安装包

- 利用 PyInstaller 制作便携版
- 安装 NSIS
- 将 NSIS 安装路径添加到环境变量中
- 运行命令：`makensis package.nsi`，或者直接双击运行 `package.bat`
