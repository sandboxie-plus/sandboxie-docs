# Leader Process

_LeaderProcess_ is a repeatable per-box setting in [Sandboxie Ini](SandboxieIni.md). It identifies executable images that Sandboxie should treat collectively as the primary programs in a sandbox.

```ini
[DefaultBox]
LeaderProcess=browser.exe
LeaderProcess=viewer.exe
```

Names are matched exactly and case-insensitively. The current consumer does not perform wildcard matching.

Configured leaders must first have been observed running. After one or more configured leaders have been present, Sandboxie requests termination of the remaining sandboxed processes when none of the configured leader images remains. With the example above, `browser.exe` exiting does not trigger cleanup while `viewer.exe` is still running.

Leader-triggered cleanup bypasses the linger-specific window exemption, leniency exemptions, and recent-process grace check. It does not take effect merely because a leader name is configured before any matching process has been observed.

The list is loaded when SandboxieRpcSs initializes inside the sandbox. Restart or recreate the affected sandbox process tree after changing it for predictable behavior.

In Sandboxie Plus, open **Sandbox Options > Program Control > Stop Behaviour > Leader Programs**. Sandboxie Control Classic exposes the historical [Sandbox Settings > Program Stop > Leader Programs](ProgramStopSettings.md#leader-programs) page.

See [Program Stop Settings](ProgramStopSettings.md) for the complete lifecycle overview.
