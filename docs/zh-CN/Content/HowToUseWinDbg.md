# 如何使用 WinDbg

在某些极少数情况下，在沙盘中运行的程序可能会无法正常工作，而且没有任何错误提示或线索。这时，微软免费的 [Windows 调试工具](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools) 可以帮助你进一步分析问题，甚至找出根本原因。

* * *

请下载并安装最新版的 [_Windows SDK_](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk)（包括 32 位和 64 位版本）。

如果你只需要 _调试工具_，也可以只安装调试组件（Debugging Tools）。

安装包默认安装在路径：
```
C:\Program Files (x86)\Windows Kits\10\Debuggers
```

它会在开始菜单中创建一个名为 _Windows Kits_ 的应用组，组中包含名为 _WinDbg_ 的调试器程序。

一般建议使用 32 位调试器，即便你的系统是 64 位。只有在调试 64 位程序时才需要使用 64 位调试器。详细说明可参考：[如何选择 32 位或 64 位调试器工具包](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/choosing-a-32-bit-or-64-bit-debugger-package)。

* * *

**场景一：从调试器中启动程序**

使用沙盘启动调试器：

* 打开 [沙盘控制面板](SandboxieControl.md) > [沙箱菜单](SandboxMenu.md) > 从开始菜单运行

* 或在 Sandboxie Plus 窗口中右键你的沙箱 > 运行 > 从开始菜单运行

然后，在沙箱开始菜单中找到 _Windows Kits_ 组并运行 _WinDbg_。

WinDbg 启动后会显示主窗口。

在调试器中点击“文件”菜单 > 打开可执行文件，然后选择你想要调试的程序的 EXE 文件。

例如，你可以选择：
```
C:\Windows\System32\notepad.exe
```

调试器会打开一个命令窗口用于控制（或调试）你启动的程序。

使用“调试”菜单 > 运行 命令（或按下 F5）开始执行程序。此时调试器的状态行将变为 *BUSY（忙）*。接下来请阅读下方的 **最后一步**。

* * *

**场景二：附加到已运行的程序**

在这种情况下，你已经通过沙盘启动了目标程序，并且它正在运行中。

正常启动 WinDbg（无需通过沙盘）——在开始菜单中找到 _Windows Kits_ 组下的 _WinDbg_ 并运行它。

WinDbg 启动后会显示主窗口。

在调试器中点击“文件”菜单 > 附加到进程（或按下 F6），然后选择你要调试的目标程序（EXE 文件）。

调试器会打开一个命令窗口用于控制该程序。

如果你是在程序出现问题**之后**才附加的调试器，请继续阅读下方的 **最后一步**。

如果程序还没有出问题，使用“调试”菜单 > 运行（或按 F5）继续程序执行。调试器状态行会变为 *BUSY*。然后继续阅读 **最后一步**。

* * *

**最后一步**

本节假设程序已出现问题：

* 如果程序卡住了，现在它应该已经卡住；
* 如果程序崩溃了，现在它应该已经崩溃。

如果问题尚未出现，你现在可以让程序触发错误。

一旦程序表现出问题，切换回 WinDbg 的命令窗口。如果状态栏仍显示 *BUSY*，请点击“调试”菜单 > 中断（或按下 Ctrl+Break）暂停程序。

当状态不再是 *BUSY*，依次输入以下命令，每行一条，输入后按 Enter：

```
.sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
.reload
~* k 99
```

第三条命令将输出一段调试信息。命令完成后，请复制全部日志：点击“编辑”菜单 > 复制窗口文本到剪贴板。
然后回到沙盘支持页面，在评论中粘贴这段日志。

非常感谢你的配合！
