# Block Password

_BlockPassword_ is a legacy setting that remains honored by the current runtime. Its old user-interface control was removed, and its metadata marks it as superseded by _OpenSamEndpoint_ for the modern Windows password-change compatibility case. Superseded does not mean that _BlockPassword_ is ignored.

The setting controls a separate LSA authentication and password-related filter. It is not an alias for _OpenSamEndpoint_ or _OpenLsaEndpoint_. _OpenLsaSSPI_ has not been confirmed as a current INI setting. See [System Endpoints](SystemEndpoints.md) for the current endpoint filters.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockPassword=n
```

The legacy filter is enabled by default. Specifying _n_ disables that filter. On Windows 10 and later, _OpenSamEndpoint_ became the recommended compatibility setting for password-change behavior beginning with Sandboxie Plus 0.7.0 / Classic 5.48.0; see [#938](https://github.com/sandboxie-plus/Sandboxie/issues/938).

~~Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access-removed)~~
