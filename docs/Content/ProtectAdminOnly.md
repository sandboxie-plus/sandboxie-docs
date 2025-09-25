# Protect Admin Only

_ProtectAdminOnly_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.16.4 / 5.71.4. This is a setting enabled by default in encrypted box, you can disable it by `ProtectAdminOnly=n`.

Usage:

```
   .
   .
   .
   [DefaultBox]
   ProtectAdminOnly=y
```

When enabled, [Sandboxie Control](SandboxieControl.md) or [SandMan](PlusMigrationGuide.md) running under user accounts which are not members of the Administrators group will not be able to access to encrypted box data.
