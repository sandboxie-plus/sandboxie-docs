# 关闭的 IPC 路径

_ClosedIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置。它指定了 Sandboxie 将拒绝沙盒程序进行 _所有_ 访问（包括 _读取_ 访问）的路径模式。此设置实际上阻止沙盒程序访问特定的资源。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=\RPC Control\AudioSrv
```

与沙盒文件、文件夹和注册表项不同，Sandboxie 通常不允许沙盒程序访问非沙盒资源。此规则的例外情况是：如果资源在 [OpenIpcPath](OpenIpcPath.md) 设置中指定，或者如果 Sandboxie 默认识别该资源并将其暴露给沙盒内使用。

_ClosedIpcPath_ 设置通常用于阻止那些 Sandboxie 默认识别的资源。在上面的示例中，AudioSrv 资源被阻止。此资源提供对音频硬件的访问，换句话说，它使沙盒程序能够生成声音。通过阻止它，沙盒程序实际上被静音。

此设置接受通配符。有关在 _OpenXxxPath_ 和 _ClosedXxxPath_ 设置中使用通配符的更多信息，请参见 [开放文件路径](OpenFilePath.md)。

**注意：** 与相应的 [OpenIpcPath](OpenIpcPath.md) 设置不同，_ClosedKeyPath_ 设置始终适用于沙盒程序，无论程序可执行文件是位于沙盒内还是沙盒外。

相关的 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > IPC 访问 > 阻止访问](ResourceAccessSettings.md#ipc-access--blocked-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 关闭 