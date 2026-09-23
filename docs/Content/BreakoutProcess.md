# Breakout Process

_BreakoutProcess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.0.8 / Classic 5.55.8. It identifies an executable that may leave the current sandbox when a sandboxed process tries to start it.

```ini
[DefaultBox]
BreakoutProcess=viewer.exe
```

The value is the executable's **basename**, such as `viewer.exe`. Matching is an exact, case-insensitive comparison. The current breakout implementation does not interpret `*` or `?` as wildcards for this setting, and a full executable path is not supported as its value. SandMan's executable picker also stores the basename.

## Host executable requirement

The service accepts a matching `BreakoutProcess` launch only if it can open and resolve the target executable as a host file outside the source sandbox's file root. An executable that resolves inside that root, a network/MUP path, or a target that cannot be opened or resolved does not pass this breakout check. This host-file validation is specific to `BreakoutProcess`; do not assume it applies to [Breakout Folder](BreakoutFolder.md).

## Interaction with forced programs

Breakout does not guarantee an unsandboxed destination. After accepting the breakout rule, the service can find a matching [Force Process](ForceProcess.md) or [Force Folder](ForceFolder.md) rule in another enabled box and create the process there. If its check resolves back to the source box, the launch follows the normal sandboxed process-creation path instead. Do not rely on a fixed priority when multiple boxes could capture the process.

This setting affects future process launches, not a process already running in the sandbox. See [Breakout Execution](BreakoutExecution.md) for the service validation, limited returned handles, security implications, and SandMan controls.
