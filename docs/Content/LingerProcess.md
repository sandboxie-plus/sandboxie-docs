# Linger Process

_LingerProcess_ is a repeatable per-box setting in [Sandboxie Ini](SandboxieIni.md). It identifies helper or background executables that Sandboxie can treat as cleanup candidates after no ordinary non-lingering program remains.

```ini
[DefaultBox]
LingerProcess=helper.exe
LingerProcess=updater.exe
```

Names are matched exactly and case-insensitively. The current consumer does not perform wildcard matching.

A matching process is not terminated immediately. Automatic cleanup is considered when all remaining relevant sandbox processes are lingerers and no applicable exemption prevents it. Sandboxie also treats some of its own service or helper processes as lingerers internally; that implementation list may change.

## Linger leniency

`LingerLeniency` is enabled by default. While enabled, it:

1. preserves matching configured lingerers already active when SandboxieRpcSs initializes;
2. exempts configured lingerers explicitly started through the relevant forced or `Start.exe` paths;
3. applies the current five-second grace check to recently started remaining processes before automatic cleanup.

```ini
[DefaultBox]
LingerLeniency=n
```

Setting it to `n` disables those behaviors. The setting is therefore broader than a timeout switch, and the five-second interval is not configurable through it. It does not support an unconditional rule that the first process in a sandbox is always exempt.

`LingerLeniency` was introduced in Sandboxie Plus 1.0.7 / Classic 5.55.7. Sandboxie Plus 1.13.4 / Classic 5.68.4 expanded `LingerLeniency=n` so it also disables the five-second grace check.

## Visible windows

[Linger Exempt Wnds](LingerExemptWnds.md) separately controls whether a visible top-level window prevents an otherwise eligible linger cleanup. It does not classify the process as a lingerer.

The linger list is loaded when SandboxieRpcSs initializes inside the sandbox. Restart or recreate the affected sandbox process tree after changing the list or leniency policy for predictable behavior.

In Sandboxie Plus, open **Sandbox Options > Program Control > Stop Behaviour > Lingering Programs**. `LingerLeniency` and the visible-window exemption are under **Stop Options**. Sandboxie Control Classic exposes the historical [Sandbox Settings > Program Stop > Lingering Programs](ProgramStopSettings.md#lingering-programs) page, but it should not be assumed to provide every newer SandMan control.

See [Program Stop Settings](ProgramStopSettings.md) for the complete lifecycle overview.
