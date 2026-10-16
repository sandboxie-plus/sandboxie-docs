# 复制限制静默

_CopyLimitSilent_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。通常指定为 _CopyLimitSilent=y_（参见 [是或否设置](YesOrNoSettings.md)），表示 Sandboxie 不应发出警报消息 [SBIE2102](SBIE2102.md)。

未找到生效的配置值时，运行时默认使用 `n`。适用的模板和 `[GlobalSettings]` 可提供生效值。

用法：

```
   .
   .
   .
   [DefaultBox]
   CopyLimitSilent=y
```

未取消大小限制、没有适用的显式迁移规则，且文件达到或超过 [CopyLimitKb](CopyLimitKb.md) 设置的阈值时，只有未收到有效的提示答复且未启用此设置，才会发出 SBIE2102。这包括禁用提示、没有可用的程序处理交互式请求，或请求超时的情况。用户同意时会选择迁移，明确拒绝时会选择不复制；两种答复都不会通过此判断路径产生 SBIE2102。

此设置只影响消息，不改变迁移决定。它不会关闭[大文件迁移提示](PromptForFileMigration.md)，不控制 [NotifyNoCopy](NotifyNoCopy.md) 的 SBIE2113、SBIE2114、SBIE2115 消息，也不会屏蔽所有迁移错误或提示请求传输错误。

此标志在进程初始化时缓存。修改后，应重新启动相关沙盒进程。

相关 [Sandboxie Ini](SandboxieIni.md) 设置项：[复制限制 Kb](CopyLimitKb.md)、[提示文件迁移](PromptForFileMigration.md)。
