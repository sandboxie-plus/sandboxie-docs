# Closed Ipc Path

_ClosedIpcPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will deny _all_ access by sandboxed programs, including _read_ access. This setting essentially blocks resources from being accessed by sandboxed programs.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:

```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=\RPC Control\AudioSrv
```

Unlike sandboxed files, folders and registry keys, Sandboxie will generally not allow a sandboxed program to access a non-sandboxed resource. The exceptions to this rule are if the resource was specified in an [OpenIpcPath](OpenIpcPath.md) setting, or if Sandboxie by default recognizes the resource and exposes it for use inside the sandbox.

The _ClosedIpcPath_ setting is typically useful to block those resources that Sandboxie recognizes by default. In the example above, the AudioSrv resource is blocked. This resource provides access to audio hardware, in other words, it enables sandboxed programs to generate sound. By blocking it, the sandboxed program is essentially muted.

This setting accepts wildcards. For more information on the use of wildcards in the _OpenXxxPath_ and _ClosedXxxPath_ settings, see [OpenFilePath](OpenFilePath.md).

**Note:** Unlike the corresponding [OpenIpcPath](OpenIpcPath.md) setting, the _ClosedKeyPath_ settings always applies to sandboxed programs, whether the program executable file resides within the sandbox, or out of it.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > IPC Access > Blocked Access](ResourceAccessSettings.md#ipc-access--blocked-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Closed
