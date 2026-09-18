# Process Number Limit

_ProcessNumberLimit_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus v1.14.0. It uses a Windows Job Object to limit the number of active processes associated with the Job Object for the sandbox and session.

Syntax:

```ini
ProcessNumberLimit=<process_count>
```

Example:

```ini
[DefaultBox]
ProcessNumberLimit=50
```

In this example, up to 50 associated processes may be active at the same time. A process that would exceed the limit cannot proceed with normal sandboxed startup. Processes that are already associated remain running.

_ProcessNumberLimit_ uses the Windows Job Object active-process limit. It does not provide a dedicated Sandboxie notification when the limit is reached. If _ProcessNumberLimit_ is not configured, this specific Job Object process-count limit is not applied.

> [!IMPORTANT]
> These limits only apply to processes that are assigned to Sandboxie's Job Object. Job Object assignment is skipped for affected processes when `NoAddProcessToJob=y`, `NoSecurityIsolation=y`, or `OpenWinClass=*` applies. `AllowBoxedJobs=y` does not disable these limits.

The limits are configured when Sandboxie creates the Job Object. If the sandbox and session already have an active Job Object with running associated processes, changes may not take effect until that Job Object is no longer in use and a new one is created.

_ProcessNumberLimit_ is separate from [ProcessLimit](ProcessLimit.md). _ProcessLimit_ is enforced by Sandboxie's process initialization logic, while _ProcessNumberLimit_ uses the Windows Job Object active-process limit.

Related [Sandboxie Ini](SandboxieIni.md) settings: [TotalMemoryLimit](TotalMemoryLimit.md), [ProcessMemoryLimit](ProcessMemoryLimit.md)
