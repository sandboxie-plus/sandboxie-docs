# 仅限管理员访问加密沙盘数据

_ProtectAdminOnly_ 是 [沙盘配置文件](SandboxieIni.md) 中的沙盒设置，自 v1.16.4 / 5.71.4 版本起可用。该设置在加密沙盘中默认启用，可以通过 `ProtectAdminOnly=n` 来禁用。

## 用法：

```ini
   .
   .
   .
   [DefaultBox]
   ProtectAdminOnly=y
```

启用后，使用非管理员组用户账户运行的 [Sandboxie Control](SandboxieControl.md) 或 [SandMan](PlusMigrationGuide.md) 将无法访问加密沙盘数据。