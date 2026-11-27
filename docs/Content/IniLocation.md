# INI Location

`IniLocation` is a read-only Sandboxie driver query. It reports the driver's location for the main [Sandboxie.ini](SandboxieIni.md) or which imported INI path is associated with a configuration section. It does not set either path. [^1]

## Syntax

There is no INI assignment. To query the main location from outside a sandbox, request `IniLocation` without a section. To query an imported path, request `IniLocation` as a property of the named section (`CONF_GET_PROPERTY`), not as a setting in that section. [^1]

## Results

| Query | Result |
| --- | --- |
| Main location | `H` for the Sandboxie home directory, `W` for the Windows directory, or the custom INI path when the driver uses one from the registry. |
| Section property | The section's associated imported INI path, if it has one. Otherwise there is no value. |

The Sandboxie service uses the main location result to resolve the file path. That result alone does not confirm that Sandboxie loaded a configuration file from there. [^1] [^2]

## See also

- [Sandboxie.ini](SandboxieIni.md)
- [Import Box](ImportBox.md)
- [Is Virtual](IsVirtual.md)

[^1]: [Main location and section-property lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L1379-L1442).
[^2]: [INI path resolution in the service](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/svc/sbieiniserver.cpp#L1339-L1388).
