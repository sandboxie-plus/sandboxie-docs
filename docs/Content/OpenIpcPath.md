# Open Ipc Path

_OpenIpcPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will not apply sandboxing for inter-process objects. This lets sandboxed programs access resources and services provided by programs running outside the sandbox.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   OpenIpcPath=\RPC Control\IcaApi
   OpenIpcPath=\RPC Control\seclogon
   OpenIpcPath=$:program.exe
```

As described in [Sandboxie Trace](SandboxieTrace.md), some sandboxed programs may need access to system resources outside the sandbox, in order to function correctly. After using the Sandboxie trace facility to isolate the needed resources, this setting is used to expose the resources for use by a sandboxed program.

```
OpenIpcPath=\RPC Control\IcaApi
```

The first example exposes a resource provided by the Terminal Services subsystem. It can let a sandboxed program talk to that subsystem and discover other Terminal Server sessions active in the computer. But this resource can also be used to terminate programs outside the control of Sandboxie.

```
OpenIpcPath=\RPC Control\seclogon
```
The second example exposes the resource provided by the Windows _Run As_ service. It can let a sandboxed program launch another program using the credentials of a different user. The launched program was executed outside of the control of Sandboxie until [v0.7.3 / 5.49.5](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.7.3), which runs it inside the sandbox.

This setting accepts wildcards. For more information on the use of wildcards in the _OpenXxxPath_ and _ClosedXxxPath_ settings, see [OpenFilePath](OpenFilePath.md).

```
OpenIpcPath=$:program.exe
```
The third example permits a program running inside the sandbox to have full access into the address space of a target process running outside the sandbox. The process name of the target process must match the name specified in the setting. When this setting is not specified, Sandboxie allows only read-access by a sandboxed process into a process outside the sandbox. This form of the _OpenIpcPath_ setting does not support wildcards.

**Note:** The examples in this page, if applied, will create vulnerabilities within the sandbox. They are meant only to show why some resources are blocked, and how they can be un-blocked and exposed for use, if necessary.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > IPC Access > Direct Access](ResourceAccessSettings.md#ipc-access--direct-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Open
