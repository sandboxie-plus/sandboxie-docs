# Open Print Spooler

_OpenPrintSpooler_ is a sandbox setting that provides nuanced control over how sandboxed applications interact with the print spooler service.

```
   .
   .
   .
   [DefaultBox]
   OpenPrintSpooler=n
```

This setting prevents sandboxed applications from setting up printers outside the sandbox.

The filter can be disabled by setting `OpenPrintSpooler=y`.

Added as part of 0.5.4 / 5.46.0 version.

_See also [ClosePrintSpooler](ClosePrintSpooler.md)_.
