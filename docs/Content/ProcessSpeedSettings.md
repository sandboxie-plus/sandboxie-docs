# Process Speed Settings

Process speed settings are sandbox settings in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.14.0. They adjust selected Windows timing, sleep, and timer APIs inside sandboxed processes. They do not change the Windows system clock or provide complete time virtualization for a sandbox.

## Enabling Process Speed Changes

Enable the feature for a sandbox with:

```ini
[DefaultBox]
UseChangeSpeed=y
```

`UseChangeSpeed=y` enables installation of the applicable timing hooks during their initialization. Its runtime fallback is disabled (`n`). A value can come from the sandbox section, applicable enabled templates, or `[GlobalSettings]`; absence from the direct sandbox section does not necessarily disable the feature. When no effective value enables it, the corresponding hooks are not installed.

Use small positive decimal integer factors. All six factors have a consumer fallback of `1`, the normal neutral value. Ordinary literal `0` values also resolve to that fallback; `AddSleepSpeed=0` is not an instruction to skip sleep calls, and zero should not be used to disable the feature.

## Affected APIs

The settings apply only to the API groups listed below.

### Tick and Clock Functions

`AddTickSpeed` and `LowTickSpeed` control:

- `GetTickCount`
- `GetTickCount64`
- `QueryUnbiasedInterruptTime`
- `QueryPerformanceCounter`

For small positive values within arithmetic limits, most listed clocks scale approximately by `AddTickSpeed / LowTickSpeed`, but their calculations differ. `GetTickCount` scales elapsed values relative to a native reference captured when its hook is installed. `GetTickCount64` and `QueryPerformanceCounter` scale absolute native values. The feature does not install a corresponding `QueryPerformanceFrequency` hook.

In the current implementation, `QueryUnbiasedInterruptTime` divides the integer factors before scaling its result. Unlike the other listed clocks, fractional ratios below one can therefore produce zero rather than a proportionally slower clock; a ratio such as `3/2` is truncated to `1`. This is a current implementation limitation, not a consistent fractional-scaling contract. See the [current clock wrappers](https://github.com/sandboxie-plus/Sandboxie/blob/31ba1e5c1aaaf3c98248a8994aecc9d016b7a310/Sandboxie/core/dll/kernel.c#L326-L401).

These functions represent elapsed or performance-counter time, not the system date and time. The affected timing sources are adjusted independently and should not be treated as a single precise virtual clock. Applications that compare different Windows timing sources may observe differences.

### Sleep Functions

`AddSleepSpeed` and `LowSleepSpeed` control the requested duration passed through Sandboxie's `SleepEx` hook. Sandboxie does not install a separate `Sleep` hook: ordinary `Sleep` calls are affected only where their actual Windows execution path reaches the intercepted `SleepEx` implementation.

For ordinary positive values within arithmetic limits, the forwarded duration is approximately `requested duration * LowSleepSpeed / AddSleepSpeed`. Shorter requested delays can allow execution to progress faster. With the other factor left at `1`:

- `AddSleepSpeed=2` forwards a requested 1000 ms sleep as 500 ms.
- `LowSleepSpeed=2` forwards a requested 1000 ms sleep as 2000 ms.

These are requested intervals, not guarantees of exact elapsed time. The conversion multiplies in 32-bit unsigned arithmetic before division: large values can overflow, very small results can truncate to zero, and arbitrary scaling need not preserve special timeout values such as `INFINITE`.

This does not modify synchronization waits such as `WaitForSingleObject`. Actual elapsed time remains subject to normal Windows scheduling, timer-resolution behavior, and alertable sleep semantics.

### Timer Functions

`AddTimerSpeed` and `LowTimerSpeed` control:

- `SetTimer`
- `timeGetTime`
- `timeSetEvent`

In the current implementation, `timeGetTime` belongs to the Timer factor group, not the Tick factor group. It adjusts a returned clock value using its own native reference captured when its hook is installed, separate from `GetTickCount`; it does not change timer intervals.

For ordinary positive factors within arithmetic limits, `SetTimer` and `timeSetEvent` adjust requested intervals approximately by `LowTimerSpeed / AddTimerSpeed`. The `timeGetTime` clock uses the corresponding `AddTimerSpeed / LowTimerSpeed` relationship. With the other factor at `1`:

- `AddTimerSpeed=2` approximately halves requested timer intervals and makes `timeGetTime` progress approximately twice as fast.
- `LowTimerSpeed=2` approximately doubles requested timer intervals and makes `timeGetTime` progress approximately half as fast.

The interval wrappers use 64-bit intermediate arithmetic, then convert back to the native interval type; large transformed values can narrow or wrap. Windows timer minimums, supported ranges, resolution, message processing, and scheduling still apply, so actual callback or message delivery times may differ from the calculated interval. Timer-hook installation also has additional GUI conditions described under Runtime Scope.

## Factor Comparison

| Setting | Controls | Value `2` |
| ------- | -------- | --------- |
| `AddTickSpeed` | Supported tick/clock sources | About 2x faster, subject to clock limitations above |
| `LowTickSpeed` | Supported tick/clock sources | About 2x slower, except `QueryUnbiasedInterruptTime`, which produces zero |
| `AddSleepSpeed` | `SleepEx` requested duration | 1000 ms forwarded as 500 ms |
| `LowSleepSpeed` | `SleepEx` requested duration | 1000 ms forwarded as 2000 ms |
| `AddTimerSpeed` | Supported timer APIs | Requested intervals about halved; `timeGetTime` faster |
| `LowTimerSpeed` | Supported timer APIs | Requested intervals about doubled; `timeGetTime` slower |

The other factor in each pair is assumed to be `1`. These are request conversions or approximate clock relationships, subject to the limitations described above.

## Example

```ini
[DefaultBox]
UseChangeSpeed=y
AddTickSpeed=2
AddSleepSpeed=2
AddTimerSpeed=2
```

With the applicable hooks installed and values within arithmetic limits, this configuration generally causes:

- the affected tick and clock sources to progress approximately twice as fast, without making them one consistent clock;
- a requested 1000 ms sleep to be forwarded as 500 ms;
- requested timer intervals to be reduced approximately by half;
- `timeGetTime` to progress approximately twice as fast.

## Combining Add and Low Factors

The Add and Low variants for the same group may be configured together. Neither setting overrides the other. For example:

```ini
[DefaultBox]
UseChangeSpeed=y
AddTickSpeed=2
LowTickSpeed=3
```

Within arithmetic limits, this applies approximately `2/3` scaling to `GetTickCount`, `GetTickCount64`, and `QueryPerformanceCounter`, using their different reference points. `QueryUnbiasedInterruptTime` instead divides `2` by `3` first and produces zero. Add and Low values therefore combine according to the intercepted API, not one uniform formula. Tick, Sleep, and Timer factor groups remain independent, so changing one group does not automatically configure the others.

## Runtime Scope

The applicable hooks run inside sandboxed processes through Sandboxie's injected DLL. Installation depends on effective configuration, the initialization path, API/module availability, successful hooking, and applicable hook-suppression settings; not every process receives every hook. This is not a system-wide change to the Windows clock. SandMan and the Sandboxie services are not normally affected in unsandboxed operation.

The Timer hooks additionally depend on GUI initialization. Their installation block is skipped in Application Compartment and with effective `NoSandboxieDesktop=y`; the Tick/Clock and `SleepEx` hooks do not share this GUI condition.

`UseChangeSpeed` is read by the relevant initializer. Reloading configuration does not replay completed initializers or retroactively install or remove timing hooks. Restart affected sandboxed applications to reliably change hook installation. A GUI initializer that has not yet run may read a newly effective value later; that is deferred initialization, not reinstallation caused by reload.

All six numeric factors are queried during the corresponding hook invocations, so successfully reloaded values can affect installed hooks. Factor pairs are read separately, updates are not atomic across timing sources, and retained initialization references mean changes can cause clock discontinuities. Interval changes apply to subsequent intercepted calls; changing the factors alone does not reprogram existing timers. Saving a file alone does not establish successful configuration reload. Ordinary updates do not inherently require restarting Sandboxie services, the driver, or Windows.

## Intended Use

The feature is intended for scenarios such as reducing fixed application delays during analysis or testing and modifying logical speed for compatible single-player applications or games. Compatibility depends on which Windows timing mechanisms an application uses. It does not accelerate CPU execution or increase processor frequency, and it does not guarantee faster application execution or game compatibility.

## Limitations

- The feature does not intercept every Windows time source or wait mechanism. System wall-clock APIs, `NtQuerySystemTime`, `NtDelayExecution`, synchronization waits, waitable timers, timer queues, and threadpool timers are not covered.
- Because only selected APIs are adjusted, applications that compare multiple timing sources may observe inconsistent elapsed times.
- Synchronization waits are not generally shortened or extended by the Sleep factors.
- Changing timing behavior can affect application logic, responsiveness, media handling, or timeout assumptions.
- Use small positive integer factors. Integer rounding, arithmetic limits, native timer constraints, and application timing assumptions can produce unexpected results, especially with large factors or very short intervals. Equal Add/Low factors are not universally protected against intermediate overflow.

There is currently no dedicated graphical control for these settings. In SandMan, use **Sandbox Options > Edit ini Section > Edit ini**. In Sandboxie Control Classic, use **Configure > Edit Configuration**. Plus and Classic share the relevant runtime code where applicable; manual configuration does not guarantee hook installation or a particular timing result.

Related: [Sandboxie Ini](SandboxieIni.md).
