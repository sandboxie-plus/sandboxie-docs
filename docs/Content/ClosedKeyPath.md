# Closed Key Path

_ClosedKeyPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will deny _all_ access by sandboxed programs, including _read_ access. This setting essentially blocks registry keys from being accessed by sandboxed programs.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:

```
   .
   .
   .
   [DefaultBox]
   ClosedKeyPath=!msimn.exe,HKEY_CURRENT_USER\Software\Microsoft\Internet Account Manager
```

The example blocks any program _other than_ Outlook Express (_msimn.exe_) from accessing the registry key containing configured email accounts for the active user account.

The value specified for _ClosedKeyPath_ can include wildcards, although for registry keys, the use of wildcards is rarely needed. For more information on this, including examples that show the use of wildcards, see [OpenFilePath](OpenFilePath.md). (_OpenFilePath_ deals with files, not registry keys, but the principle of using wildcards remains the same.)

**Note:** _ClosedKeyPath_ only blocks access to registry keys outside the sandbox, which have not yet been copied (or created) in the sandbox.

**Note:** Unlike the corresponding [OpenKeyPath](OpenKeyPath.md) setting, the _ClosedKeyPath_ settings are always applied to programs in the sandbox, regardless of whether the program's executable file is inside or outside the sandbox.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > Registry Access > Blocked Access](ResourceAccessSettings.md#registry-access--blocked-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Closed
