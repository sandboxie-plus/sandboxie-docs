# 文件迁移提示

PromptForFileMigration是[沙盘.ini](SandboxieIni.md)中的一个沙箱设置。它指定了沙盘是否会提示进行大文件迁移。更多信息请参见[SBIE2102](SBIE2102.md)。

```ini
   .
   .
   .
   [DefaultBox]
   PromptForFileMigration=n
```
指定_n_表示沙箱不会提示用户进行文件迁移（访问将为只读）。

相关的沙盘增强版设置：沙箱选项 > 文件选项 > 文件迁移 > 提示用户进行大文件迁移

相关的[沙盘设置](SandboxieIni.md)设置：[复制限制 KB](CopyLimitKb.md)、[复制限制静默](CopyLimitSilent.md)