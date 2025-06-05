# Encryption & Security Platform 32

## 开发指南

### 组件库

使用[Fluent Widget](https://qfluentwidgets.com/zh/)组件库。

安装指令

```bash
pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/
```

组件库使用指南：[基础输入-按钮](https://qfluentwidgets.com/zh/pages/components/button)

### 模板使用

> [!IMPORTANT]
>
> 以下内容由豆包生成。

模板位于`src/template`目录下，方便对同样输入输出功能的组件进行快速开发。

`CLImode`使用样例

```python
# 假设这是你的加密函数
def my_encode_function(file_path):
    # 实际的加密逻辑
    with open(file_path, 'r') as f:
        content = f.read()
    # 这里执行加密操作
    encrypted = content[::-1]  # 简单示例：反转字符串
    return encrypted

# 假设这是你的解密函数
def my_decode_function(file_path):
    # 实际的解密逻辑
    with open(file_path, 'r') as f:
        content = f.read()
    # 这里执行解密操作
    decrypted = content[::-1]  # 简单示例：反转字符串（对应上面的加密）
    return decrypted

# 创建CLITab实例
tab = CLITab(
    tab_name="加密/解密工具",
    algorithm_name="简单加密算法",
    encode_func=my_encode_function,
    decode_func=my_decode_function
)
```

`CLImodeInput`使用样例

```python
# 假设这是你的文本处理函数
def my_process_function(text):
    # 实际的处理逻辑
    processed_text = text.upper()  # 简单示例：将文本转为大写
    return processed_text

# 创建CLIInputTab实例
tab = CLIInputTab(
    tab_name="文本处理工具",
    algorithm_name="文本转换算法",
    process_func=my_process_function
)
```

## 打包教程

首先，确保所处安装环境已安装全部依赖库，安装`nuitka`。

使用下面指令进行打包：

```powershell
<PYHTON_PATH>/python.exe -m nuitka `
--onefile `
--show-progress `
--remove-output `
--lto=no `
--assume-yes-for-downloads `
--jobs=12 `
--output-dir=<DIR_PATH>/ESP32/src/output `
--main=<DIR_PATH>/ESP32/src/mainWindows.py `
--windows-icon-from-ico=<DIR_PATH>/ESP32/src/res/icons/favicon.ico `
--plugin-enable=pyqt5 `
--include-package=algorithms.SecureEditor `
--include-package=template `
--include-module=mod.Fluent3Icon `
--include-data-dir=<DIR_PATH>/ESP32/src/mod/font=mod/font `
--include-data-dir=<DIR_PATH>/ESP32/src/log=log `
--include-data-dir=<DIR_PATH>/ESP32/src/res/=res `
```

其中`<PYHTON_PATH>`为 Python 安装路径，`<DIR_PATH>`为 ESP32 项目根目录。

### 资源文件的添加

当需要添加资源文件时，可以使用`--include-data-dir`参数来指定资源文件的路径。注意在代码中使用绝对路径来引用这些资源文件。

例如，要引用资源文件中的图标，可以在代码中这样写：

```python
# 获取当前运行路径，无论是.py还是.exe都能适配
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR,"res", "icons", "favicon.png")
```

### 模块、包添加

当需要添加模块时，可以使用`--include-module`参数来指定模块的名称。

例如，要添加`mod.Fluent3Icon`模块，可以在打包命令中使用：

```powershell
--include-module=mod.Fluent3Icon
```

当需要添加包时，可以使用`--include-package`参数来指定包的名称。

例如，要添加`template`包，可以在打包命令中使用：

```powershell
--include-package=template
```

并在`template`包中添加`__init__.py`文件，以确保它被识别为一个包。

在`__init__.py`文件中，使用相对导入来引用包中的模块。

### 插件的添加

当需要添加插件时，可以使用`--plugin-enable`参数来启用插件。

例如，要启用`pyqt5`插件，可以在打包命令中使用：

```powershell
--plugin-enable=pyqt5
```

PyQt5 项目通常需要启用此插件，以确保 PyQt5 的功能能够正常工作。

### 无控制台窗口

如果需要打包成无控制台的应用程序，可以在打包命令中添加`--windows-disable-console`或`--windows-console-mode=disable`参数。

```powershell
--windows-console-mode=disable
```

注意关闭控制台窗口可能会导致调试信息无法输出到控制台，因此在开发阶段建议保留控制台窗口，打包时再关闭。

### 输出目录

使用`--output-dir`参数来指定输出目录。

例如，要将输出文件放在`<DIR_PATH>/ESP32/src/output`目录下，可以在打包命令中使用：

```powershell
--output-dir=<DIR_PATH>/ESP32/src/output
```
