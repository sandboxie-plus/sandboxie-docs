# No Sandboxie Console

_NoSandboxieConsole_ is an advanced debug and compatibility setting that bypasses Sandboxie's custom console-redirection and proxy path.

```ini
[DefaultBox]
NoSandboxieConsole=y
```

The default is `n`. This is a box-wide Boolean setting; normal template and `GlobalSettings` inheritance can contribute its effective value.

> [!IMPORTANT]
> The name does not mean that console applications are disabled or that no console window can exist. It disables Sandboxie's custom console handling so that normal Windows console behavior can be used where possible.

## What changes

With `NoSandboxieConsole=y`, Sandboxie takes the no-custom-console branch during process initialization:

- the driver skips the special initialization that can detach a console application from its initial console and mark it for later proxy-console creation;
- the low-level initialization skips the corresponding WOW64 console-handle adjustment;
- SbieDll skips its proxy-console reconnection and `AllocConsole` replacement path, along with the console-title hooks installed by the normal branch;
- Sandboxie's `ConsoleControl` hook is not imported or installed.

These changes bypass the path in which SbieDll asks the SbieSvc GUI proxy to create a helper console and then attaches the sandboxed process to it. The setting does not prevent `cmd.exe`, PowerShell, or other console applications from running.

## What remains active

The setting does not remove every console-related Sandboxie code path. SbieDll still records the current console window when one exists so that its later auxiliary GUI/message thread can operate, including message handling used for device-change notifications.

Other Sandboxie isolation and virtualization mechanisms also remain independent. `NoSandboxieConsole` is not a general switch for terminal, desktop, token, or GUI isolation.

## Compatibility and debugging

The option exists as a debug and compatibility escape for applications that do not work with Sandboxie's custom console redirection. It is not the normal default and should not be described as disabling Windows Console Host.

Current source implements the classic Sandboxie console path described above. It does not establish comprehensive behavior for Windows Terminal or pseudoconsole (ConPTY) sessions.

## Application Compartment

[Application Compartment](NoSecurityIsolation.md) processes already bypass the same custom console branches during driver, low-level, and SbieDll initialization. Adding `NoSandboxieConsole=y` does not enable that console behavior a second time in an Application Compartment box. This equivalence is limited to the relevant console paths; the two settings are not otherwise interchangeable.

## Relationship to DropConHostIntegrity

[Drop ConHost Integrity](DropConHostIntegrity.md) applies to the external console host created through Sandboxie's proxy/helper path. Because `NoSandboxieConsole=y` bypasses that path, `DropConHostIntegrity` should not be expected to modify a console host created through the resulting normal Windows console path.

## SandMan configuration

SandMan does not currently provide a dedicated control for `NoSandboxieConsole`. Configure it manually in the sandbox section of `Sandboxie.ini`, or through an applicable template or `GlobalSettings` entry.

## Applying changes

The setting is consumed during early process and console initialization and cannot retrofit a different console path into an already-running process. Restart affected sandboxed console applications after changing it. A SandMan, service, or driver restart is not normally required.

## Version history

`NoSandboxieConsole` was introduced in Sandboxie Plus 0.9.8 / Classic 5.53.0. The changelog notes that this console behavior had previously been part of `NoSandboxieDesktop=y`; current source reads `NoSandboxieConsole` and `NoSandboxieDesktop` as separate settings.

## Related pages

- [Drop ConHost Integrity](DropConHostIntegrity.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
