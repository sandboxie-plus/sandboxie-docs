# 封禁注册表路径

_ClosedKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它指定了路径模式，对于这些路径，Sandboxie 会拒绝沙箱程序的 _所有_ 访问权限，包括 _读取_ 权限。此设置实质上阻止了沙箱程序访问注册表键。

可以指定 [程序名前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedKeyPath=!msimn.exe,HKEY_CURRENT_USER\Software\Microsoft\Internet Account Manager
```

此示例阻止除 Outlook Express（msimn.exe）之外的任何程序访问包含活动用户帐户已配置电子邮件账户的注册表键。

_ClosedKeyPath_ 指定的值可以包含通配符，尽管对于注册表键而言，很少需要使用通配符。有关更多信息，包括使用通配符的示例，请参见 [开放文件路径](OpenFilePath.md)。（_OpenFilePath_ 处理文件，而非注册表键，但使用通配符的原理相同。）

**注意：** _ClosedKeyPath_ 仅阻止对沙箱外尚未被复制（或创建）到沙箱中的注册表键的访问。

**注意：** 与对应的 [开放注册表路径](OpenKeyPath.md) 设置不同，_ClosedKeyPath_ 设置始终应用于沙箱中的程序，无论该程序的可执行文件是在沙箱内还是沙箱外。

相关的 [沙箱控制](SandboxieControl.md) 设置: [沙箱设置 > 资源访问 > 注册表访问 > 封禁](ResourceAccessSettings.md#registry-access--blocked-access)

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 注册表 > 添加注册表键 > 访问列 > 封禁
