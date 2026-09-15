# Total Memory Limit

_TotalMemoryLimit_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus v1.14.0. It limits the total committed virtual memory of the processes associated with Sandboxie's Windows Job Object for the sandbox and session.

The value is specified in bytes and is applied directly as the Job Object's total committed-memory limit. It is not a physical memory or working-set limit.

Syntax:

```ini
TotalMemoryLimit=<total_limit_in_byte>
```

Example:

```ini
[DefaultBox]
TotalMemoryLimit=1073741824
```

In this example, the total committed-memory limit is 1073741824 bytes, or 1 GiB.

When an additional memory commit would exceed the limit, Windows fails that allocation or commit. Reaching the limit does not by itself automatically terminate all sandboxed processes. What happens next depends on how the affected application handles the allocation failure.

If [ProcessMemoryLimit](ProcessMemoryLimit.md) is also configured, each process remains subject to the per-process limit as well as this total limit. If _TotalMemoryLimit_ is not configured, this specific Job Object memory limit is not applied.

> [!IMPORTANT]
> These limits only apply to processes that are assigned to Sandboxie's Job Object. Job Object assignment is skipped for affected processes when `NoAddProcessToJob=y`, `NoSecurityIsolation=y`, or `OpenWinClass=*` applies. `AllowBoxedJobs=y` does not disable these limits.

The limits are configured when Sandboxie creates the Job Object. If the sandbox and session already have an active Job Object with running associated processes, changes may not take effect until that Job Object is no longer in use and a new one is created.

Related [Sandboxie Ini](SandboxieIni.md) settings: [ProcessMemoryLimit](ProcessMemoryLimit.md), [ProcessNumberLimit](ProcessNumberLimit.md)
