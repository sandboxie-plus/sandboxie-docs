# Auto Recover Ignore

_AutoRecoverIgnore_ is a repeatable sandbox setting in [Sandboxie Ini](SandboxieIni.md). Automatic [Immediate Recovery](ImmediateRecovery.md) detection checks this list after matching [RecoverFolder](RecoverFolder.md), so ignored candidates are not reported for automatic recovery. SandMan can also use it to hide matching [Quick Recovery](QuickRecovery.md) entries when [UseAutoRecoverIgnoreForQuick](UseAutoRecoverIgnoreForQuick.md) is enabled. For example:

```
   .
   .
   .
   [DefaultBox]
   AutoRecoverIgnore=.part
   AutoRecoverIgnore=%Desktop%
   AutoRecoverIgnore=C:\Folder
```

The first example excludes files ending in _.part_ from automatic recovery. Such files can represent incomplete downloads; removing the extension can make the completed file eligible. The supplied AutoRecoverIgnore template includes _.part_. Literal entries are matched case-insensitively as path-prefix or end-of-path suffix patterns, as applicable.

The second and third examples exclude the specified folders from automatic recovery. Effective ignore entries can also come from enabled templates.

Since Sandboxie Plus 1.18.0, entries may contain wildcard patterns using `*`, `?`, and `**`. Matching can consider translated NT, DOS, and network-alias paths. The process-side detector and SandMan's Quick Recovery list use different pattern matchers, so these symbols should not be read as a universal filesystem glob grammar.

Since Sandboxie Plus 1.18.0, the exclusion list can also be applied to the [Quick Recovery](QuickRecovery.md) window; see [UseAutoRecoverIgnoreForQuick](UseAutoRecoverIgnoreForQuick.md). The window's **Show All Files** or **Show Ignored** view can expose entries hidden by Quick-list filtering; neither changes automatic detection's own ignore check.

See [File Recovery Architecture](RecoveryArchitecture.md) for the distinction between automatic detection and Quick-list filtering.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Recovery > Immediate Recovery](RecoverySettings.md#immediate-recovery)
