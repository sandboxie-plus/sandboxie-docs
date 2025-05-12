# 程序视图

[沙盘控制面板](SandboxieControl.md) > [视图菜单](ViewMenu.md) > [程序](ViewMenu.md#programs)

![](../Media/MainWindow.png)

_程序视图_是[沙盘控制面板](SandboxieControl.md)中的默认视图模式。在此处按沙箱名称分组显示每个沙箱中运行的程序。该列表显示三列：

*   _程序名称_列显示程序的可执行文件名称。例如，图中显示的是 _iexplore.exe_，它是 Internet Explorer 的可执行名称。
    *   对于描述沙箱的行，此列显示沙箱的名称。

*   _PID_ 列显示程序的进程 ID。此数字与 Windows 任务管理器的“进程”选项卡中显示的数字相同。（按 Ctrl+Shift+Esc 键盘快捷键或 Ctrl+Alt+Del 会显示 Windows 任务管理器，后者会进入 Windows 登录屏幕。）
    *   对于描述沙箱的行，如果沙箱中有任何程序正在运行，此列将显示 _Active_。

*   _窗口标题_列显示与程序主窗口关联的标题。

使用每个 _Active_ 沙箱行开头的小“+”或“-”图标来展开或折叠沙箱中程序的显示。

**右键菜单**

_程序视图_为沙箱和程序提供右键菜单。要显示某行中项目（沙箱或程序）的右键菜单，请执行以下操作之一：

*   在该行的任意位置点击鼠标右键。

*   使用鼠标或键盘选择（高亮显示）该行，然后按 Shift+F10。

*   使用鼠标或键盘选择（高亮显示）该行，然后使用[视图菜单 -> 右键菜单](ViewMenu.md#context-menu)命令。

对于沙箱行，显示的右键菜单与[沙箱菜单 -> 沙箱子菜单](SandboxMenu.md#sandbox-sub-menu)相同。有关完整说明，请参阅该部分。

对于程序行，右键菜单提供以下命令：

*   _终止程序_命令终止该程序。

*   _程序设置_命令显示该程序的[程序设置](ProgramSettings.md)窗口。

*   _资源访问_命令显示[沙箱设置 > 资源访问](ResourceAccessSettings.md)组的设置页面，其中程序名称会预先选择在程序名称过滤器（_The list above applies to_ 过滤器）中。

* * *

转到[沙盘控制面板](SandboxieControl.md)、[文件和文件夹视图](FilesAndFoldersView.md)、[帮助主题](HelpTopics.md)。
