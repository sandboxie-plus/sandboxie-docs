# CPU Rate Limit

_CpuRateLimit_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.17.5. It configures an integer CPU-rate percentage from 1 through 100 for the Sandboxie Job Object.

## Usage

```ini
[DefaultBox]
CpuRateLimit=25
```

## Syntax

```ini
CpuRateLimit=1-100
```

In this example, Sandboxie configures a 25% hard CPU-rate cap for the Job Object. Internally, the value is passed to Windows as `CpuRate = 2500` because Windows represents the rate as the percentage multiplied by 100. Users should configure the percentage directly; `25` means 25% and `100` means 100%.

## Collective CPU Limit

The limit applies collectively to all processes assigned to the same Sandboxie Job Object. If several sandboxed processes consume CPU simultaneously, they share one CPU-rate budget; each process does not receive a separate 25% quota.

When the Sandboxie Job has no parent Job with CPU-rate control, the percentage represents a portion of the processor-cycle capacity of the entire system. If it is nested under a parent that also has CPU-rate control, Windows calculates its rate relative to the immediate parent's allocation.

Sandboxie enables the Windows `JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP` policy. When the Job consumes its permitted processor cycles for a scheduling interval, Windows stops scheduling its threads until the next interval. This throttles the processes rather than terminating them and is not a processor-affinity restriction. The underlying Windows mechanism is available starting with Windows 8 and Windows Server 2012.

## Job Object Requirements

_CpuRateLimit_ affects only processes assigned to Sandboxie's Job Object. Sandboxie skips that assignment for affected processes when `NoAddProcessToJob=y`, [`NoSecurityIsolation=y`](NoSecurityIsolation.md), or [`OpenWinClass=*`](OpenWinClass.md) is configured. `AllowBoxedJobs=y` does not itself disable the Sandboxie CPU-rate limit.

The rate is configured when Sandboxie creates its Job Object. If that Job still has active processes, Sandboxie reuses it, so a configuration change may not take effect until the current Job is no longer in use and a new one is created.

In SandMan, this setting is available under **Sandbox Options > Security Options > Job Object** as **Total CPU Rate Limit (%)**. The field accepts values from 1 through 100 and shows `unlimited` when the setting is not configured.

_CpuRateLimit_ controls how much aggregate processor scheduling capacity the Job Object may consume. To restrict where sandboxed processes may execute, see [CPU Affinity Mask](CpuAffinityMask.md). The two settings can be used together; the percentage is not recalculated solely from the processors selected by the affinity mask.
