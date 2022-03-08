# Privacy Mode
_PrivacyMode_ is a Box Type Preset introduced in v1.0.5 / 5.55.5. It can be selected from the Sandboxie Plus interface when creating a new sandbox or in the "General Options" of an existing one. This preset is labeled "with data protection".

It is also a sandbox setting in [Sandboxie Ini](SandboxieIni.md)

Usage:

```
   .
   .
   .
   [DefaultBox]
   UsePrivacyMode=y
```

This mode makes all unsandboxed locations unreadable (except "C:\Windows" and "C:\Program Files"), hence denying programs access to any personal data. Also, the registry only allows reading parts of the local machine's root keys (HKLM) but not user root keys (HKCU). Exceptions can be specified in [Resource Access](ResourceAccess.md).
