# Drop ConHost Integrity

_DropConHostIntegrity_ is a console-compatibility setting. It makes Sandboxie attempt to lower the integrity level of the external `conhost.exe` associated with a console created through Sandboxie's console proxy.

```ini
[DefaultBox]
DropConHostIntegrity=y
```

The default is `n`. This is a box-wide Boolean setting; normal template and `GlobalSettings` inheritance can contribute its effective value.

## Runtime behavior

When Sandboxie's console proxy is used, an SbieSvc helper creates a console and Windows starts the associated `conhost.exe` outside the sandbox. The sandboxed process then attaches to that console and the helper exits.

With `DropConHostIntegrity=y`, the helper identifies its associated console-host process, opens that process token, and attempts to set its mandatory integrity level to **Untrusted**. This changes the integrity label of that proxy-created console host; it does not sandbox `conhost.exe` or change the token of the sandboxed application.

The adjustment is best effort. If Sandboxie cannot identify the console host, open the process or its token, or apply the new integrity label, console creation continues without treating that adjustment failure as fatal.

## Why it exists

This setting was introduced for console applications that could not perform some console-buffer operations when an Untrusted sandboxed process was attached to a console host at a higher integrity level. Reported symptoms included PowerShell errors and Node.js interactive-console failures. Lowering the associated console host to Untrusted resolved the reported mismatch, but not every console failure has this cause and behavior can vary between Windows versions. See [Sandboxie issue #678](https://github.com/sandboxie-plus/Sandboxie/issues/678) for the original report.

## Scope and limitations

`DropConHostIntegrity` is not a global policy for every `conhost.exe` process. It is consulted when the Sandboxie console helper successfully creates a proxy console, and it targets only the console host associated with that helper-created console.

The setting does not control every terminal architecture. In particular, its implementation does not establish general coverage for Windows Terminal, pseudoconsole (ConPTY), or console hosts created outside Sandboxie's proxy path.

## Relationship to NoSandboxieConsole

[No Sandboxie Console](NoSandboxieConsole.md) bypasses Sandboxie's custom console-redirection and proxy path. `DropConHostIntegrity` applies inside that proxy path, so it should not be expected to modify a console host created through the `NoSandboxieConsole` path.

## SandMan configuration

In SandMan, open:

**Sandbox Options > Security Options > Advanced Security**

The checkbox is labeled **Drop ConHost.exe Process Integrity Level**. Selecting it writes `DropConHostIntegrity=y`; clearing it leaves the option disabled.

## Applying changes

The value is consulted when a new proxy console is created. Changing it does not relabel an existing console host. Restart the affected sandboxed console application so that an applicable console can be created with the new setting. A SandMan, service, or driver restart is not normally required.

## Version history

`DropConHostIntegrity` was introduced in Sandboxie Plus 0.7.3 / Classic 5.49.5. The dedicated SandMan checkbox was added in Sandboxie Plus 1.14.7 / Classic 5.69.7.

## Related pages

- [No Sandboxie Console](NoSandboxieConsole.md)
- [Sandboxie Ini](SandboxieIni.md)
