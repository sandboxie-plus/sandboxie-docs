# Process Memory Limit

_ProcessMemoryLimit_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus v1.14.0. It limits the committed virtual memory of each process associated with Sandboxie's Windows Job Object.

The value is specified in bytes and is applied independently to every associated process. It is not a physical memory or working-set limit.

Syntax:

```ini
ProcessMemoryLimit=<per_process_limit_in_byte>
```

Example:

```ini
[DefaultBox]
ProcessMemoryLimit=536870912
```

In this example, each associated process has a committed-memory limit of 536870912 bytes, or 512 MiB.

When an additional memory commit would exceed the per-process limit, Windows fails that allocation or commit. The process is not automatically terminated solely because the Job Object memory limit was reached. What happens next depends on how the application handles the allocation failure.

This setting can be used together with [TotalMemoryLimit](TotalMemoryLimit.md). When both are configured, each process is subject to its individual limit and all associated processes are also subject to the total limit. If _ProcessMemoryLimit_ is not configured, this specific Job Object memory limit is not applied.

> [!IMPORTANT]
> These limits only apply to processes that are assigned to Sandboxie's Job Object. Job Object assignment is skipped for affected processes when `NoAddProcessToJob=y`, `NoSecurityIsolation=y`, or `OpenWinClass=*` applies. `AllowBoxedJobs=y` does not disable these limits.

The limits are configured when Sandboxie creates the Job Object. If the sandbox and session already have an active Job Object with running associated processes, changes may not take effect until that Job Object is no longer in use and a new one is created.

Related [Sandboxie Ini](SandboxieIni.md) settings: [TotalMemoryLimit](TotalMemoryLimit.md), [ProcessNumberLimit](ProcessNumberLimit.md)
