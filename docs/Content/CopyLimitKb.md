# Copy Limit Kb

_CopyLimitKb_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls the normal size decision when Sandboxie needs to copy the contents of an existing host file into the sandbox. The limit is specified in units of kilobytes (1 kilobyte = 1024 bytes).

For more information, see [SBIE2102](SBIE2102.md).

Usage:

```
   .
   .
   .
   [DefaultBox]
   CopyLimitKb=128000
```

This example sets the threshold for _DefaultBox_ to 128000 KiB, or 125 MiB. When no overriding migration rule applies, a file strictly smaller than that threshold is selected for full-content migration. A file exactly at the threshold, or larger, enters the large-file prompt/non-copy decision.

Use `CopyLimitKb=-1` to disable the normal size threshold. Otherwise, use a sensible positive integer value.

## Migration decision

Matching [DontCopy](DontCopy.md), [CopyAlways](CopyAlways.md), and [CopyEmpty](CopyEmpty.md) rules are evaluated before the size decision, in that priority order. When none matches and a finite threshold is reached or exceeded, [PromptForFileMigration](PromptForFileMigration.md) allows SandMan to ask whether to migrate the file. An affirmative reply selects full-content migration for that attempt; it does not guarantee that the source can be read or the copy completed.

If migration is not approved, [CopyBlockDenyWrite](CopyBlockDenyWrite.md) controls the initial migration-dependent open: `y` denies it; otherwise Sandboxie retries host access after removing write and delete access. That retry can still fail because of the remaining request parameters or host permissions.

The threshold does not govern all file access. New files, ordinary access to an existing sandbox copy, direct access through [OpenFilePath](OpenFilePath.md), and operations that do not copy host contents follow separate paths. [CopyNewer](CopyNewer.md) can initiate a refresh of an existing sandbox copy; its migration attempt can use this size decision.

## Effective value and UI fallbacks

The initialized runtime consumer fallback is `-1`: if no effective value is configured, the normal size threshold is disabled. An effective value can come from the sandbox, applicable enabled templates, or `[GlobalSettings]` fallback. Setting a direct value for one sandbox does not change other sandboxes' values.

The interfaces have different display fallbacks:

- **SandMan:** 81920 KiB (80 MiB), read from the direct box setting. When the enabled size field contains `81920`, saving removes the direct `CopyLimitKb` entry rather than writing that number. Applicable inherited configuration, or the runtime `-1` fallback, can then become effective. An unchecked limit checkbox writes `-1`.
- **Sandboxie Control Classic:** 49152 KiB (48 MiB), its own File Migration UI/accessor fallback. This is not the current runtime consumer fallback.

Neither displayed fallback establishes a universal Sandboxie size limit. The size limit and alert message can be configured in [Sandbox Settings > File Migration](FileMigrationSettings.md).

## Applying changes

The limit is cached when the sandboxed process initializes its file subsystem. Start new affected sandboxed processes after changing it; reloading configuration does not replace the cached limit in an already initialized process.

Related [Sandboxie Ini](SandboxieIni.md) setting: [CopyLimitSilent](CopyLimitSilent.md)
