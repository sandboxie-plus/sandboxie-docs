# 仅限管理员强制禁用

_ForceDisableAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。如果指定此选项，[禁用强制程序](FileMenu.md#disable-forced-programs) 模式将仅对属于管理员组的用户账户可用。

用法：
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableAdminOnly=y
```

此设置设计用于网络管理员使用。