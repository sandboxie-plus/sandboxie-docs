# Linger Exempt Wnds

_LingerExemptWnds_ is a per-box Boolean setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.13.4 / Classic 5.68.4. It defaults to `y`.

```ini
[DefaultBox]
LingerExemptWnds=n
```

When automatic linger cleanup would otherwise occur, `LingerExemptWnds=y` prevents that cleanup while a remaining sandbox process has a visible top-level window. Setting it to `n` removes the visible-window exemption.

This setting does not make a process a lingerer and does not independently trigger termination. [Linger Process](LingerProcess.md) identifies configured linger candidates, while `LingerLeniency` controls separate startup and grace-period exemptions.

Sandboxie Plus exposes the setting under **Sandbox Options > Program Control > Stop Behaviour > Stop Options** as **Don't stop lingering processes with windows**. The checkbox is selected for the default `y` behavior.

The value is read during linger-cleanup evaluation. For predictable behavior after changing related leader, linger, or leniency policy, restart or recreate the affected sandbox process tree.

See [Program Stop Settings](ProgramStopSettings.md) for the complete lifecycle overview.
