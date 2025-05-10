# 文件菜单

[沙盒控制](SandboxieControl.md) > 文件菜单

![](../Media/FileMenu.png)

* * *

### 终止所有程序

[沙盒控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 终止所有程序

“终止所有程序”命令可立即停止所有沙箱中正在运行的全部程序。此命令没有关联的窗口。但在执行前，你可能会收到提示，警告即将终止的程序可能导致相关数据丢失：

![](../Media/TerminateWarning.png)

该警告例如指的是任何未保存的打开文档。你可以通过勾选底部的“下次无需确认，直接终止进程”来禁用此警告。

另请参阅：[托盘图标菜单](TrayIconMenu.md)中的 [终止所有程序](TrayIconMenu.md#terminate-all-programs)

* * *

### 禁用强制程序

[沙盒控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 禁用强制程序

“禁用强制程序”切换命令可临时禁用或重新启用强制沙箱化。通常，所有[强制程序](ProgramStartSettings.md#forced-programs)（或位于任意[强制文件夹](ProgramStartSettings.md#forced-folders)中的程序）都会自动在沙盒的监管下启动。执行“禁用强制程序”命令时，强制沙箱化会被临时暂停。

默认情况下，强制沙箱化会暂停 10 秒。你可以在弹出的对话框中修改暂停秒数，该对话框会在你选择此命令时出现。

![](../Media/DisableForcedPrograms.png)

请注意，[托盘图标菜单](TrayIconMenu.md)中的相关命令不会显示此对话框，并会使用上一次设定的持续时间，或默认的 10 秒。

在“禁用强制程序”模式有效期间：

*   系统托盘区域的沙盒图标将带有一个小红 X
*   [文件菜单](FileMenu.md) 和 [托盘图标菜单](TrayIconMenu.md)中的“禁用强制程序”命令旁会有一个勾选标记
*   如果有强制程序启动，则会发出消息 [SBIE1301](SBIE1301.md)
*   再次选择此命令，将取消该模式，恢复图标原状，并恢复强制沙箱化的正常操作

另请参阅：[托盘图标菜单](TrayIconMenu.md)中的 [禁用强制程序](TrayIconMenu.md#disable-forced-programs)

* * *

### 以 UAC 管理员身份运行

[沙盒控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 以 UAC 管理员身份运行

“以 UAC 管理员身份运行”切换命令可使沙盒在启动任何程序前请求提升到管理员权限。该命令仅适用于启用了用户帐户控制（UAC）且当前用户账号尚未提升的 Windows。如果菜单中出现该命令，通常需要在将程序安装到沙箱前启用，安装完成后建议禁用。

此命令没有关联的窗口。然而，在启用“以 UAC 管理员身份运行”后， [文件菜单](FileMenu.md) 及 [托盘图标菜单](TrayIconMenu.md)中的该命令旁将显示勾选标记。

另请参阅：[托盘图标菜单](TrayIconMenu.md)中的 [以 UAC 管理员身份运行](TrayIconMenu.md#run-as-uac-administrator)

* * *

### 窗口处于沙箱中吗？

[沙盒控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 窗口处于沙箱中吗？

“窗口处于沙箱中吗？”命令用于选择屏幕上已显示的窗口，如果该窗口由沙箱中的程序所有，命令会显示该程序及其所在沙箱的名称。

![](../Media/IsWindowSandboxed.png)

使用方法：按住左键点击“查找工具”（窗口内的目标图标），在不松开的情况下，将目标拖到需要确认的窗口上。当目标移入所选窗口边界后，松开左键。

如果该窗口由沙箱中的程序所有，沙盒会显示其程序名称和沙箱名称，同时切换到[程序视图](ProgramsView.md)，并高亮显示该程序。

部分程序使用自定义图形方式显示窗口，导致沙盒无法在标题栏显示 [#] 指示标记。这种情况下，你可以通过“窗口处于沙箱中吗？”命令确认窗口及其相关程序是否正在沙箱中运行。

* * *

### 退出

[沙盒控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 退出

“退出”命令可关闭 [沙盒控制](SandboxieControl.md)。注意，仅关闭窗口（或在 [托盘图标菜单](TrayIconMenu.md) 中选择 “隐藏窗口”）**并不会**退出沙盒控制。

即使前端应用程序沙盒控制处于非活动状态，沙盒仍然有效并能正确监管各程序。但下列功能由沙盒控制前端提供，若其未运行则不可用：

*   自动删除沙箱
*   快速和即时恢复
*   禁用强制程序模式（通过 [Sandboxie Start](StartCommandLine.md) 程序发起时）

如你不希望在系统托盘区域看到沙盒控制，请考虑配置 Windows 任务栏始终隐藏该图标，而非完全退出沙盒控制。

* * *

前往 [沙盒控制](SandboxieControl.md#menus)、[托盘图标菜单](TrayIconMenu.md)、[帮助主题](HelpTopics.md)