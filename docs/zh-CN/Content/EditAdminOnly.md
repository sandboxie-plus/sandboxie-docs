# 仅管理员可编辑

_EditAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。如果指定了该设置，则在非 Administrators 组成员的用户账户下运行的 [沙盒控制](SandboxieControl.md) 或 [Sandman](PlusMigrationGuide.md) 将无法对全局设置部分或任何沙盒部分进行配置更改。然而，即使在这种情况下，用户仍然可以对用户设置部分进行更改。

用法示例：

```
   .
   .
   .
   [GlobalSettings]
   EditAdminOnly=y
```

此设置适用于网络管理员使用。
