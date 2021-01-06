# Leader Process

_LeaderProcess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies names of programs that are considered primary in the sandbox, and when they stop running, all other programs in the sandbox are stopped as well. For example:
```
   .
   .
   .
   [DefaultBox]
   LeaderProcess=iexplore.exe
```

_iexplore.exe_ is Internet Explorer.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings -> Program Stop -> Leader Programs](ProgramStopSettings#leader)

See also: [Program Settings](ProgramSettings#leader).
