# 提示文件迁移

提示文件迁移是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否会提示进行大文件迁移。更多信息参见 [SBIE2102](SBIE2102.md)。

```
   .
   .
   .
   [DefaultBox]
   PromptForFileMigration=n
```

指定 _n_ 表示沙盒不会提示用户进行文件迁移（访问将是只读的）。

相关 Sandboxie Plus 设置：沙盒选项 > 文件选项 > 文件迁移 > 提示用户进行大文件迁移

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制 Kb](CopyLimitKb.md)、[复制限制静默](CopyLimitSilent.md)
