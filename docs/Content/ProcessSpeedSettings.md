# Process Speed Settings

Process speed settings are sandbox settings in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.14.0. They adjust selected Windows timing, sleep, and timer APIs inside sandboxed processes. They do not change the Windows system clock or provide complete time virtualization for a sandbox.

## Enabling Process Speed Changes

Enable the feature for a sandbox with:

```ini
[DefaultBox]
UseChangeSpeed=y
```

`UseChangeSpeed=y` is required for the six speed factors to have an effect. If `UseChangeSpeed` is absent or disabled, Sandboxie does not install the process-speed hooks when a sandboxed process initializes.

Use positive decimal integer factors. A value of `1` is neutral and leaves that factor unchanged.

## Affected APIs

The settings apply only to the API groups listed below.

### Tick and Clock Functions

`AddTickSpeed` and `LowTickSpeed` control:

- `GetTickCount`
- `GetTickCount64`
- `QueryUnbiasedInterruptTime`
- `QueryPerformanceCounter`

For normal positive values, the effective clock-speed relationship is approximately `AddTickSpeed / LowTickSpeed`. `AddTickSpeed` makes the affected clocks progress faster, while `LowTickSpeed` makes them progress slower.

These functions represent elapsed or performance-counter time, not the system date and time. The affected timing sources are adjusted independently and should not be treated as a single precise virtual clock. Applications that compare different Windows timing sources may observe differences.

### Sleep Functions

`AddSleepSpeed` and `LowSleepSpeed` control the requested duration passed through Sandboxie's `SleepEx` hook. Sandboxie's implementation relies on normal `Sleep` calls reaching this `SleepEx` path on Windows; it does not install a separate `Sleep` hook.

For normal positive values, the effective duration relationship is approximately `LowSleepSpeed / AddSleepSpeed`. Shorter delays allow execution to progress faster. For example:

- `AddSleepSpeed=2` changes a requested 1000 ms sleep to approximately 500 ms.
- `LowSleepSpeed=2` changes a requested 1000 ms sleep to approximately 2000 ms.

This does not modify synchronization waits such as `WaitForSingleObject`. Very small transformed durations remain subject to normal Windows scheduling and timer-resolution behavior.

### Timer Functions

`AddTimerSpeed` and `LowTimerSpeed` control:

- `SetTimer`
- `timeGetTime`
- `timeSetEvent`

In the current implementation, `timeGetTime` belongs to the Timer factor group, not the Tick factor group.

For supported timer intervals, the effective duration relationship is approximately `LowTimerSpeed / AddTimerSpeed`. The `timeGetTime` clock uses the corresponding `AddTimerSpeed / LowTimerSpeed` relationship. Therefore:

- `AddTimerSpeed=2` approximately halves supported timer intervals and makes `timeGetTime` progress approximately twice as fast.
- `LowTimerSpeed=2` approximately doubles supported timer intervals and makes `timeGetTime` progress approximately half as fast.

Windows timer minimums, resolution, message processing, and scheduling still apply, so actual callback or message delivery times may differ from the calculated interval.

## Factor Comparison

| Setting | Controls | Value `2` |
| ------- | -------- | --------- |
| `AddTickSpeed` | Supported tick/clock sources | About 2x faster |
| `LowTickSpeed` | Supported tick/clock sources | About 2x slower |
| `AddSleepSpeed` | `SleepEx` duration | 1000 ms becomes about 500 ms |
| `LowSleepSpeed` | `SleepEx` duration | 1000 ms becomes about 2000 ms |
| `AddTimerSpeed` | Supported timer APIs | Intervals about halved; `timeGetTime` faster |
| `LowTimerSpeed` | Supported timer APIs | Intervals about doubled; `timeGetTime` slower |

## Example

```ini
[DefaultBox]
UseChangeSpeed=y
AddTickSpeed=2
AddSleepSpeed=2
AddTimerSpeed=2
```

This configuration generally causes:

- the supported tick and clock sources to progress approximately twice as fast;
- a requested 1000 ms sleep to become approximately 500 ms;
- supported timer intervals to be reduced approximately by half;
- `timeGetTime` to progress approximately twice as fast.

## Combining Add and Low Factors

The Add and Low variants for the same group may be configured together. Neither setting overrides the other. For example:

```ini
[DefaultBox]
UseChangeSpeed=y
AddTickSpeed=2
LowTickSpeed=3
```

For normal clock transformations, this produces an effective ratio of approximately `2/3`. Tick, Sleep, and Timer factors are independent, so changing one group does not automatically configure the others.

## Runtime Scope

The hooks run inside each sandboxed process through Sandboxie's injected DLL. Each sandboxed process receives the hooks when it initializes; this is not a system-wide change to the Windows clock. SandMan and the Sandboxie services are not normally affected.

`UseChangeSpeed` determines whether the hooks are installed during process initialization. Changing it after a process has started does not retroactively install or remove hooks in that process. The individual numeric factors are read by the hooked paths, so a configuration change may affect a process that already has the hooks installed.

## Intended Use

The feature is intended for scenarios such as reducing fixed application delays during analysis or testing and modifying logical speed for compatible single-player applications or games. Compatibility depends on which Windows timing mechanisms an application uses.

## Limitations

- The feature does not intercept every Windows time source or wait mechanism. System wall-clock APIs, `NtQuerySystemTime`, `NtDelayExecution`, synchronization waits, waitable timers, timer queues, and threadpool timers are not covered.
- Because only selected APIs are adjusted, applications that compare multiple timing sources may observe inconsistent elapsed times.
- Synchronization waits are not generally shortened or extended by the Sleep factors.
- Changing timing behavior can affect application logic, responsiveness, media handling, or timeout assumptions.
- Large factors and very small resulting intervals can produce unusual behavior because Windows timer resolution and application assumptions still apply.

There is currently no dedicated graphical control for these settings. Configure them through the sandbox INI editor.

Related: [Sandboxie Ini](SandboxieIni.md).
