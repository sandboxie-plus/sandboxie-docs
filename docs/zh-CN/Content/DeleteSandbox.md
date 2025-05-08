# 删除沙盒

[Sandboxie Control](SandboxieControl.md) > [沙盒菜单](SandboxMenu.md) > 删除内容

[Sandboxie Control](SandboxieControl.md) > [托盘图标菜单](TrayIconMenu.md) > 删除内容

![](../Media/DeleteSandbox.png)

当沙盒即将被删除时，会显示_删除沙盒_窗口。该窗口分为两个区域：

* 上半部分（约占窗口的 3/4）显示[快速恢复](QuickRecovery.md)的显示和控制，其操作方式与_快速恢复_窗口相同。有关更多信息，请参见[快速恢复](QuickRecovery.md)。

* 下半部分统计沙盒的大小（以文件、文件夹和磁盘空间字节数计），并包含_删除沙盒_按钮，用于启动沙盒的删除处理。

当调用[沙盒菜单 > 沙盒 > 删除内容](SandboxMenu.md#sandbox-menu)命令（或[托盘图标菜单](TrayIconMenu.md)中的相应命令）时，会显示此窗口。

如果沙盒配置为自动删除（参见[沙盒设置 > 删除 > 调用](DeleteSettings.md#invocation)），并且有任何文件符合[快速恢复](QuickRecovery.md)条件，也会显示此窗口。请注意，如果没有符合条件的文件，沙盒会静默删除，不会显示_删除沙盒_窗口。

请注意，_删除沙盒_命令会终止在沙盒中运行的所有程序并启动删除过程。一旦您点击_删除沙盒_按钮，空的沙盒将立即可用于运行程序。在旧沙盒进行删除处理时，Sandboxie 托盘图标会变为红色 X 图标，表示沙盒删除正在进行中。在正常操作中，红色 X 图标不应显示超过几秒钟。

* * *

转到[快速恢复](QuickRecovery.md)、[Sandboxie Control](SandboxieControl.md)、[帮助主题](HelpTopics.md)。 