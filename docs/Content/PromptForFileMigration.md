# Prompt For File Migration

PromptForFileMigration is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies whether Sandboxie will prompt for large file migration. For more information, see [SBIE2102](SBIE2102.md).

```
   .
   .
   .
   [DefaultBox]
   PromptForFileMigration=n
```

Specifying _n_ indicates sandbox will not prompt user for file migration (the access will be read-only).

Related Sandboxie Plus setting: Sandbox Options > File Options > File Migration > Prompt user for large file migration

Related [Sandboxie Ini](SandboxieIni.md) setting: [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md)
