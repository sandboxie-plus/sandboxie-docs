# 删除设置

## “删除”设置分组

[沙箱控制](SandboxieControl.md) > [沙箱设置](SandboxSettings.md) > 删除：

![](../Media/DeleteSettings.png)

在此页面，您可以配置 Sandboxie 删除沙箱的时间和方式

## 调用方式

[沙箱控制](SandboxieControl.md) > [沙箱设置](SandboxSettings.md) > 删除 > 调用方式：

![](../Media/DeleteInvocationSettings.png)

该设置页面用于指示您希望在何时删除沙箱：

- 仅在明确请求时删除：请保持两个复选框均未选中  
- 定期自动删除：请选中第一个复选框  
- 永不删除：请选中第二个复选框

请注意，虽然两个复选框都可以被清除，但任何时候都只能选中一个复选框。

只要第二个复选框被选中，Sandboxie 将不会对沙箱执行任何删除操作，即使您明确要求删除也不会执行。重要提示：这无法防止其他程序删除沙箱。

相关的 [Sandboxie Ini](SandboxieIni.md) 设置： [自动删除](AutoDelete.md)、[从不删除](NeverDelete.md)、[删除命令](DeleteCommand.md)。

## 命令

[沙箱控制](SandboxieControl.md) > [沙箱设置](SandboxSettings.md) > 删除 > 命令：

![](../Media/DeleteCommandSettings.png)

本设置页用于指定用于删除沙箱的系统命令。默认情况下为 RMDIR（删除目录）命令。关心隐私问题的用户可以选择使用更安全的删除方式，详细说明参见 [安全删除沙箱](SecureDeleteSandbox.md)。

您可以使用页面上的按钮来选择预定义命令。RMDIR 按钮会选择上述的简单 RMDIR 命令。

SDelete 按钮会调用由 [SysInternals/Microsoft 提供的 SDelete](https://docs.microsoft.com/en-us/sysinternals/downloads/sdelete) 以删除沙箱内容。请注意，您需要自行调整命令路径。

Eraserl 按钮会调用由 [Heidi Computers 提供的 Eraser](https://eraser.heidi.ie/) 以删除沙箱内容。