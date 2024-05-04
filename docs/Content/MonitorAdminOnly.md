# Monitor Admin Only

_MonitorAdminOnly_ is a global setting in [Sandboxie Ini](SandboxieIni.md). If specified, [Sandboxie Control](SandboxieControl.md) running under user accounts which are not members of the Administrators group will not be able to invoke the [Resource Access Monitor](ResourceAccessMonitor.md) facility.

The rationale is that Resource Access Monitor consumes 64K bytes of system memory for each user session in which it is invoked, so network administrators may wish to prevent their users from invoking that facility.

Usage:

```
   .
   .
   .
   [GlobalSettings]
   MonitorAdminOnly=y
```

This setting is designed for use by network administrators.
