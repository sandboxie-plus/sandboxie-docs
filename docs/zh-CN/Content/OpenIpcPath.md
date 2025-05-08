# 开放IPC路径

_OpenIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 不会对其应用沙盒化的进程间对象路径模式。这允许沙盒化程序访问由沙盒外运行的程序提供的资源和服务。

可以指定[程序名称前缀](ProgramNamePrefix.md)。

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

如 [Sandboxie Trace](SandboxieTrace.md) 中所述，一些沙盒化程序可能需要访问沙盒外的系统资源才能正常运行。在使用 Sandboxie 跟踪工具隔离所需资源后，此设置用于暴露这些资源供沙盒化程序使用。

```
OpenIpcPath=\RPC Control\IcaApi
```

第一个示例暴露了由终端服务子系统提供的资源。它可以让沙盒化程序与该子系统通信，并发现计算机中活动的其他终端服务器会话。但此资源也可用于终止 Sandboxie 控制之外的程序。

```
OpenIpcPath=\RPC Control\seclogon
```

第二个示例暴露了由 Windows _以其他用户身份运行_服务提供的资源。它可以让沙盒化程序使用不同用户的凭据启动另一个程序。在 [v0.7.3 / 5.49.5](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.7.3) 版本之前，启动的程序在 Sandboxie 控制之外执行，该版本将其在沙盒内运行。

此设置接受通配符。有关在 _OpenXxxPath_ 和 _ClosedXxxPath_ 设置中使用通配符的更多信息，请参见 [OpenFilePath](OpenFilePath.md)。

```
OpenIpcPath=$:program.exe
```

第三个示例允许在沙盒内运行的程序完全访问沙盒外运行的目标进程的地址空间。目标进程的进程名称必须与设置中指定的名称匹配。当未指定此设置时，Sandboxie 只允许沙盒化进程对沙盒外的进程进行读取访问。这种形式的 _OpenIpcPath_ 设置不支持通配符。

**注意：** 如果应用本页中的示例，将在沙盒内创建漏洞。它们仅用于说明为什么某些资源被阻止，以及如何在必要时解除阻止并暴露它们以供使用。

相关的 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > IPC 访问 > 直接访问](ResourceAccessSettings.md#ipc-access--direct-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 开放 