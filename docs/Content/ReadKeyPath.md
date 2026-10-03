# Read Key Path

_ReadKeyPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). A winning rule selects direct host Registry access. In a standard sandbox with the Registry filter active, host write/delete access is normally denied by the driver. Native Windows permissions also remain applicable.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   ReadKeyPath=HKEY_LOCAL_MACHINE\SOFTWARE\Policies
```

With the standard Registry filter active and this rule selected, the example uses host reads for the _Policies_ key and its descendants while normally denying host write/delete access.

Note: _ReadKeyPath_ uses the same direct-host data path as [OpenKeyPath](OpenKeyPath.md); ordinary sandbox copies are not merged into that selected view. This describes the normal access path, not every metadata/query API. Disabling relevant Registry filtering changes the read-only enforcement assumption, and configuration changes do not universally revoke already-open handles.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > Registry Access > Read-Only Access](ResourceAccessSettings.md#registry-access-read-only-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Read Only
