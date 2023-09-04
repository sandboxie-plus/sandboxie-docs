# Read Ipc Path

_ReadIpcPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.16 / 5.55.16. It specifies path patterns for which Sandboxie will allow read access to unsandboxed processes or processes in other boxes. This lets sandboxed programs access resources and services provided by programs running outside the sandbox.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   ReadIpcPath=$:program.exe
```

This example permits a program running inside the sandbox to have read access into the address space of a target process running outside the sandbox or processes in other boxes. The process name of the target process must match the name specified in the setting.

It is also possible to restore the old behavior entirely by specifying:
```
   .
   .
   .
   [DefaultBox]
   ReadIpcPath=$:*
```

By default the only process whos memory can be read is explorer.exe many processes want that and explorer should not keep any secrets normally anyways. To block this you can use:
```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=$:explorer.exe
```

Related Sandboxie Plus setting:

Sandbox Options > General Options > Resource Access > IPC

Sandbox Options > General Options > Restrictions > Other restrictions
