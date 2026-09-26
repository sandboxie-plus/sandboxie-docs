# Breakout Folder

_BreakoutFolder_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.0.8 / Classic 5.55.8. It matches the directory portion of an executable that a sandboxed process is trying to start. It does not make arbitrary access to files in that directory unsandboxed.

```ini
[DefaultBox]
BreakoutFolder=C:\Example
BreakoutFolder=C:\OtherApp\*
BreakoutFolder=C:\?pp\*
```

The first rule matches an executable directly in `C:\Example`, but does not automatically match its subdirectories. The second uses `*` to match executable directories below `C:\OtherApp`; it does not include executables directly in `C:\OtherApp`. Add separate rules when both the directory itself and its subdirectories should match.

`BreakoutFolder` uses case-insensitive pattern matching and supports `*` and `?`. For example, `C:\App?` can match a one-character variation of an executable directory name. The combined `C:\?pp\*` example matches directories below a name such as `App`, but not an executable directly in `C:\App`. Match the directory string deliberately: a trailing `\` is not interchangeable with the directory name without that slash. A bare drive-root entry such as `E:\` is not a rule for the entire drive.

For a shortcut launch, the relevant directory is that of the executable actually selected for the new process, not merely the directory containing the shortcut. A shortcut in `C:\Example` pointing to `C:\Tools\viewer.exe` does not match `BreakoutFolder=C:\Example` just because of the shortcut's location. A matching launch may still be captured by another enabled sandbox's [Force Process](ForceProcess.md) or [Force Folder](ForceFolder.md) rule; breakout does not guarantee an unsandboxed destination.

This setting affects future process launches, not existing processes or general file access. See [Breakout Execution](BreakoutExecution.md) for the service validation, security implications, and SandMan controls. Unlike [Breakout Process](BreakoutProcess.md), this rule does not use the service's separate host-file check for the executable.
