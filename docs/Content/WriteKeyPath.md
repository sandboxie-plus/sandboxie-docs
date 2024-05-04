# Write Key Path

WriteKeyPath is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will hide any registry keys outside the sandbox, while allowing new registry keys and registry values to be created in the sandbox.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   WriteKeyPath=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```


This example hides any data which exists outside the sandbox within the _TypedPaths_ registry key, while allowing a program to create new keys and values within the corresponding _TypedPaths_ registry key in the sandbox. This means that Windows Explorer running in the sandbox will not be able to display the history of paths that were typed into Windows Explorer outside the sandbox. But the Windows Explorer running in the sandbox will be able to record and store new paths as they are typed.

Note: _WriteKeyPath_ is implemented internally as an enhanced form of [ClosedKeyPath](ClosedKeyPath.md).

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > Registry Access > Write-Only Access](ResourceAccessSettings.md#registry-access--write-only-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Box Only (Write Only)
