# Open Print Spooler

_OpenPrintSpooler_ is a sandbox setting that provides nuanced control over how sandboxed applications interact with the print spooler service.

```ini
[DefaultBox]
OpenPrintSpooler=n
```

This setting prevents sandboxed applications from setting up printers outside the sandbox.

The filter can be disabled by setting `OpenPrintSpooler=y`.

Added as part of [0.5.4 / 5.46.0 version](https://github.com/sandboxie-plus/Sandboxie/blob/f3ab6a73a13a74f894b2d5ceb47ab69ee0581c97/CHANGELOG.md#054--5460---2021-01-06).

_See also [ClosePrintSpooler](ClosePrintSpooler.md)_.
