# Hide Other Boxes

_HideOtherBoxes_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.3 / 5.42. Its runtime fallback is `y`: entries for processes assigned to a different sandbox are removed from Sandboxie's filtered native process-list results. Entries assigned to the same box, or without a sandbox association, are not removed by this setting. To disable this specific filter:

```
   .
   .
   .
   [DefaultBox]
   HideOtherBoxes=n
```

Setting `HideOtherBoxes=n` does not guarantee that other-box processes appear through every enumeration method, nor does the setting itself control access to processes by known PID.

In SandMan, the checkbox is Sandbox Options > Advanced Options > Processes > Process Hiding > Don't allow sandboxed processes to see processes running in other boxes. Its direct box-side default is checked; an effective value inherited through configuration may differ from the direct checkbox state.

The value is read on later enumerations, so a configuration reload can affect an already-running process if the `NtQuerySystemInformation` hook was installed for it. See [Hide Non System Processes](HideNonSystemProcesses.md) for the hook and WMI limitations.
