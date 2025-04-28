# Open Key Path

_OpenKeyPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies a path patterns, for which Sandboxie will not apply sandboxing for registry keys. This lets sandboxed programs have direct access to update system settings _outside the sandbox_. This setting essentially _punches a hole_ in the sandbox, at a particular registry key location.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   OpenKeyPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenKeyPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

These examples let the Firefox program, _firefox.exe_, have direct access to the Mozilla registry key trees (both system-wide and per-user registry trees).

The value specified for _OpenKeyPath_ can include wildcards, although for registry keys, the use of wildcards is rarely needed. For more information on this, including examples that show the use of wildcards, see [OpenFilePath](OpenFilePath.md). (_OpenFilePath_ deals with files, not registry keys, but the principle of using wildcards remains the same.)

**Note:** For security reasons, this setting does not apply when the program executable file resides within the sandbox. This means that (potentially malicious) software downloaded into your computer and executed, cannot take advantage of this setting.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > Registry Access > Direct Access](ResourceAccessSettings.md#registry-access--direct-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Open
