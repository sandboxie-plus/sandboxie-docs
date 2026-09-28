# Open Print Spooler

_OpenPrintSpooler_ controls Sandboxie's selective filter for messages sent to the Windows Print Spooler. If no effective value is configured, it defaults to `n`.

```
   .
   .
   .
   [DefaultBox]
   OpenPrintSpooler=n
```

With `OpenPrintSpooler=n`, the filter remains active and denies selected spooler RPC-message operations, including some printer-management operations. It does not block every printer-configuration or installation operation, and it does not by itself guarantee that normal printing will succeed.

Setting `OpenPrintSpooler=y` skips this specific message filter. It does not override [ClosePrintSpooler](ClosePrintSpooler.md), which controls new endpoint-resolution requests, or bypass other IPC restrictions, Windows permissions, or the separate [print-to-file file-open guard](AllowSpoolerPrintToFile.md).

The effective value is loaded when a sandboxed process initializes its IPC state. Restart affected sandboxed processes after changing the setting to ensure they use the new value.

In SandMan, the control is **Sandbox Options > General Options > Restrictions > Printing restrictions > Remove spooler restriction, printers can be installed outside the sandbox**. It is disabled when **Block access to the printer spooler** is checked or in Application Compartment. The checkbox reflects the direct box value, while the runtime can also use applicable template or global configuration. Sandboxie Control Classic does not provide the equivalent active settings page; the option can be configured in `Sandboxie.ini`.

Added as part of 0.5.4 / 5.46.0 version.

_See also [ClosePrintSpooler](ClosePrintSpooler.md)_.
