# 开放 IPC 路径

_OpenIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它用于指定路径模式，使沙盘不会对这些进程间对象进行沙箱处理。借此，被沙箱化的程序能够访问由沙箱外程序提供的资源与服务。

可以指定 [程序名前缀](ProgramNamePrefix.md)。

示例：
```ini
   .
   .
   .
   [DefaultBox]
   OpenIpcPath=\RPC Control\IcaApi
   OpenIpcPath=\RPC Control\seclogon
   OpenIpcPath=$:program.exe
```

如 [沙盘跟踪](SandboxieTrace.md) 所述，某些被沙箱化的程序可能需要访问沙箱外的系统资源，以便正常运行。在通过沙盘追踪功能隔离出所需资源后，可以使用此设置，将相关资源暴露给沙箱内程序使用。

```ini
OpenIpcPath=\RPC Control\IcaApi
```

第一个示例暴露了终端服务子系统所提供的一个资源。这允许沙箱内程序与该子系统进行通信，并发现计算机上处于活动状态的其他终端服务器会话。但该资源也可能被用于终止沙盘外控制的程序。

```ini
OpenIpcPath=\RPC Control\seclogon
```
第二个示例暴露了由 Windows _以其他身份运行_ 服务提供的资源。这允许沙箱内的程序使用不同用户的凭据启动另一个程序。在 [v0.7.3 / 5.49.5](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.7.3) 之前，启动的程序会在沙盘控制之外运行；而自该版本起，会在沙箱中运行。

该设置支持通配符。关于 _OpenXxxPath_ 和 _ClosedXxxPath_ 设置中通配符的用法，请参见 [OpenFilePath](OpenFilePath.md)。

```ini
OpenIpcPath=$:program.exe
```
第三个示例允许在沙箱中运行的程序完整访问沙箱外指定目标进程的地址空间。被访问目标进程的进程名称需与设置中指定的名称完全匹配。若未作此设置，沙盘内程序对沙盘外进程仅有只读访问权限。这种 _OpenIpcPath_ 的设置形式不支持通配符。

**注意：** 本页中的这些示例若实际应用，会在沙箱之内产生安全漏洞。它们仅用于说明为何某些资源会被阻止，以及在需要时如何解除阻止并暴露资源用以访问。

相关 [沙盘控制](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > IPC 访问 > 直接访问](ResourceAccessSettings.md#ipc-access--direct-access)

相关 Sandboxie Plus 设置：沙箱选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 开放