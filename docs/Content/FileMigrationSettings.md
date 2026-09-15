# File Migration Settings

SandMan > Sandbox Options > General Options > File Migration

Sandboxie normally lets a sandboxed program read a host file without first copying it. When the program requests an operation that needs to change an existing file, Sandboxie migrates the file into the sandbox and applies the change to that sandbox copy. The host file remains unchanged.

The File Migration page controls the normal size decision and the path rules that can override it.

## Migration rules

The rule list supports four actions:

- **Always copy** ([CopyAlways](CopyAlways.md)) migrates the matching host file with its contents, without applying the normal size threshold.
- **Don't copy** ([DontCopy](DontCopy.md)) prevents content migration. The open is retried without write and delete access, or denied when [CopyBlockDenyWrite](CopyBlockDenyWrite.md) is enabled.
- **Copy empty** ([CopyEmpty](CopyEmpty.md)) creates a zero-length sandbox copy instead of migrating the host contents.
- **Copy newer** ([CopyNewer](CopyNewer.md)) refreshes an existing sandbox copy when the matching host file has a later last-write time.

The first three actions select how an existing regular host file is initially migrated. If their patterns overlap, _DontCopy_ takes priority over _CopyAlways_, which takes priority over _CopyEmpty_. _CopyNewer_ is a separate check for a sandbox copy that already exists.

Rules may be repeated and may be limited to a program. See the dedicated setting pages for syntax, pattern behavior, and open-mode limitations.

## Normal size decision

When no initial-migration rule matches, Sandboxie compares the host file size with [CopyLimitKb](CopyLimitKb.md). A file strictly smaller than the configured threshold is copied with its contents; setting the limit to `-1` disables the size limit. For a file that reaches or exceeds the threshold, SandMan can prompt the user according to [PromptForFileMigration](PromptForFileMigration.md). If migration is not approved, the open falls back to read-only access or is denied according to [CopyBlockDenyWrite](CopyBlockDenyWrite.md).

[CopyLimitSilent](CopyLimitSilent.md) controls message [SBIE2102](SBIE2102.md) when the size decision prevents migration and no prompt result is returned. [NotifyNoCopy](NotifyNoCopy.md) separately controls messages SBIE2113, SBIE2114, and SBIE2115 for explicit _CopyEmpty_ and _DontCopy_ rules.
