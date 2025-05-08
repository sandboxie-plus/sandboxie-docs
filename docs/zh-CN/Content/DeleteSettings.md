# 删除设置

## "删除"设置组

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 删除：

![](../Media/DeleteSettings.png)

在这里配置 Sandboxie 何时以及如何删除沙盒。

## 调用

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 删除 > 调用：

![](../Media/DeleteInvocationSettings.png)

使用此设置页面来指定何时删除沙盒：

* 仅通过明确请求删除：保持两个复选框都未选中
* 定期自动删除：选中第一个复选框
* 永不删除：选中第二个复选框

请注意，虽然两个复选框都可以取消选中，但任何时候只能选中一个复选框。

只要选中第二个复选框，Sandboxie 就不会对沙盒发起任何删除操作，即使您明确要求删除。重要提示：这并不能保护沙盒不被其他程序删除。

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[AutoDelete](AutoDelete.md)、[NeverDelete](NeverDelete.md)、[DeleteCommand](DeleteCommand.md)。

## 命令

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 删除 > 命令：

![](../Media/DeleteCommandSettings.png)

使用此设置页面来指定用于删除沙盒的系统命令。默认情况下，这是一个简单的 RMDIR（删除目录）命令。关注隐私问题的人可以选择使用安全删除，如 [安全删除沙盒](SecureDeleteSandbox.md) 中更详细描述的那样。

您可以使用按钮选择预设命令。RMDIR 按钮选择上面提到的简单 RMDIR。

SDelete 按钮使用 [SysInternals/Microsoft 的 SDelete](https://docs.microsoft.com/en-us/sysinternals/downloads/sdelete) 来删除沙盒内容。请注意，您需要调整命令的路径。

Eraserl 按钮使用 [Heidi Computers 的 Eraser](https://eraser.heidi.ie/) 来删除沙盒内容。 