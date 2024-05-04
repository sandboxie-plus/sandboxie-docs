# Alert Folder

_AlertFolder_ is a global setting in [Sandboxie Ini](SandboxieIni.md) available since v0.5.0 / 5.45.0. It specifies path patterns that, if started outside the sandbox, will cause Sandboxie to issue message [SBIE1301](SBIE1301.md).

Usage:
```
   .
   .
   .
   [GlobalSettings]
   AlertFolder=%ProgramFiles%\Mozilla Firefox
```

Related Sandboxie Plus setting: Options menu > Global Settings > Program Control > Program Alerts

See also: [Alert Process](AlertProcess.md).
