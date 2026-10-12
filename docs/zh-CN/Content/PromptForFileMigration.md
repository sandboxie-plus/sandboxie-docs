# 提示文件迁移

_PromptForFileMigration_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。在启用大小限制的情况下，若需要迁移内容的文件达到或超过 [CopyLimitKb](CopyLimitKb.md) 设置的阈值，且尚无显式迁移规则选定处理方式，此选项决定 Sandboxie 是否请求用户作出选择。更多信息参见 [SBIE2102](SBIE2102.md)。

未找到生效的配置值时，运行时默认使用 `y`。生效值也可能来自适用且已启用的模板，或 `[GlobalSettings]` 中的默认设置。

```
   .
   .
   .
   [DefaultBox]
   PromptForFileMigration=n
```

指定 _n_ 会禁用交互式请求。启用提示后，SandMan 可以显示请求，但不保证有程序处理该请求或返回有效答复。同意迁移后会尝试复制完整内容，但不保证复制成功。拒绝迁移、禁用提示或未收到有效答复时，均不复制文件内容。

对于依赖初次迁移的文件打开操作，[CopyBlockDenyWrite](CopyBlockDenyWrite.md) 决定是拒绝打开，还是移除写入和删除权限后重试打开宿主机文件。重试本身也可能失败，因此禁用提示并不保证能够以只读方式访问。用户明确选择“否”时，不会通过此路径产生 SBIE2102；未收到有效答复时，该消息由 [CopyLimitSilent](CopyLimitSilent.md) 控制。

SandMan 提供“记住对此进程的选择”选项。记住的答复适用于该进程后续的迁移请求，不限于同一个文件。该选择仅由界面为此进程保存，不会成为永久的 INI 例外规则，也不会改变 _CopyLimitKb_。

相关 Sandboxie Plus 设置：沙盒选项 > 常规选项 > 文件迁移 > **询问用户是否迁移大文件**。Sandboxie Control Classic 不提供同等的交互式迁移提示功能。

## 使更改生效

与缓存的大小限制和静默标志不同，每次符合条件的大文件迁移判断都会查询此设置。重新加载生效配置后，已运行进程的后续判断也能使用新值，但不会改变已在处理中的请求。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)
