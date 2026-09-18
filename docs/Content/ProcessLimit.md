# Process Limit

_ProcessLimit_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.9.7 / 5.52.1. This setting allows you to limit the maximum number of processes that Sandboxie will allow in the sandbox at the same time.

**Note:** The start of new processes is delayed for 3 seconds when 80% of the set limit is reached. Once the limit is reached, no new process will be allowed to start (until another process is killed).

_ProcessLimit_ is separate from [ProcessNumberLimit](ProcessNumberLimit.md). _ProcessLimit_ is enforced by Sandboxie's process initialization logic, while _ProcessNumberLimit_ uses the Windows Job Object active-process limit.

```
   .
   .
   .
   [DefaultBox]
   ProcessLimit=100
```
