# 强制禁用仅限管理员

_ForceDisableAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。如果指定此设置，[禁用强制程序](FileMenu.md#disable-forced-programs)模式将仅对管理员组成员的用户账户可用。

用法：
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableAdminOnly=y
```

此设置专为网络管理员使用而设计。 