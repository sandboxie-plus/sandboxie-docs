# Block Password

**This feature is obsolete. If you use Windows 10 or later, we recommend _OpenSamEndpoint_ since version 0.7.0 / 5.48.0: [#938](https://github.com/sandboxie-plus/Sandboxie/issues/938)**

_BlockPassword_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies whether Sandboxie will allow sandboxed programs to change the password of user accounts.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockPassword=n
```

Specifying _n_ indicates that a sandboxed program should be permitted to issue requests to change the user account password.

~~Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access--removed)~~
