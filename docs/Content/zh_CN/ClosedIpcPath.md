# 封禁 IPC 路径

_ClosedIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置项。它指定了路径模式，Sandboxie 将拒绝沙盒程序对这些路径的_所有_访问，包括_读取_访问。该设置本质上阻止了沙盒程序访问指定的资源。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=\RPC Control\AudioSrv
```

与沙盒内的文件、文件夹和注册表键不同，Sandboxie 通常不允许沙盒程序访问非沙盒资源。该规则的例外情况是资源被指定在 [开放 IPC 路径](OpenIpcPath.md) 设置中，或者 Sandboxie 默认识别该资源并允许在沙盒内使用。

_ClosedIpcPath_ 设置通常用于阻止那些 Sandboxie 默认识别的资源。在上述示例中，AudioSrv 资源被阻止。该资源提供访问音频硬件的能力，换言之，它使沙盒程序能够产生声音。通过屏蔽它，沙盒程序实际上被静音。

该设置支持通配符。关于在 _OpenXxxPath_ 和 _ClosedXxxPath_ 设置中使用通配符的详细信息，请参见 [开放文件路径](OpenFilePath.md)。

**注意：** 与对应的 [开放 IPC 路径](OpenIpcPath.md) 设置不同，_ClosedKeyPath_ 设置始终适用于沙盒程序，无论程序的可执行文件是位于沙盒内部还是外部。

相关 [Sandboxie 控制](SandboxieControl.md) 设置：  
沙盒设置 > 资源访问 > IPC 访问 > 封禁访问 ([资源访问设置](ResourceAccessSettings.md#ipc-access--blocked-access))

相关 Sandboxie Plus 设置：  
沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问 列 > 封禁