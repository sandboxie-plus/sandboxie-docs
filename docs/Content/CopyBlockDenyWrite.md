# Copy Block Deny Write

_CopyBlockDenyWrite_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 0.6.5. It controls what happens to an open that needs file migration when Sandboxie has decided not to copy the host file.

Usage:

```ini
[DefaultBox]
CopyBlockDenyWrite=y
CopyBlockDenyWrite=viewer.exe,n
```

The syntax is `CopyBlockDenyWrite=[program,]y|n`. The optional [Program Name Prefix](ProgramNamePrefix.md) makes the value apply only to that executable. Multiple entries can provide values for different programs, but this is a yes-or-no setting rather than a path list.

When set to `y`, an open that requires a sandbox copy fails with access denied if the migration decision is **do not copy**. When absent or set to `n`, Sandboxie instead removes write and delete rights from the request and retries the open against the host file. A read-capable request may therefore succeed as read-only; a request that cannot be satisfied after those rights are removed may still fail.

The **do not copy** decision can come from a matching [DontCopy](DontCopy.md) rule or from the normal size decision controlled by [CopyLimitKb](CopyLimitKb.md), including when a large-file prompt is unavailable or declined. This setting does not itself choose files or prevent successful migrations.

Matching [CopyAlways](CopyAlways.md) and [CopyEmpty](CopyEmpty.md) rules select copy modes instead, so _CopyBlockDenyWrite_ does not act on those outcomes. [CopyNewer](CopyNewer.md) refreshes an existing sandbox copy and is also unrelated to this failure choice.

[CopyLimitSilent](CopyLimitSilent.md) only controls message SBIE2102 for a size-based refusal; it does not change whether the open is denied or retried read-only. For an explicit _DontCopy_ rule, enabling [NotifyNoCopy](NotifyNoCopy.md) produces SBIE2114 when this setting is `y`, or SBIE2115 for the read-only fallback when it is `n`.

In SandMan, open Sandbox Options > General Options > File Migration. The checkbox is phrased in the opposite direction: **When a file cannot be migrated, open it in read-only mode instead**. Clearing that checkbox enables `CopyBlockDenyWrite=y`.

Related [Sandboxie Ini](SandboxieIni.md) settings: [DontCopy](DontCopy.md), [CopyAlways](CopyAlways.md), [CopyEmpty](CopyEmpty.md), [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md), [NotifyNoCopy](NotifyNoCopy.md). See also [File Migration Settings](FileMigrationSettings.md).
