# 文件迁移设置

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 文件迁移：

![](../Media/FileMigrationSettings.png)

在沙盒程序可以修改计算机中已存在的文件之前，Sandboxie 必须首先在沙盒中创建该文件的副本。但是，复制非常大的文件将是一个漫长的操作。因此，Sandboxie 只会复制低于特定最大大小的文件。大于此大小的文件在沙盒内将被视为只读，任何修改它们的尝试都将导致消息 [SBIE2102](SBIE2102.md)。

使用此设置页面设置最大大小阈值，以及是否希望在尝试修改大于该最大大小的文件时显示消息 [SBIE2102](SBIE2102.md)。

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)。 