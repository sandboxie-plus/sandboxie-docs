# Alert Process

_AlertProcess_ is a global setting in [Sandboxie Ini](SandboxieIni.md). It specifies names of programs that if started outside the sandbox, will cause Sandboxie to issue message [SBIE1301](SBIE1301.md).

Usage:
```
   .
   .
   .
   [GlobalSettings]
   AlertProcess=iexplore.exe
   AlertProcess=firefox.exe
```


See also:
* [Program Settings](ProgramSettings.md).
* [Configure Menu > Alert Programs](ConfigureMenu.md#program-alerts).
