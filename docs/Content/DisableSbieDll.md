# Disable SbieDll

`DisableSbieDll` is a debugging option that makes SbieDll return early during initialization. Despite its name, it does not stop Windows from loading SbieDll. The guarded reader is present in the source for 1.7.0 / 5.62.0. [^1]

## Syntax

`DisableSbieDll=(y|n)`

> [!NOTE]
> This option needs a SbieDll build with `WITH_DEBUG` defined. The checked-in `SbieRelease` configurations do not define it, so the entry has no effect in those builds. [^2]

In a build that reads it, use [Sandboxie.ini](SandboxieIni.md). The sandbox's effective value takes precedence over the global fallback. The default is `n`. [^3]

## Debug-build behavior

With `y`, the DLL skips the rest of its normal initialization for a newly started sandboxed process, including its usual user-mode hooks. The process is still sandboxed by the driver, and applications may fail without the hooks they normally use. The entry does not undo initialization in a process that is already running. [^4]

## See also

- [Hook and Loader Compatibility](HookAndLoaderCompatibility.md)

[^1]: [Release 1.7.0 / 5.62.0](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.7.0) and [tagged SbieDll source](https://github.com/sandboxie-plus/Sandboxie/blob/v1.7.0/Sandboxie/core/dll/dllmain.c#L357-L366).
[^2]: [SbieDll build configurations](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/SboxDll.vcxproj#L165-L350).
[^3]: [Boolean configuration lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/sbieapi.c#L1387-L1401) and [driver configuration lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L1443-L1468).
[^4]: [Debug-only return before hook initialization](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/dllmain.c#L376-L402).
