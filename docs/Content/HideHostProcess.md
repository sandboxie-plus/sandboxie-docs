# Hide Host Process

_HideHostProcess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.3 / 5.42. It removes matching entries from process lists returned to sandboxed applications through Sandboxie's filtered native enumeration path. You can repeat the setting for multiple process names.

```
   .
   .
   .
   [DefaultBox]
   HideHostProcess=program.exe
```

The value is compared with the presented process name using an exact, case-insensitive match. Use an executable name, not a full path or wildcard pattern. The setting normally applies to entries without a sandbox association; it can also match entries whose presented name begins with `Sandboxie`, including some Sandboxie service or worker processes. It does not normally remove an ordinary process assigned to another box merely because its name matches.

In SandMan, manage the process-name list under Sandbox Options > Advanced Options > Processes > Process Hiding. The list may also show entries supplied by templates.

This setting filters a process-list result; it does not by itself deny access to a process by known PID. Other discovery paths, including WMI, are separate. See [Hide Non System Processes](HideNonSystemProcesses.md) and [Hide Other Boxes](HideOtherBoxes.md) for related list filters.
