# 删除设置

## “删除”设置组

[沙盒管理器](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 删除：

![](../Media/DeleteSettings.png)

在这里配置 Sandboxie 在何时以及如何删除沙盒。

## 调用方式

[沙盒管理器](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 删除 > 调用方式：

![](../Media/DeleteInvocationSettings.png)

使用此设置页指定希望何时删除沙盒：

* 仅在显式请求时删除：保持两个复选框均不勾选
* 定期自动删除：勾选第一个复选框
* 从不删除：勾选第二个复选框

注意：虽然两个复选框都可以不勾选，但同一时间只能勾选其中一个。

只要第二个复选框处于勾选状态，即使你显式提出请求，Sandboxie 也不会对沙盒发起任何删除操作。重要提示：这并不能保护沙盒免于被其他程序删除。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[自动删除](AutoDelete.md)、[从不删除](NeverDelete.md)、[删除命令](DeleteCommand.md)。

## 命令

[沙盒管理器](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 删除 > 命令：

![](../Media/DeleteCommandSettings.png)

使用此设置页指定用于删除沙盒的系统命令。默认是一个简单的 RMDIR（删除目录）命令。注重隐私问题的用户可以选择改用安全删除，详见 [安全删除沙盒](SecureDeleteSandbox.md)。

你可以使用按钮选择一个预设命令。RMDIR 按钮会选择上面提到的简单 RMDIR 命令。

SDelete 按钮使用 [SysInternals/Microsoft 的 SDelete](https://docs.microsoft.com/en-us/sysinternals/downloads/sdelete) 删除沙盒内容。注意，你需要调整命令的路径。

Eraser 按钮使用 [Heidi Computers 的 Eraser](https://eraser.heidi.ie/) 删除沙盒内容。
