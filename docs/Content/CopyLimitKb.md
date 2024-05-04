# Copy Limit Kb

_CopyLimitKb_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). Existing files that are modified by sandboxed programs have to be copied into the sandbox first. This setting specifies the file size limit for this copy operation. Files larger than the limit will not be copied into the sandbox, and cannot be modified by sandboxd programs. The limit is specified in units of kilobytes (1 kilobyte = 1024 bytes).

For more information, see [SBIE2102](SBIE2102.md).

Usage:

```
   .
   .
   .
   [DefaultBox]
   CopyLimitKb=128000
```

This example specifies that only files smaller than (approx.) 128MB will be copied into the sandbox _DefaultBox_, when needed. Files larger than this limit can only be read, not updated, by sandboxed programs.

The default setting is 49152 kilobytes, or 48 megabytes. Setting _CopyLimitKb_ to some value for one sandbox does not change the default value for other sandboxes.

The size limit and alert message can be configured in [SandboxSettings > File Migration](FileMigrationSettings.md).

Related [Sandboxie Ini](SandboxieIni.md) setting: [CopyLimitSilent](CopyLimitSilent.md)
