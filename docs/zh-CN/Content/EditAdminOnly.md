# 仅管理员可编辑

_EditAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。如果指定此设置，在非管理员组成员的用户账户下运行的 [Sandboxie Control](SandboxieControl.md) 或 [Sandman](PlusMigrationGuide.md) 将无法在全局设置部分或任何沙盒部分进行任何配置更改。但是，即使在这种情况下，他们仍然可以在用户设置部分进行更改。

用法：

```
   .
   .
   .
   [GlobalSettings]
   EditAdminOnly=y
```

此设置专为网络管理员使用而设计。 