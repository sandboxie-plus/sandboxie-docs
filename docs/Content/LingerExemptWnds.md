# Linger Exempt Wnds

_LingerExemptWnds_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.13.4 / 5.68.4. To make the lingering process monitor mechanism no longer exempt lingering processes with windows from termination. For example:

```
   .
   .
   .
   [DefaultBox]
   LingerExemptWnds=n
```

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings -> Program Stop -> Lingering Programs](ProgramStopSettings.md#lingering-programs)

See also: [Program Settings](ProgramSettings.md#linger).
