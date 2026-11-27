# Set Compartment Mode

`SetCompartmentMode` overrides how SbieDll classifies a sandboxed process during initialization. It was introduced in 1.17.0 / 5.72.0. The override changes only the DLL's application-compartment flag; it does not change the sandbox mode enforced by the driver or create a Windows AppContainer. [^1] [^2]

## Syntax

`SetCompartmentMode=(y|n)`

In [Sandboxie.ini](SandboxieIni.md), `y` forces the DLL's flag on and `n` forces it off. The sandbox's effective value takes precedence over the global fallback. If the effective value is missing or not recognized, SbieDll uses the driver-reported flag. [^2]

## Usage

To force only the DLL-side application-compartment flag for one sandbox:

```ini
[DefaultBox]
SetCompartmentMode=y
```

Reload the configuration and restart the affected processes. The DLL can now use compartment-mode behavior even if the driver's sandbox mode is unchanged. To configure an actual application compartment instead, see [No Security Isolation](NoSecurityIsolation.md). [^2] [^3]

## See also

- [Application Compartment](../PlusContent/compartment-mode.md)

[^1]: [Release 1.17.0 / 5.72.0](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.17.0) and [tagged DLL initialization](https://github.com/sandboxie-plus/Sandboxie/blob/v1.17.0/Sandboxie/core/dll/dllmain.c#L308-L314).
[^2]: [DLL compartment flag initialization](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/dllmain.c#L311-L314), [Boolean configuration lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/sbieapi.c#L1387-L1401), and [driver fallback to global settings](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L1443-L1468).
[^3]: [Driver compartment configuration](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/process.c#L730-L739) and [driver fallback](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/process.c#L817-L829).
