# 仅限管理员访问加密沙盒数据

_ProtectAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.16.4 / 5.71.4 起可用。这是加密沙盒中默认启用的设置，你可以通过 `ProtectAdminOnly=n` 禁用它。

## 用法：

```ini
   .
   .
   .
   [DefaultBox]
   ProtectAdminOnly=y
```

启用时，在非管理员组成员用户帐户下运行的 [沙盒管理器](SandboxieControl.md)（经典版）或 [沙盒管理器](PlusMigrationGuide.md)（Plus 版）将无法访问加密沙盒的数据。
