# Use Auto Recover Ignore For Quick

_UseAutoRecoverIgnoreForQuick_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.18.0. It specifies whether the [AutoRecoverIgnore](AutoRecoverIgnore.md) exclusion list is also applied to the [Quick Recovery](QuickRecovery.md) window, hiding matching files from the list of recoverable files.

Usage:

```
   .
   .
   .
   [DefaultBox]
   UseAutoRecoverIgnoreForQuick=n
```

The setting metadata describes an _n_ default, but current SandMan reads an absent value as enabled. Thus its ordinary Quick Recovery list hides matching files unless the option is explicitly set to _n_ or the window's display controls override filtering. This is a SandMan consumer default, not a process-side detector default. Setting _n_ does not change how automatic recovery applies [AutoRecoverIgnore](AutoRecoverIgnore.md).

The Quick Recovery **Show All Files** or **Show Ignored** view can display entries normally hidden by this option. SandMan also consults this preference when deciding whether to open an initial Immediate Recovery dialog for a reported candidate; it does not change the SbieDll detector's ignore decision.

In SandMan, this corresponds to the "Use the above exclusion list to hide matching files from the Quick Recovery window" checkbox under Sandbox Options > File Recovery > Immediate Recovery.

Related [Sandboxie Ini](SandboxieIni.md) settings: [AutoRecoverIgnore](AutoRecoverIgnore.md), [RecoverFolder](RecoverFolder.md). See also [Quick Recovery](QuickRecovery.md).

See [File Recovery Architecture](RecoveryArchitecture.md) for the separate recovery workflows.
