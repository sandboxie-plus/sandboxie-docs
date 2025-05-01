# 系统托盘图标菜单

![](../Media/TrayPopupMenu.png)

要从系统托盘图标菜单调用命令，请右键单击系统通知区域（通常位于屏幕右下角）中显示的 Sandboxie 系统托盘图标。

* * *

### 隐藏窗口 / 显示窗口

当 [Sandboxie 控制](SandboxieControl.md) 的主窗口可见时，第一个命令是“隐藏窗口”。当主窗口隐藏时，该命令变为“显示窗口”。此命令用于显示或隐藏 Sandboxie 控制的主窗口。

* * *

### 沙箱子菜单

为每个定义的沙箱显示一个或多个子菜单。默认配置仅包含一个名为“DefaultBox”的沙箱，但可以使用 [沙箱菜单](SandboxMenu.md) 添加更多沙箱。每个子菜单包含以下命令：

*   “运行 Web 浏览器”命令将启动系统（默认）Web 浏览器。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 以沙箱模式运行 -> Web 浏览器 相同。<br>
    （注意：如果启动的程序不正确，请参阅 [常见问题解答](FrequentlyAskedQuestions.md#why-does-the-wrong-program-start-when-i-run-my-default-web-browser-sandboxed) 来解决此问题。）
*   “运行电子邮件阅读器”命令将启动系统（默认）电子邮件阅读器。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 以沙箱模式运行 -> 电子邮件阅读器 相同。
*   “运行任意程序”命令将显示“运行任意程序”对话框，该对话框类似于标准的 Windows“运行...”对话框。它可用于启动程序、打开文档和浏览文件夹，所有操作都在 Sandboxie 的监控下进行。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 以沙箱模式运行 -> 任意程序 相同。
*   “从开始菜单运行”命令将显示 Sandboxie 开始菜单，类似于标准的 Windows 开始菜单。它可用于启动开始菜单和桌面上显示的程序和其他快捷方式。请注意，如果有任何程序安装到了沙箱中，Sandboxie 开始菜单将包含安装过程中创建的快捷方式。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 以沙箱模式运行 -> 从开始菜单 相同。
*   “运行 Windows 资源管理器”命令将启动一个沙箱化的 Windows 资源管理器实例。它可用于浏览文件夹和启动程序，所有操作都在 Sandboxie 的监控下进行。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 以沙箱模式运行 -> Windows 资源管理器 相同。
*   “终止程序”命令将停止在沙箱中运行的所有程序。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 终止正在运行的程序 相同。
*   “快速恢复”命令将显示 [快速恢复](QuickRecovery.md) 窗口。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 快速恢复 相同。
*   “删除内容”命令将显示 [删除沙箱](DeleteSandbox.md) 窗口。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 删除内容 相同。
*   “浏览内容”命令将打开一个 _非沙箱化_ 的文件夹视图，用于查看沙箱的内容，_不在 Sandboxie 的监控之下_。如果可能，请使用 [文件和文件夹视图](FilesAndFoldersView.md) 来浏览沙箱的内容。<br>
    与 [沙箱菜单](SandboxMenu.md) -> _(沙箱)_ -> 浏览内容 相同。

* * *

### 终止所有程序

“终止所有程序”命令将停止所有沙箱中运行的所有程序。<br>
与 [文件菜单](FileMenu.md) -> 终止所有程序 相同。

另请参阅：[文件菜单](FileMenu.md) 中的 [终止所有程序](FileMenu.md#terminate-all-programs)。

* * *

### 禁用强制沙箱化程序

“禁用强制沙箱化程序”切换命令可临时禁用和重新启用强制沙箱化。请参阅 [文件菜单](FileMenu.md) 中的相关命令。请注意，与文件菜单命令不同，系统托盘图标命令不会显示对话框来更改命令的持续时间。相反，强制沙箱化将暂停上次指定的持续时间，或者默认的 10 秒。<br>
与 [文件菜单](FileMenu.md) -> 禁用强制沙箱化程序 相同。

另请参阅：[文件菜单](FileMenu.md) 中的 [禁用强制沙箱化程序](FileMenu.md#disable-forced-programs)。

* * *

### 以 UAC 管理员身份运行

“以 UAC 管理员身份运行”（图片中未显示；请参阅 [文件菜单](FileMenu.md)）切换命令告诉 Sandboxie 在启动任何程序之前请求提升到管理员权限。此命令仅在启用了用户账户控制 (UAC) 且用户账户尚未提升权限的 Windows 系统上可用。如果此命令在菜单中可用，则通常在将程序安装到沙箱之前需要启用它，并建议在安装完成后禁用它。<br>
与 [文件菜单](FileMenu.md) -> 以 UAC 管理员身份运行 相同。

另请参阅：[文件菜单](FileMenu.md) 中的 [以 UAC 管理员身份运行](FileMenu.md#run-as-uac-administrator)。

* * *

### 退出

“退出”命令将退出 [Sandboxie 控制](SandboxieControl.md)。请注意，仅关闭窗口（或选择“隐藏窗口”命令）_不会_ 退出 Sandboxie 控制。<br>
与 [文件菜单](FileMenu.md) -> 退出 相同。

* * *

转到 [Sandboxie 控制](SandboxieControl.md#menus)、[帮助主题](HelpTopics.md)。