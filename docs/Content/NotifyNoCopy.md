# Notify No Copy

_NotifyNoCopy_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.7.0. It enables messages for migration rules that deliberately omit some or all of a host file's contents.

Usage:

`NotifyNoCopy=y|n`

```ini
[DefaultBox]
NotifyNoCopy=y
```

This is a [Yes Or No Setting](YesOrNoSettings.md), not a path list. It applies to the sandbox in which it is configured (or to sandboxes that inherit it from `[GlobalSettings]`) and does not accept a program-name prefix. When the setting is absent or set to `n`, these notifications are disabled.

When enabled, Sandboxie issues a message after an explicit file migration rule matches:

- SBIE2113 when [CopyEmpty](CopyEmpty.md) selects a copy without the host file contents.
- SBIE2114 when [DontCopy](DontCopy.md) selects non-copy with [CopyBlockDenyWrite](CopyBlockDenyWrite.md) enabled, the deny-write mode for initial migration.
- SBIE2115 when _DontCopy_ selects non-copy with deny-write disabled, the reduced-access retry mode for initial migration.

The message includes the file name, sandbox name, and host file size. It is generated when the migration code selects the matching _CopyEmpty_ or _DontCopy_ rule, not merely when a sandboxed program reads the file.

There is no dedicated _NotifyNoCopy_ message for [CopyNewer](CopyNewer.md). However, its refresh migration can select _CopyEmpty_ or _DontCopy_ and emit the corresponding notification. These messages describe the selected migration mode, not proof of completed copying or the eventual open result. During a refresh, a non-copy result can leave the existing sandbox copy available rather than deny its open or retry against the host.

_NotifyNoCopy_ does not report successful [CopyAlways](CopyAlways.md) migrations, ordinary access to an existing sandbox copy without such a refresh, or general low-level copy failures. It also does not report a file rejected only by the [CopyLimitKb](CopyLimitKb.md) size decision. Size-limit message SBIE2102 is controlled separately by [CopyLimitSilent](CopyLimitSilent.md).

In SandMan, open Sandbox Options > General Options > File Migration and select **Issue message 2113/2114/2115 when a file is not fully migrated**.

Related [Sandboxie Ini](SandboxieIni.md) settings: [CopyEmpty](CopyEmpty.md), [DontCopy](DontCopy.md), [CopyBlockDenyWrite](CopyBlockDenyWrite.md), [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md). See also [File Migration Settings](FileMigrationSettings.md).
