# Prompt For File Migration

PromptForFileMigration is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls whether Sandboxie requests an interactive decision when the normal content-migration decision reaches or exceeds a finite [CopyLimitKb](CopyLimitKb.md) threshold and no explicit migration rule has already selected a mode. For more information, see [SBIE2102](SBIE2102.md).

The consumer fallback is `y` when no effective value is configured. An effective value can also come from applicable enabled templates or `[GlobalSettings]` fallback.

```
   .
   .
   .
   [DefaultBox]
   PromptForFileMigration=n
```

Specifying _n_ disables the interactive request. With prompting enabled, SandMan can display the request, but an available interactive consumer and a usable reply are not guaranteed. An affirmative answer selects full-content migration for that attempt, not guaranteed copy success. A negative answer, disabled prompting, or no usable reply selects the non-copy path.

For the initial migration-dependent open, [CopyBlockDenyWrite](CopyBlockDenyWrite.md) then determines denial versus a host-open retry with write and delete access removed. The retry can itself fail; disabling prompting does not guarantee read-only access. An explicit **No** reply does not produce SBIE2102 from this decision path; [CopyLimitSilent](CopyLimitSilent.md) controls that message when no usable reply is returned.

SandMan offers **Remember for this process**. A remembered answer applies to later migration requests for that process, not just the same file. It is process-local UI state, not a permanent INI exception or a change to _CopyLimitKb_.

Related Sandboxie Plus setting: Sandbox Options > General Options > File Migration > **Prompt user for large file migration**. Sandboxie Control Classic does not provide the equivalent interactive migration-prompt consumer.

## Applying changes

Unlike the cached size limit and silent flag, this setting is queried at each qualifying oversized migration decision. After effective configuration is reloaded, later decisions in an already-running process can use the changed value. A request already in progress is not changed retroactively.

Related [Sandboxie Ini](SandboxieIni.md) setting: [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md)
