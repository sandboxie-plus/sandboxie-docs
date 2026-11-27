# No Auto Exit Explorer

`NoAutoExitExplorer` disables the Sandboxie window monitor that can close sandboxed Windows Explorer and legacy Internet Explorer when their qualifying windows are gone. It does not disable other ways those processes can exit. [^1]

## Syntax

`NoAutoExitExplorer=<value>`

In [Sandboxie.ini](SandboxieIni.md), use `y` to suppress the monitor. This is not a Boolean setting: Sandboxie checks whether it can read a nonempty first value. A readable `n` suppresses the monitor too. [^1]

## Usage

To suppress the monitor in one sandbox:

```ini
[DefaultBox]
NoAutoExitExplorer=y
```

Reload the configuration and restart the affected Windows Explorer or Internet Explorer processes. To restore monitoring, remove the entry and check for values inherited from templates or `[GlobalSettings]`. Reload and restart again. Do not replace the value with an empty assignment: the INI parser rejects it. [^1] [^2]

## See also

- [Program Stop Settings](ProgramStopSettings.md)

[^1]: [Monitor setup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/sh.c#L1395-L1410) and [window monitor behavior](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/sh.c#L1814-L1871).
[^2]: [INI parser handling of empty values](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L694-L702).
