# 封禁注册表项路径

_ClosedKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 拒绝沙盒化程序对这些路径的_所有_访问，包括_读取_访问。本质上，此设置阻止沙盒化程序访问这些注册表项。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedKeyPath=!msimn.exe,HKEY_CURRENT_USER\Software\Microsoft\Internet Account Manager
```

此示例阻止 Outlook Express（_msimn.exe_）_以外_的任何程序访问当前用户帐户存放已配置电子邮件帐户的注册表项。

_ClosedKeyPath_ 指定的值可以包含通配符，不过对注册表项而言，很少需要使用通配符。更多信息（包括展示通配符用法的示例）参见 [开放文件路径](OpenFilePath.md)。（_OpenFilePath_ 处理的是文件而非注册表项，但使用通配符的原理相同。）

**注意：** _ClosedKeyPath_ 只阻止访问沙盒外尚未在沙盒中被复制（或创建）的注册表项。

**注意：** 与对应的 [开放注册表路径](OpenKeyPath.md) 设置不同，_ClosedKeyPath_ 设置始终适用于沙盒中的程序，无论程序的可执行文件位于沙盒内还是沙盒外。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 注册表访问 > 阻止访问](ResourceAccessSettings.md#注册表访问-阻止访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 封闭
