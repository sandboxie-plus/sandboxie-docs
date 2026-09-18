# Copy Empty

_CopyEmpty_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 0.6.5. It specifies host-file path patterns for which Sandboxie creates a zero-length sandbox copy instead of copying the host file contents during file migration.

Usage:

`CopyEmpty=[program,]pattern`

```ini
[DefaultBox]
CopyEmpty=*\Cache\*.log
CopyEmpty=indexer.exe,*\SearchData\*.db
```

Each _CopyEmpty_ entry is one rule, and the setting may be repeated. The optional prefix before the comma limits a rule to that program; see [Program Name Prefix](ProgramNamePrefix.md). Paths use the same pattern form as [OpenFilePath](OpenFilePath.md). Matching is case-insensitive and is performed against the host (true) file path. `*` matches any sequence of characters, including path separators, and `?` matches one character.

When a program prefix is used, current setting metadata requires the drive or device portion of a path to be represented by a wildcard, for example `*\Cache\*.log`. Do not use a fixed drive path such as `C:\Cache\*.log` or rely on an [expandable variable](ExpandableVariables.md) that becomes a full path in a program-specific rule.

When a matching existing regular file needs to be migrated, Sandboxie opens the host file to obtain its file information, creates the corresponding sandbox file, and sets the content length to zero. The host file remains unchanged. The sandboxed program can then work with the empty sandbox copy and write new content to it.

The rule is selected before [CopyLimitKb](CopyLimitKb.md), so it creates an empty copy regardless of the host file's size. [CopyLimitSilent](CopyLimitSilent.md) does not affect this rule. If [NotifyNoCopy](NotifyNoCopy.md) is enabled, the migration attempt produces message SBIE2113 to report that the contents were discarded.

If _CopyEmpty_ is absent or no entry matches, Sandboxie uses another matching migration rule or its normal size-based decision. When rules overlap, [DontCopy](DontCopy.md) takes priority over [CopyAlways](CopyAlways.md), and _CopyAlways_ takes priority over _CopyEmpty_. [CopyNewer](CopyNewer.md) is evaluated separately for an existing sandbox copy; it does not change how the initial empty copy is selected.

Please note the following limitations:

- _CopyEmpty_ is consulted only when the contents of an existing regular host file would normally be migrated on a non-destructive open.
- It does not affect directories, files created only inside the sandbox, an already existing sandbox copy, or overwrite/delete/create operations for which Sandboxie does not copy the host contents.
- Sandboxie must still be able to open the host object and query its file information. Failures at that stage can make the migration fail instead of producing an empty copy.

Copy rules can be managed in SandMan under Sandbox Options > General Options > File Migration. Choose **Copy empty** for this rule type.

Related [Sandboxie Ini](SandboxieIni.md) settings: [CopyAlways](CopyAlways.md), [DontCopy](DontCopy.md), [CopyNewer](CopyNewer.md), [NotifyNoCopy](NotifyNoCopy.md), [CopyLimitKb](CopyLimitKb.md). See also [File Migration Settings](FileMigrationSettings.md).
