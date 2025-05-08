# 如何使用 WinDbg

在某些罕见情况下，在 Sandboxie 监督下运行的程序可能无法正常工作，且没有提供任何故障原因的提示。在这些情况下，Microsoft 的免费[Windows 调试工具](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools)可以帮助更好地了解问题，甚至找出问题的原因。

* * *

下载并安装最新版本的 [_Windows SDK_](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk)（32 位和 64 位版本都需要）。

如果您只需要 _Windows 调试工具_，可以将调试工具作为独立组件安装。

该软件包默认安装在 _C:\Program Files (x86)\Windows Kits\10\Debuggers_ 目录下。

该软件包在 Windows 开始菜单中创建一个名为 _Windows Kits_ 的应用程序组。该应用程序组包含 _WinDbg_ 程序。

即使在 64 位 Windows 上，您也可能应该使用 32 位调试器。只有在调试 64 位程序时才需要使用 64 位调试器。更多信息，请参阅[选择 32 位或 64 位调试工具](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/choosing-a-32-bit-or-64-bit-debugger-package)。

* * *

**场景 1：从调试器启动程序**

通过使用 Sandboxie 开始菜单在 Sandboxie 下启动调试器。

* [Sandboxie 控制器](SandboxieControl.md) > [沙盒菜单](SandboxMenu.md) > 从开始菜单运行

* Sandboxie Plus 窗口 > 右键点击您的沙盒 > 运行 > 从开始菜单运行

然后在 Sandboxie 开始菜单中导航到 _Windows Kits_ 组，找到并启动 _WinDbg_ 程序。

WinDbg 调试器应该启动并打开其主窗口。

在调试器中，调用"文件"菜单 > "打开可执行文件"命令。然后导航到并选择您想要在调试器中运行的程序的 EXE 文件。

例如，导航到并选择 _C:\Windows\System32\notepad.exe_

调试器将打开一个命令窗口，用于控制（或调试）新程序。

使用"调试"菜单 > "开始"命令来开始执行程序。（您也可以按 F5。）此时调试器状态行将变为 *BUSY*。继续阅读下面标题为**最后一步**的部分。

* * *

**场景 2：将调试器附加到正在运行的程序**

在这种情况下，您已经使用 Sandboxie 启动了程序，并且程序已经在运行。

从 Windows 开始菜单正常启动调试器：在 _Windows Kits_ 组中找到并启动 _WinDbg_ 程序。

WinDbg 调试器应该启动并打开其主窗口。

在调试器中，调用"文件"菜单 > "附加到进程"命令。（您也可以按 F6。）然后找到您想要附加调试器的程序的 EXE 文件。

调试器将打开一个命令窗口，用于控制（或调试）已附加的程序。

如果您是在程序已经出现问题后才附加到程序，那么请继续阅读下面标题为**最后一步**的部分。

否则使用"调试"菜单 > "开始"命令来继续执行程序。（您也可以按 F5。）此时调试器状态行将变为 *BUSY*。继续阅读下面标题为**最后一步**的部分。

* * *

**最后一步**

本节假设相关程序已经出现问题：

* 如果程序陷入循环，那么它应该已经卡住。
* 如果程序崩溃，那么它应该已经崩溃。

如果问题状况尚未发生，您应该现在让程序出现故障。

一旦程序出现问题，切换回 WinDbg 调试器命令窗口。如果调试器状态行仍显示 *BUSY*，使用"调试"菜单 > "中断"命令来停止程序。（您也可以按 Ctrl+Break。）

当调试器状态行不再显示 *BUSY* 时，输入以下命令。每次输入一个命令，然后按 Enter。

```
    .sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
    .reload
    ~* k 99
```

第三个命令将导致调试器产生一些输出。当命令完成时，请复制整个调试日志。使用"编辑"菜单 > "将窗口文本复制到剪贴板"命令将整个调试日志复制到剪贴板，然后返回 Sandboxie 支持并将此调试日志粘贴到您的评论中。

提前感谢您的配合。 