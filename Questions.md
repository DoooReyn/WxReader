# 记录开发中遇到的一些问题

- **无法解析的模块**
    - 描述：在 Pycharm 下，`import` 进来的模块显示 unresolved 错误
    - 原因：没有在 Pycharm 下设置代码目录
    - 方案：将 app 目录设置为 `Sources Root` 即可
    - 操作：右键 app 目录，在弹出菜单里选择 **Mark Directory as > Sources Root**

- **无法加载文件 Scripts\Activate.ps1，因为在此系统上禁止运行脚本的问题**
    - 描述：使用 venv，在终端激活虚拟环境时报错
    - 原因：组策略限制
    - 方案：解除限制即可
    - 操作：
        - 使用管理员权限打开 PowerShell
        - `Set-ExecutionPolicy RemoteSigned`

- **No Modules named "PyQt5.QtWebEngineWidgets"**
    - 描述：找不到 `QtWebEngineWidgets` 模块
    - 原因：`QtWebEngineWidgets` 独立于 `PyQt5` 核心包之外，需要另外安装
    - 方案：单独安装 `QtWebEngineWidgets`
    - 操作：`pip install pyqtwebengine`