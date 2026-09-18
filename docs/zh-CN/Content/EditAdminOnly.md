# 仅管理员可编辑

_EditAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。如果指定，在非管理员组成员用户帐户下运行的 [沙盒管理器](SandboxieControl.md)（经典版）或 [沙盒管理器](PlusMigrationGuide.md)（Plus 版）将无法在全局设置节或任何沙盒节中做出任何配置更改。不过，即使在这种情况下，它们仍然可以在用户设置节中做出更改。

用法：

```
   .
   .
   .
   [GlobalSettings]
   EditAdminOnly=y
```

此设置专为网络管理员使用而设计。
