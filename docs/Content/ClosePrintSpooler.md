# Close Print Spooler

_ClosePrintSpooler_ controls Sandboxie's mediated path for resolving the Windows Print Spooler endpoint. If no effective value is configured, it defaults to `n`.

```
   .
   .
   .
   [DefaultBox]
   ClosePrintSpooler=n
```

With `ClosePrintSpooler=y`, Sandboxie rejects new spooler endpoint-resolution requests through this path. This normally prevents printing that depends on obtaining that endpoint, but does not stop the Windows Print Spooler service or revoke an endpoint, binding, or handle already obtained.

The service checks the effective value for each new endpoint request. After reloading a changed configuration, later endpoint-resolution requests can use the new value.

In SandMan, this is **Sandbox Options > General Options > Restrictions > Printing restrictions > Block access to the printer spooler**. The checkbox is disabled for Application Compartment boxes. It reflects the direct box value, while the runtime can also use applicable template or global configuration. Sandboxie Control Classic does not provide the equivalent active settings page; the option can be configured in `Sandboxie.ini`.

Added as part of 0.5.4 / 5.46.0 version.

## Interaction with [OpenPrintSpooler](OpenPrintSpooler.md)

```
   .
   .
   .
   [DefaultBox]
   ClosePrintSpooler=n
   OpenPrintSpooler=n
```

With both settings at `n`, _ClosePrintSpooler_ does not deny new endpoint-resolution requests, while _OpenPrintSpooler_ keeps Sandboxie's selective spooler RPC-message filter active. The filter denies selected operations, not every printer-configuration operation, and does not guarantee that printing will succeed. Setting `OpenPrintSpooler=y` skips that specific filter but does not override `ClosePrintSpooler=y`.

The separate [AllowSpoolerPrintToFile](AllowSpoolerPrintToFile.md) setting concerns file opens by the host spooler on behalf of sandboxed processes.
