# Copy Always

_CopyAlways_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 0.6.5. It specifies host-file path patterns that must be migrated with their contents when a sandboxed program needs a sandbox copy.

Usage:

`CopyAlways=[program,]pattern`

```ini
[DefaultBox]
CopyAlways=C:\Data\Reference\*.db
CopyAlways=reporter.exe,*\Reports\*.csv
```

Each _CopyAlways_ entry is one rule, and the setting may be repeated. The optional prefix before the comma limits a rule to that program; see [Program Name Prefix](ProgramNamePrefix.md). Paths use the same pattern form as [OpenFilePath](OpenFilePath.md). Matching is case-insensitive and is performed against the host (true) file path. `*` matches any sequence of characters, including path separators, and `?` matches one character.

When a program prefix is used, current setting metadata requires the drive or device portion of a path to be represented by a wildcard, for example `*\Reports\*.csv`. Do not use a fixed drive path such as `C:\Reports\*.csv` or rely on an [expandable variable](ExpandableVariables.md) that becomes a full path in a program-specific rule.

Normally, Sandboxie migrates an existing host file only when a sandboxed program requests an operation that needs a sandbox copy. If the file matches _CopyAlways_, Sandboxie selects a full-content migration before considering [CopyLimitKb](CopyLimitKb.md). The configured size threshold and the large-file prompt are therefore bypassed for the matching migration; [CopyLimitSilent](CopyLimitSilent.md) has no effect on it.

If _CopyAlways_ is absent or no entry matches, Sandboxie uses another matching migration rule or its normal size-based decision. When rules overlap, [DontCopy](DontCopy.md) takes priority over _CopyAlways_, and _CopyAlways_ takes priority over [CopyEmpty](CopyEmpty.md). [CopyNewer](CopyNewer.md) is separate: it can refresh an existing sandbox copy, whereas _CopyAlways_ selects how the initial migration is performed.

Please note the following limitations:

- The rule is consulted for an existing regular host file only when its contents would otherwise be migrated. It does not refresh an existing sandbox copy and does not govern new files, directories, or create/overwrite operations that do not copy host contents.
- The rule overrides the migration-size decision, but it cannot guarantee that inaccessible host contents can be read. The rule does not bypass host-file access restrictions. If Sandboxie cannot access the source file as required for migration, the migration may fail or proceed without copying its contents.
- The host file is not modified; subsequent writes are made to the sandbox copy.

Copy rules can be managed in SandMan under Sandbox Options > General Options > File Migration. Choose **Always copy** for this rule type.

Related [Sandboxie Ini](SandboxieIni.md) settings: [DontCopy](DontCopy.md), [CopyEmpty](CopyEmpty.md), [CopyNewer](CopyNewer.md), [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md). See also [File Migration Settings](FileMigrationSettings.md).
