# 删除沙箱

[沙箱控制](SandboxieControl.md) > [沙箱菜单](SandboxMenu.md) > 删除内容

[沙箱控制](SandboxieControl.md) > [托盘图标菜单](TrayIconMenu.md) > 删除内容

![](../Media/DeleteSandbox.png)

当即将删除沙箱时，会弹出“删除沙箱”窗口。该窗口分为两个区域：

*   上部区域（约占窗口的 3/4）显示 [快速恢复](QuickRecovery.md) 的界面和控制项，其操作方式与“快速恢复”窗口相同。详细信息请参见 [快速恢复](QuickRecovery.md)。

*   下部区域会统计沙箱的大小（包括文件数、文件夹数和所占磁盘空间的字节数），并包含一个“删除沙箱”按钮，用于启动沙箱的删除操作。

当执行 [沙箱菜单 > 沙箱 > 删除内容](SandboxMenu.md#sandbox-menu) 命令（或通过 [托盘图标菜单](TrayIconMenu.md) 执行相应命令）时，会显示此窗口。

如果沙箱配置为自动删除（参见 [沙箱设置 > 删除 > 调用方式](DeleteSettings.md#invocation)），且有文件符合 [快速恢复](QuickRecovery.md) 条件时，也会显示该窗口。注意，如果没有文件符合条件，沙箱将被静默删除，不会弹出“删除沙箱”窗口。

请注意，“删除沙箱”命令会终止在沙箱中运行的所有程序，并启动删除流程。当您点击“删除沙箱”按钮后，空沙箱将立即可用于运行程序。在旧沙箱的删除过程中，Sandboxie 托盘图标会变为红色 X 图标，以指示正在删除沙箱。正常情况下，红色 X 图标不应显示超过几秒钟。

* * *

前往 [快速恢复](QuickRecovery.md)、[沙箱控制](SandboxieControl.md)、[帮助主题](HelpTopics.md)