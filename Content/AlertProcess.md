# Alert Process

The _AlertProcess_ setting in [Sandboxie Ini](SandboxieIni.md) is a global configuration that specifies the names of programs triggering message [SBIE1301](SBIE1301.md) when started outside the sandbox.


To utilize this setting, add program names to the [GlobalSettings] section, as demonstrated:

```ini
[GlobalSettings]
AlertProcess=iexplore.exe
AlertProcess=firefox.exe
```

This example would trigger an alert if Internet Explorer or Firefox is initiated outside the sandbox.

### Additional References:

* [Program Settings](ProgramSettings.md).
* [Configure Menu > Alert Programs](ConfigureMenu.md#program-alerts).
