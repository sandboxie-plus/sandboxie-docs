# 封禁 IPC 路径

_ClosedIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 拒绝沙盒化程序对这些路径的_所有_访问，包括_读取_访问。本质上，此设置阻止沙盒化程序访问这些资源。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=\RPC Control\AudioSrv
```

与沙盒化文件、文件夹和注册表项不同，Sandboxie 通常不允许沙盒化程序访问非沙盒化资源。此规则的例外是：资源在 [开放 IPC 路径](OpenIpcPath.md) 设置中被指定，或 Sandboxie 默认识别该资源并将其暴露供沙盒内使用。

_ClosedIpcPath_ 设置通常用于阻止那些 Sandboxie 默认识别的资源。在上面的示例中，AudioSrv 资源被阻止。此资源提供对音频硬件的访问，换句话说，它让沙盒化程序能够产生声音。阻止它后，沙盒化程序实际上就被静音了。

此设置接受通配符。关于在 _OpenXxxPath_ 和 _ClosedXxxPath_ 设置中使用通配符的更多信息，参见 [开放文件路径](OpenFilePath.md)。

**注意：** 与对应的 [开放 IPC 路径](OpenIpcPath.md) 设置不同，_ClosedKeyPath_ 设置始终适用于沙盒化程序，无论程序可执行文件位于沙盒内还是沙盒外。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > IPC 访问 > 阻止访问](ResourceAccessSettings.md#ipc-访问-阻止访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 封闭
