# 关闭的注册表项路径

_ClosedKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置。它指定了 Sandboxie 将拒绝沙盒程序进行 _所有_ 访问（包括 _读取_ 访问）的路径模式。此设置实际上阻止沙盒程序访问特定的注册表项。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedKeyPath=!msimn.exe,HKEY_CURRENT_USER\Software\Microsoft\Internet Account Manager
```

此示例阻止除 Outlook Express (_msimn.exe_) 之外的任何程序访问包含活动用户账户已配置电子邮件账户的注册表项。

为 _ClosedKeyPath_ 指定的值可以包含通配符，尽管对于注册表项，很少需要使用通配符。有关此内容的更多信息，包括展示通配符使用的示例，请参见 [开放文件路径](OpenFilePath.md)。（_OpenFilePath_ 处理的是文件而不是注册表项，但使用通配符的原则保持不变。）

**注意：** _ClosedKeyPath_ 仅阻止访问沙盒外的注册表项，这些注册表项尚未在沙盒中复制（或创建）。

**注意：** 与相应的 [OpenKeyPath](OpenKeyPath.md) 设置不同，_ClosedKeyPath_ 设置始终适用于沙盒中的程序，无论程序可执行文件是位于沙盒内还是沙盒外。

相关的 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 注册表访问 > 阻止访问](ResourceAccessSettings.md#registry-access--blocked-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 关闭 