# 文件迁移设置

[沙盒控制](SandboxieControl.md) > [沙箱设置](SandboxSettings.md) > 文件迁移：

![](../Media/FileMigrationSettings.png)

在沙箱中的程序尝试修改计算机中已存在的文件之前，沙盒会首先将该文件复制到沙箱内。然而，复制非常大的文件将耗费较长时间。因此，沙盒只会复制那些小于设定最大大小的文件。超过该大小的文件在沙箱内将被视为只读，任何尝试修改它们的操作都会导致弹出消息 [SBIE2102](SBIE2102.md)

您可以在此设置页面中指定最大文件大小阈值，以及是否希望在尝试修改超过该最大大小的文件时，弹出消息 [SBIE2102](SBIE2102.md)

相关的 [沙盒配置文件](SandboxieIni.md) 设置项：[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)