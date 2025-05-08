# 文件菜单

[Sandboxie 控制](SandboxieControl.md) > 文件菜单

![](../Media/FileMenu.png)

* * *

### 终止所有程序

[Sandboxie 控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 终止所有程序

_终止所有程序_命令会立即停止所有沙盒中运行的所有程序。此命令没有关联的窗口。但是，您可能会收到关于即将终止的程序可能丢失数据的警告：

![](../Media/TerminateWarning.png)

此警告指的是，例如，任何未保存的打开文档。可以通过选择底部的复选框来禁用此警告：_将来终止进程时不询问。_

另见：[托盘图标菜单](TrayIconMenu.md)中的[终止所有程序](TrayIconMenu.md#terminate-all-programs)。

* * *

### 禁用强制程序

[Sandboxie 控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 禁用强制程序

_禁用强制程序_切换命令临时禁用或重新启用强制沙盒化。通常，任何[强制程序](ProgramStartSettings.md#forced-programs)（或任何[强制文件夹](ProgramStartSettings.md#forced-folders)中的程序）都会在 Sandboxie 的监督下自动启动。当调用禁用强制程序命令时，强制沙盒化会临时暂停。

默认情况下，强制沙盒化会暂停 10 秒。当您选择此命令时，可以在以下对话框中更改秒数：

![](../Media/DisableForcedPrograms.png)

请注意，[托盘图标菜单](TrayIconMenu.md)中的相关命令不会显示此对话框，而是使用最后指定的持续时间或默认的 10 秒。

在禁用强制程序模式生效期间：

* 系统托盘区域中的 Sandboxie 图标包含一个小红 X。
* [文件菜单](FileMenu.md)和[托盘图标菜单](TrayIconMenu.md)中的"禁用强制程序"命令旁边会出现一个复选标记。
* 如果启动任何强制程序，将发出消息 [SBIE1301](SBIE1301.md)。
* 再次选择此命令将取消该模式，恢复图标的原始外观，并恢复强制沙盒化的正常操作。

另见：[托盘图标菜单](TrayIconMenu.md)中的[禁用强制程序](TrayIconMenu.md#disable-forced-programs)。

* * *

### 以 UAC 管理员身份运行

[Sandboxie 控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 以 UAC 管理员身份运行

_以 UAC 管理员身份运行_切换命令告诉 Sandboxie 在启动任何程序之前请求提升到管理员权限。此命令仅在 Windows 上用户账户控制 (UAC) 生效且用户账户尚未提升时可用。如果此命令在菜单中可用，通常在将程序安装到沙盒之前需要启用它，建议在安装完成后禁用它。

此命令没有关联的窗口。但是，当_以 UAC 管理员身份运行_生效时，该命令会在[文件菜单](FileMenu.md)和[托盘图标菜单](TrayIconMenu.md)中显示，旁边有一个复选标记。

另见：[托盘图标菜单](TrayIconMenu.md)中的[以 UAC 管理员身份运行](TrayIconMenu.md#run-as-uac-administrator)。

* * *

### 窗口是否在沙盒中？

[Sandboxie 控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 窗口是否在沙盒中？

_窗口是否在沙盒中？_命令用于选择屏幕上显示的窗口，如果该窗口属于沙盒化程序，该命令将显示程序名称和运行它的沙盒。

![](../Media/IsWindowSandboxed.png)

要使用此命令，请在_查找工具_上点击并按住鼠标左键，即窗口内目标的图标。在不释放鼠标左键的情况下，将目标拖动到所需窗口上，当目标在所需窗口的边界内时，释放鼠标左键。

如果窗口属于沙盒化程序，Sandboxie 将显示程序名称和沙盒名称，将视图切换到[程序视图](ProgramsView.md)，并高亮显示该程序。

某些程序使用自定义图形显示其窗口，这会阻止 Sandboxie 在标题栏中显示 [#] 指示器。在这些情况下，您可以使用_窗口是否在沙盒中？_命令来确保窗口及其相关程序在沙盒中运行。

* * *

### 退出

[Sandboxie 控制](SandboxieControl.md) > [文件菜单](FileMenu.md) > 退出

_退出_命令退出 [Sandboxie 控制](SandboxieControl.md)。请注意，仅关闭窗口（或从[托盘图标菜单](TrayIconMenu.md)中选择_隐藏窗口_命令）_不会_退出 Sandboxie 控制。

即使前端应用程序 Sandboxie 控制不活动，Sandboxie 仍然处于活动状态并正确监督程序。但是，以下功能由 Sandboxie 控制提供，当前端程序未运行时将不可用：

* 自动删除沙盒
* 快速和即时恢复
* 禁用强制程序模式（当从 [Sandboxie 启动](StartCommandLine.md) 程序启动时）

如果您不希望看到系统托盘区域中的 Sandboxie 控制，请考虑配置 Windows 任务栏始终隐藏该图标，而不是退出 Sandboxie 控制。

* * *

转到 [Sandboxie 控制](SandboxieControl.md#menus)、[托盘图标菜单](TrayIconMenu.md)、[帮助主题](HelpTopics.md)。 