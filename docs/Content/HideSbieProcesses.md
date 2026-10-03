# Hide Sandboxie Processes

_HideSbieProcesses_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). Its runtime fallback is `n`.

```
   .
   .
   .
   [DefaultBox]
   HideSbieProcesses=y
```

With `HideSbieProcesses=y`, Sandboxie removes entries whose presented process name begins with `Sandboxie` or `Sbie` (case-insensitively) from its filtered native process-list results. `SbieSvc.exe` and `SandboxieRpcSs.exe` are examples, not an exhaustive list. The name-prefix test does not verify product identity: another executable with a matching prefix can qualify, while names without those prefixes are not removed by this setting.

This box setting is different from SandMan's global **Hide Sandboxie's own processes from the task list** preference (`Options/HideSbieProcesses`). The global preference affects SandMan's own task tree and can be configured independently; it is not a checkbox for this sandbox setting. No dedicated box-options checkbox for this setting is available in the current SandMan interface, but it can be configured in the INI file.

The value is read on later enumerations, so a configuration reload can affect an already-running process if the `NtQuerySystemInformation` hook was installed for it. See [Hide Non System Processes](HideNonSystemProcesses.md) for the hook and WMI limitations.

Related [Sandboxie Ini](SandboxieIni.md) settings: [Hide Host Process](HideHostProcess.md) and [Hide Non System Processes](HideNonSystemProcesses.md).
