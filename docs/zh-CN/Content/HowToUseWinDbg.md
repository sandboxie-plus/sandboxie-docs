# 如何使用 WinDbg

在某些少见情况下，运行在沙盘监管下的程序可能无法正常工作，并且不会提供任何有关故障原因的提示。在这些情况下，微软免费的 [Windows 调试工具](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools) 可以帮助更好地分析问题，甚至定位问题的根源。

* * *

下载并安装最新版的 [Windows SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk)（包括 32 位和 64 位）。

如果你只需要 Windows 调试工具，你可以单独安装调试工具组件。

该软件包默认安装到 _C:\Program Files (x86)\Windows Kits\10\Debuggers_。

安装完成后会在 Windows 开始菜单中创建一个名为 _Windows Kits_ 的应用程序组，该应用组中包含 _WinDbg_ 程序。

即使在 64 位 Windows 上，通常也建议优先使用 32 位调试器。只有在调试 64 位程序时才需要使用 64 位调试器。更多信息请参见 [选择 32 位还是 64 位调试工具](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/choosing-a-32-bit-or-64-bit-debugger-package)。

* * *

**方案 1：从调试器启动程序**

通过沙盘使用沙盘开始菜单运行调试器。

* [沙盘控制](SandboxieControl.md) > [沙箱菜单](SandboxMenu.md) > 从开始菜单运行

* Sandboxie Plus 窗口 > 右键点击你的沙箱 > 运行 > 从开始菜单运行

然后在沙箱开始菜单中，找到并启动 _Windows Kits_ 组下的 _WinDbg_ 程序。

WinDbg 调试器将启动并打开其主窗口。

在调试器中，执行 文件菜单 > 打开可执行文件命令。然后浏览并选择你希望在调试器中运行的程序的 EXE 文件。

例如，浏览并选择 _C:\Windows\System32\notepad.exe_

调试器将打开一个命令窗口，用于控制（或调试）新的程序。

使用 调试菜单 > 运行命令 来启动程序的执行（你也可以按 F5）。此时调试器状态栏会变为 *BUSY*。请继续阅读下方标题为 **最后一步** 的部分。

* * *

**方案 2：附加调试器到正在运行的程序**

在这种情况下，你已经通过沙盘启动了程序，并且程序正在运行。

从 Windows 开始菜单启动调试器：找到并启动 _Windows Kits_ 组下的 _WinDbg_ 程序。

WinDbg 调试器将启动并打开其主窗口。

在调试器中，执行 文件菜单 > 附加到进程 命令（你也可以按 F6）。然后找到并确认要附加调试器的程序的 EXE 文件。

调试器将打开一个命令窗口，用于控制（或调试）被附加的程序。

如果你是在程序已经出现问题之后附加的调试器，请继续阅读下方标题为 **最后一步** 的部分。

否则，使用 调试菜单 > 运行命令 继续程序的执行（你也可以按 F5）。此时调试器状态栏会变为 *BUSY*。请继续阅读下方标题为 **最后一步** 的部分。

* * *

**最后一步**

本节假设所涉程序已经出现了问题：

*   如果程序陷入死循环，则现在应该已经卡住
*   如果程序崩溃，则现在应该已经崩溃

如果问题现象尚未出现，你现在应促使程序出现故障。

一旦程序出现问题，切换回 WinDbg 调试器命令窗口。如果调试器状态栏仍显示 *BUSY*，请使用  调试菜单 > 中断命令 停止程序（你也可以按 Ctrl+Break）。

当调试器状态栏不再显示 *BUSY*，请依次输入以下命令，每次输入一个命令后按回车：

```
    .sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
    .reload
    ~* k 99
```

第三条命令会导致调试器生成一些输出。命令执行完成后，请复制整个调试日志。使用  编辑菜单 > 将窗口文本复制到剪贴板 命令将整个调试日志复制到剪贴板，然后返回到沙盘支持页面，把该调试日志粘贴到你的评论中。

感谢配合。