# Drop Admin Rights

_DropAdminRights_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies whether Sandboxie will strip Administrator rights from programs running in this sandbox.

Usage:

```
   .
   .
   .
   [DefaultBox]
   DropAdminRights=y
```

The setting in this page causes Sandboxie to strip administrative rights from programs running in this sandbox.

Specifically, the security credentials used to start the sandboxed program will not include membership in the Administrators and Power Users groups.

Note that this has little effect if you are already running under a non-Administrator user account.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Drop Rights](RestrictionsSettings.md#drop-rights)
