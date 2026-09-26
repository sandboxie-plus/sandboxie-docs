# Auto Recover

_AutoRecover_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). With _AutoRecover=y_, SbieDll initializes process-side [Immediate Recovery](ImmediateRecovery.md) detection using the effective [RecoverFolder](RecoverFolder.md) and [AutoRecoverIgnore](AutoRecoverIgnore.md) entries. It reports eligible files to the recovery UI; it does not itself move files to the host.

When no effective value is present, the detector's runtime fallback is disabled. Classic new-box defaults explicitly enable it, and the current SandMan new-box wizard offers it enabled by default. [Quick Recovery](QuickRecovery.md) remains available when _AutoRecover=n_ because its SandMan scan is separate. Restart affected sandboxed processes after changing automatic detection settings.

Usage:

```
   .
   .
   .
   [DefaultBox]
   AutoRecover=y
```

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Recovery > Immediate Recovery](RecoverySettings.md#immediate-recovery)

See [File Recovery Architecture](RecoveryArchitecture.md) for the complete workflow.
