# Don't Copy

_DontCopy_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 0.6.5. It specifies host-file path patterns whose contents must not be migrated into the sandbox.

Usage:

`DontCopy=[program,]pattern`

```ini
[DefaultBox]
DontCopy=*.iso
DontCopy=media-player.exe,*\Media\*.mkv
```

Each _DontCopy_ entry is one rule, and the setting may be repeated. The optional prefix before the comma limits a rule to that program; see [Program Name Prefix](ProgramNamePrefix.md). Paths use the same pattern form as [OpenFilePath](OpenFilePath.md). Matching is case-insensitive and is performed against the host (true) file path. `*` matches any sequence of characters, including path separators, and `?` matches one character.

When a program prefix is used, current setting metadata requires the drive or device portion of a path to be represented by a wildcard, for example `*\Media\*.mkv`. Do not use a fixed drive path such as `D:\Media\*.mkv` or rely on an [expandable variable](ExpandableVariables.md) that becomes a full path in a program-specific rule.

Ordinary read-only access to a host file does not require migration and continues to use the host file. The rule matters when a sandboxed program requests an operation for which Sandboxie would normally migrate the existing file so that it can be changed in the sandbox. For a matching file, Sandboxie does not create that content copy:

- With [CopyBlockDenyWrite](CopyBlockDenyWrite.md) absent or set to `n`, Sandboxie removes write and delete rights from the request and retries the open against the host file. A read-capable request can therefore succeed as read-only. A write-only request, an incompatible create disposition, or host permissions may still make the open fail.
- With _CopyBlockDenyWrite=y_ for the program, the migration-dependent open fails with access denied instead.

_DontCopy_ is not direct-access permission like [OpenFilePath](OpenFilePath.md): it never permits the sandboxed program to write to the host file. If a sandbox copy already exists, this migration rule is not consulted and does not remove or replace that copy.

If _DontCopy_ is absent or no entry matches, it does not suppress migration; Sandboxie uses another matching migration rule or its normal size-based decision.

_DontCopy_ is evaluated before [CopyLimitKb](CopyLimitKb.md), so the file size and [CopyLimitSilent](CopyLimitSilent.md) do not change the selected rule. It also has priority over matching [CopyAlways](CopyAlways.md) and [CopyEmpty](CopyEmpty.md) entries. [CopyNewer](CopyNewer.md) concerns an already existing sandbox copy and is not part of this initial migration decision.

Please note that the rule is consulted only for an existing regular host file when its contents would otherwise be migrated. It does not govern directories, new files, or create/overwrite/delete operations for which Sandboxie does not need to copy the host contents.

If [NotifyNoCopy](NotifyNoCopy.md) is enabled, a matching migration attempt produces SBIE2115 when Sandboxie uses the read-only fallback, or SBIE2114 when _CopyBlockDenyWrite_ makes it deny access.

Copy rules can be managed in SandMan under Sandbox Options > General Options > File Migration. Choose **Don't copy** for this rule type.

Related [Sandboxie Ini](SandboxieIni.md) settings: [CopyAlways](CopyAlways.md), [CopyEmpty](CopyEmpty.md), [CopyNewer](CopyNewer.md), [CopyBlockDenyWrite](CopyBlockDenyWrite.md), [NotifyNoCopy](NotifyNoCopy.md). See also [File Migration Settings](FileMigrationSettings.md).
