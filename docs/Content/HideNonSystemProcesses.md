# Hide Non System Processes

_HideNonSystemProcesses_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). Its runtime fallback is `n`.

```
   .
   .
   .
   [DefaultBox]
   HideNonSystemProcesses=y
```

With `HideNonSystemProcesses=y`, Sandboxie removes many entries not associated with a sandbox from its filtered native process-list results.

> [!CAUTION]
> The system and service SID exceptions do not protect entries without a sandbox association, because the query API used by sandboxed callers does not return a SID for those targets. Legitimate system or service processes may therefore also be hidden.

The setting does not prevent discovery through every mechanism or deny access to a process by known PID. WMI is a separate path that may expose process information; SandMan provides a separate WMI-blocking option, without making this setting a general WMI filter.

In SandMan, the checkbox is Sandbox Options > Advanced Options > Processes > Process Hiding > Don't allow sandboxed processes to see processes running outside any boxes. Its direct box-side default is unchecked; an effective value inherited through configuration may differ from the direct checkbox state.

The value is read on later enumerations, so a configuration reload can affect an already-running process if the `NtQuerySystemInformation` hook was installed for it. If that hook was skipped at process initialization through [SkipHook](SkipHook.md) (`ntqsi`), changing this value does not install it retroactively.

Related [Sandboxie Ini](SandboxieIni.md) settings: [Hide Host Process](HideHostProcess.md), [Hide Other Boxes](HideOtherBoxes.md), and [Hide Sandboxie Processes](HideSbieProcesses.md).
