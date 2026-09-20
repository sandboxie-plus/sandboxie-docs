# Strip System Privileges

_StripSystemPrivileges_ controls privilege removal from SYSTEM-source tokens created through specific SbieSvc service and RpcSs paths:

```ini
[DefaultBox]
StripSystemPrivileges=y
```

The default is `y`, which is the protective behavior.

> [!WARNING]
> `StripSystemPrivileges=n` restores the older, less-restricted behavior for affected SYSTEM-token paths and is not recommended.

## Privileges removed

When enabled on an affected path, Sandboxie removes these privileges from the newly duplicated token:

- `SeTcbPrivilege`
- `SeCreateTokenPrivilege`

Sandboxie uses the Windows `SE_PRIVILEGE_REMOVED` operation. The privileges are removed from that token rather than merely disabled, so they cannot simply be re-enabled on the same token. `SeAssignPrimaryTokenPrivilege` is not removed by the current helper.

## Runtime scope

The current implementation applies this setting when SbieSvc creates:

- a SYSTEM-source token for a sandboxed service selected to run as SYSTEM;
- a SYSTEM-source token for the relevant sandboxed RpcSs process-server path.

It does not apply to ordinary user-token service launches and should not be described as a global privilege filter for every sandboxed process or every SYSTEM process.

If token duplication, adjustment, or the required privilege-removal operation fails, the affected launch or token request fails rather than intentionally continuing with an unstripped SYSTEM token.

## Configuration scope

_StripSystemPrivileges_ is a box-wide Boolean setting. Normal template and global fallback can contribute its effective value when the box does not provide an overriding value. It is consulted when an affected token is created, so changing it does not modify tokens already assigned to running processes. Restart the affected sandboxed service or process after changing it.

## SandMan

Open **Sandbox Options > Security Options > Advanced Security** and use:

> Drop critical privileges from processes running with a SYSTEM token

The checkbox directly represents the protective setting:

- checked: privilege removal is enabled, which is the default;
- unchecked: SandMan writes `StripSystemPrivileges=n`.

## Relationship to Session 0 startup

[Start System Box](StartSystemBox.md) uses a different startup path. A box being started in Session 0 with SYSTEM identity does not, by itself, cause that token to pass through the _StripSystemPrivileges_ helper documented here.

## Version history

_StripSystemPrivileges_ was introduced in Sandboxie Plus 0.5.4 / Classic 5.46.0 as part of the fix for Security Issue ID-4.

## Related pages

- [Sandboxed Services](SandboxedServices.md)
- [Start System Box](StartSystemBox.md)
- [Drop Admin Rights](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
