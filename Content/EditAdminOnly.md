# Edit Admin Only

_EditAdminOnly_ is a global setting in [Sandboxie Ini](SandboxieIni). If specified, [Sandboxie Control](SandboxieControl) running under user accounts which are not members of the Administrators group will not be able to make any configuration changes in the global settings section or any sandbox section. However, even in that case, [Sandboxie Control](SandboxieControl) will still be able to make changes in the user settings section.

Usage:

```
   .
   .
   .
   [GlobalSettings]
   EditAdminOnly=yes
```

This setting is designed for use by network administrators.
