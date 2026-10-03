# Closed Key Path

_ClosedKeyPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which a winning Closed rule denies new hooked registry opens or creates, including _read_ access.

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

**Note:** For a new hooked registry open/create, a winning Closed rule is checked before the normal sandbox-copy path. The existence of a sandbox copy does not by itself bypass the rule. Already-open handles are separate; changing the rule does not imply revocation of a handle that was previously granted.

**Note:** Unlike the ordinary eligibility restriction on [OpenKeyPath](OpenKeyPath.md), Closed rules can apply even when the executable resides inside the sandbox. When `AlwaysCloseForBoxed` is active, a negated program selector does not provide its usual exemption to an executable inside the sandbox; this qualifies the example above.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > Registry Access > Blocked Access](ResourceAccessSettings.md#registry-access-blocked-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Closed
