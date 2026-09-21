# Unrestricted SCM

_UnrestrictedSCM_ is an advanced sandbox setting that bypasses one Service Control Manager (SCM) permission check in Sandboxie's service-start authorization path:

```ini
[DefaultBox]
UnrestrictedSCM=y
```

The default is `n`.

> [!WARNING]
> Enabling this setting weakens isolation. It should be used only when a service-compatibility requirement has been established.

## What the setting changes

When the broad `RunServicesAsSystem=y` path selects a SYSTEM source token for a sandboxed service, SbieSvc normally checks whether the caller would have `SC_MANAGER_ALL_ACCESS` to the real Windows SCM. It obtains the SCM security descriptor and performs a Windows access check using the appropriate caller token for the box mode. If that check fails, Sandboxie rejects the SYSTEM-service launch.

_UnrestrictedSCM_ bypasses that specific permission check. It does not grant unrestricted SCM access to every sandboxed process or disable Sandboxie's general SCM interception and emulation.

## Related service controls

_UnrestrictedSCM_ does not:

- enable `RunServicesAsSystem`;
- add a service to `RunServiceAsSystem`;
- classify a service as sandboxed;
- move an existing host service into the sandbox;
- make the resulting service process unsandboxed.

`RunServicesAsSystem` and `RunServiceAsSystem` select SYSTEM source identity through separate broad and per-service paths. See [Sandboxed Services](SandboxedServices.md) for those settings.

Sandboxie evaluates [Drop Admin Rights](DropAdminRights.md) before the _UnrestrictedSCM_ check. If drop-rights policy already denies the elevation path, enabling _UnrestrictedSCM_ does not override that denial.

`SandboxieDcomLaunch.exe` has a separate built-in authorization exception and does not require _UnrestrictedSCM_.

## Configuration scope

_UnrestrictedSCM_ is a box-wide Boolean setting. Normal template and global fallback can contribute its effective value when the box does not provide an overriding value. It is queried when the relevant service-start authorization is performed, so a configuration reload can affect later requests; it does not alter a service process that is already running.

## SandMan

Open **Sandbox Options > Security Options > Advanced Security** and use:

> Allow only privileged processes to access the Service Control Manager

The checkbox is inverted relative to _UnrestrictedSCM_:

- checked: normal protection is enabled, which is the default;
- unchecked: SandMan can write `UnrestrictedSCM=y`.

SandMan identifies a box with `UnrestrictedSCM=y` as having **Reduced Isolation**.

## Version history

_UnrestrictedSCM_ was introduced in Sandboxie Plus 0.3 / Classic 5.42 as the debug option for disabling the SCM access check added for Security Issue ID-3.

## Related pages

- [Sandboxed Services](SandboxedServices.md)
- [Drop Admin Rights](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
