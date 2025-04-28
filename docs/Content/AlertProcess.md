# Alert Process

_AlertProcess_ is a global setting in [Sandboxie Ini](SandboxieIni.md). It specifies names of programs that, if started outside the sandbox, will cause Sandboxie to issue message [SBIE1301](SBIE1301.md).

Usage:
```
   .
   .
   .
   [GlobalSettings]
   AlertProcess=iexplore.exe
   AlertProcess=firefox.exe
```

Related [Sandboxie Control](SandboxieControl.md) settings:
* [Program Settings](ProgramSettings.md)
* [Configure Menu > Alert Programs](ConfigureMenu.md#program-alerts)

Related Sandboxie Plus setting:
* Options menu > Global Settings > Program Control > Program Alerts

See also: [Alert Folder](AlertFolder.md).
