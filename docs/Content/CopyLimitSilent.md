# Copy Limit Silent

_CopyLimitSilent_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It is typically specified as _CopyLimitSilent=y_ (see [Yes Or No Settings](YesOrNoSettings.md)), and indicates that Sandboxie should not issue alert message [SBIE2102](SBIE2102.md).

The consumer fallback is `n` when no effective value is configured. Applicable templates and `[GlobalSettings]` can supply an effective value.

Usage:

```
   .
   .
   .
   [DefaultBox]
   CopyLimitSilent=y
```

When no explicit migration rule applies and a finite [CopyLimitKb](CopyLimitKb.md) threshold is reached or exceeded, SBIE2102 is issued only if no usable prompt reply is returned and this setting is not enabled. This includes disabled prompting, an unavailable interactive consumer, or a timeout. An affirmative reply selects migration without SBIE2102; an explicit negative reply selects non-copy without SBIE2102 from this decision path.

This setting changes the message, not the migration decision. It does not disable the [large-file prompt](PromptForFileMigration.md), control [NotifyNoCopy](NotifyNoCopy.md) messages SBIE2113/2114/2115, or suppress every migration or prompt-transport error.

The flag is cached during process initialization. Start new affected sandboxed processes after changing it.

Related [Sandboxie Ini](SandboxieIni.md) settings: [CopyLimitKb](CopyLimitKb.md), [PromptForFileMigration](PromptForFileMigration.md).
