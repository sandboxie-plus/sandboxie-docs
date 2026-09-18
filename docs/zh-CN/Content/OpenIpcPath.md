# 开放 IPC 路径

_OpenIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径的进程间对象不应用沙盒化。这让沙盒化程序可以访问由沙盒外运行的程序提供的资源和服务。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenIpcPath=\RPC Control\IcaApi
   OpenIpcPath=\RPC Control\seclogon
   OpenIpcPath=$:program.exe
```

如 [Sandboxie 跟踪](SandboxieTrace.md) 中所述，某些沙盒化程序可能需要访问沙盒外的系统资源才能正常运行。使用 Sandboxie 跟踪功能隔离所需资源后，此设置用于暴露这些资源供沙盒化程序使用。

```
OpenIpcPath=\RPC Control\IcaApi
```

第一个示例暴露由终端服务子系统提供的资源。它可以让沙盒化程序与该子系统通信，并发现计算机中处于活动状态的其他终端服务器会话。但此资源也可以用于终止 Sandboxie 控制之外的程序。

```
OpenIpcPath=\RPC Control\seclogon
```
第二个示例暴露由 Windows _Run As_（运行方式）服务提供的资源。它可以让沙盒化程序使用不同用户的凭据启动另一个程序。在 [v0.7.3 / 5.49.5](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.7.3) 之前，启动的程序在 Sandboxie 的控制之外执行，该版本起改为在沙盒内运行。

此设置接受通配符。关于在 _OpenXxxPath_ 和 _ClosedXxxPath_ 设置中使用通配符的更多信息，参见 [开放文件路径](OpenFilePath.md)。

```
OpenIpcPath=$:program.exe
```
第三个示例允许沙盒内运行的程序完全访问沙盒外运行的某个目标进程的地址空间。目标进程的进程名必须匹配设置中指定的名称。未指定此设置时，Sandboxie 只允许沙盒化进程对沙盒外进程进行只读访问。此形式的 _OpenIpcPath_ 设置不支持通配符。

**注意：** 本页中的示例如果应用，会在沙盒内制造漏洞。它们只是为了说明为什么某些资源会被阻止，以及必要时如何解除阻止并暴露这些资源供使用。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > IPC 访问 > 直接访问](ResourceAccessSettings.md#ipc-访问-直接访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 开放
