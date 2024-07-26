# Allow Spooler Print To File

`AllowSpoolerPrintToFile` is a sandbox setting that provides nuanced control over how sandboxed applications interact with the print spooler service.

```
   .
   .
   .
   [DefaultBox]
   AllowSpoolerPrintToFile=n
```

This setting can be used to prevent sandboxed applications from printing to file. By default, Sandboxie blocks all `CreateFile` calls that ask for write access for a sandboxed `spoolsv.exe`.
