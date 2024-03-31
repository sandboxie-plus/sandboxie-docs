# Close Print Spooler

_ClosePrintSpooler_ is a sandbox setting that provided nuanced control over how sandboxed applications interact with the print spooler service.

```ini
[DefaultBox]
ClosePrintSpooler=n
```

This setting can be used to prevent sandboxed applications from interacting with the print spooler service. When set to `y`, sandboxed applications will be unable to interact with the print spooler service - for example, print.

Added as part of [0.5.4 / 5.46.0 version](https://github.com/sandboxie-plus/Sandboxie/blob/f3ab6a73a13a74f894b2d5ceb47ab69ee0581c97/CHANGELOG.md#054--5460---2021-01-06).

## Interaction with [OpenPrintSpooler](OpenPrintSpooler.md)

```ini
[DefaultBox]
ClosePrintSpooler=n
OpenPrintSpooler=n
```

When both settings are configured as shown above, the sandboxed applications' requests to the print spooler are selectively filtered. This means that certain actions related to the print spooler are permitted ("open") while others are restricted ("closed"). Specifically, this configuration allows for printing operations but restricts activities that would modify printer configurations or the installation/removal of printers on the system.
