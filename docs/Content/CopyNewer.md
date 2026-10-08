# Copy Newer

_CopyNewer_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.18.1. It specifies a list of file path patterns for which an existing sandbox copy of a file is refreshed when the matching file on the host has been modified more recently.

Usage:

```
   .
   .
   .
   [DefaultBox]
   CopyNewer=C:\Data\*.txt
```

Normally, once a file has been copied into the sandbox (see [File Migration Settings](FileMigrationSettings.md)), a sandboxed program keeps using that copy even if the original file on the host is changed later. When a file path matches a _CopyNewer_ pattern, Sandboxie compares the last-write time of the host file with the sandboxed copy on eligible opens; if the host file is newer, a refresh is attempted before the open completes.

The refresh migration uses the same migration rules, size limit, prompt behavior, and notifications as initial content migration. A matching [DontCopy](DontCopy.md) rule can prevent the refresh, [CopyAlways](CopyAlways.md) can select full-content migration before the size limit and prompt, and [CopyEmpty](CopyEmpty.md) can select an empty replacement. These rules do not themselves trigger the refresh. [CopyBlockDenyWrite](CopyBlockDenyWrite.md) can affect the refresh migration's result, but a failed refresh does not necessarily deny the subsequent open of the existing sandbox copy.

Please note the following limitations:

- It only applies to regular files that already have a copy inside the sandbox, when they are opened normally.
- It does not apply to the initial migration of a file, to directories, to deleted files, or to create/overwrite operations. Refresh is also skipped for a write-only resource-path mode, such as [WriteFilePath](WriteFilePath.md); this is not simply a test of the application's requested access.
- Pattern matching is case-insensitive and is applied to the host (true) file path.
- If a refresh is already in progress or fails, the existing sandbox copy remains available to the program.
- A successful refresh is not necessarily a full-content replacement: a migration rule or a source-access fallback can result in empty contents.

Copy rules, including rules of type "Copy newer", can be managed in SandMan under Sandbox Options > General Options > File Migration.

Related [Sandboxie Ini](SandboxieIni.md) settings: [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md). See also [File Migration Settings](FileMigrationSettings.md).
