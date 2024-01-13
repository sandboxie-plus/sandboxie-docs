# Open Conf Path

_OpenConfPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.0 / 5.55.0. It specifies a path pattern, for which Sandboxie will not apply sandboxing for registry keys. This lets sandboxed programs have direct access to update system settings _outside the sandbox_. This setting essentially _punches a hole_ in the sandbox, at a particular registry key location.

It is the same as the [OpenKeyPath](OpenKeyPath.md) setting, except that this setting is always applied, whereas _OpenKeyPath_ is only applied if the application is running from a file or folder that is located outside the sandbox.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   OpenConfPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenConfPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

These examples let the Firefox program, _firefox.exe_, have direct access to the Mozilla registry key trees (both system-wide and per-user registry trees).

The value specified for _OpenConfPath_ can include wildcards, although for registry keys, the use of wildcards is rarely needed. For more information on this, including examples that show the use of wildcards, see [OpenFilePath](OpenFilePath.md). (_OpenFilePath_ deals with files, not registry keys, but the principle of using wildcards remains the same.)

**Note:** This setting does apply even when the program executable file resides within the sandbox. This means that (potentially malicious) software downloaded into your computer and executed, can take advantage of this setting.

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Open for All
