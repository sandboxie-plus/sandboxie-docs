# Allow Spooler Print To File

`AllowSpoolerPrintToFile` controls a special file-open guard for the Windows Print Spooler service, `spoolsv.exe`, when it acts on behalf of a sandboxed process. If no effective value is configured, it defaults to `n`.

```
   .
   .
   .
   [DefaultBox]
   AllowSpoolerPrintToFile=n
```

With `AllowSpoolerPrintToFile=n`, Sandboxie checks applicable write-access file opens by the host `spoolsv.exe` against the originating sandboxed process's normal file-access policy. The guard has exceptions, including the sandbox's spooler work directory, and does not block every `CreateFile` call or every print job. Normal file-access rules can affect whether a destination is allowed.

With `AllowSpoolerPrintToFile=y`, this special guard is skipped for the associated sandboxed process. This does not give `spoolsv.exe` unrestricted access to the host filesystem; Windows permissions and other controls still apply.

An applicable denial can produce **SBIE1319**. For a process that is still running, SandMan can ask whether to allow the spooler to write outside the sandbox for that process. Choosing **Yes** grants a temporary exception for that process ID and future matching file opens. It does not change `Sandboxie.ini`, set `AllowSpoolerPrintToFile=y`, or retry the file open that already failed. The exception ends when that process exits. In Sandboxie Control Classic, **SBIE1319** is followed by **SBIE1320**; double-clicking the latter grants the same process-specific exception.

The persistent setting is loaded when the sandboxed process initializes its IPC state. Restart affected sandboxed processes after changing it to ensure they use the new value. In SandMan, the control is **Sandbox Options > General Options > Restrictions > Printing restrictions > Allow the print spooler to print to files outside the sandbox**. It is disabled when **Block access to the printer spooler** or **Disable Security Filtering (not recommended)** is checked, but not solely because the box uses Application Compartment. In an Application Compartment with `NoSecurityFiltering=y`, the normal file-policy check used by this guard no longer provides its usual denial. The checkbox reflects the direct box value, while the runtime can also use applicable template or global configuration.

[ClosePrintSpooler](ClosePrintSpooler.md) instead controls new spooler endpoint-resolution requests; [OpenPrintSpooler](OpenPrintSpooler.md) controls a separate, selective message filter.
