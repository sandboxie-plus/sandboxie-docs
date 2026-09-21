# Apply ElevateCreateProcess Fix

## Overview

**ApplyElevateCreateProcessFix** enables Sandboxie's legacy ElevateCreateProcess compatibility fallback when a process launch through `CreateProcess` fails because elevation is required. It is disabled by default and can be configured for the whole sandbox or for the sandboxed executable making the `CreateProcess` call.

```ini
[DefaultBox]
ApplyElevateCreateProcessFix=y
```

For a process-specific rule:

```ini
[DefaultBox]
ApplyElevateCreateProcessFix=legacy-installer.exe,y
```

The optional executable selector is matched against the sandboxed process that attempted the launch, not the requested child executable.

## When it applies

The setting does not force every process launch to elevate. Sandboxie first uses the normal `CreateProcess` path. The fallback is considered only when that attempt fails with `ERROR_ELEVATION_REQUIRED` and the effective **ApplyElevateCreateProcessFix** rule is enabled for the calling process.

Sandboxie then retries the requested launch through `ShellExecuteExW` with the `runas` verb. If the request succeeds, the resulting process handle is returned through the original process-information structure. If the user cancels the elevation request, the launch remains cancelled. The fallback also avoids recursively starting another elevation attempt while Sandboxie is already processing a `ShellExecute` path.

The resulting `runas` request can subsequently enter Sandboxie's UAC proxy. [No UAC Proxy](NoUACProxy.md) controls whether supported elevation RPC is intercepted, while [Use Sandboxie UAC](UseSandboxieUAC.md) controls the enhanced prompt when proxying is active.

## Why it is legacy behavior

Older Sandboxie versions automatically emulated an ElevateCreateProcess compatibility shim sometimes applied by Windows Program Compatibility Assistant. Automatic emulation could turn a normal `ERROR_ELEVATION_REQUIRED` result into an elevation prompt even when the application expected the call to fail. Sandboxie Plus 0.8.0 / Classic 5.50.0 therefore made the behavior opt-in.

Use this workaround only for applications that require the legacy behavior. It does not guarantee that Windows will approve the elevation or that the target application will start successfully.

## SandMan configuration

The box-wide checkbox is under **Sandbox Options > Various Options > Compatibility**:

> Apply ElevateCreateProcess Workaround (legacy behaviour)

The dedicated checkbox writes the box-wide value. SandMan's advanced-options editor also lists **ApplyElevateCreateProcessFix** for process-specific configuration.

## Applying changes

Sandboxie evaluates the effective rule when an applicable `CreateProcess` failure occurs. After the configuration has been saved and reloaded, subsequent launch attempts from an already-running sandboxed process can use the new value; restarting SandMan, SbieSvc, or the driver is not normally required.

## Version history

The setting was introduced in Sandboxie Plus 0.8.0 / Classic 5.50.0 when the previously automatic compatibility behavior became opt-in. A dedicated SandMan checkbox was added in Sandboxie Plus 1.4.2 / Classic 5.59.2.

The 1.4.2 / 5.59.2 changelog also announced message `SBIE2226` for processes that need this setting. The current implementation retains the message text but does not actively emit it, so users should not rely on receiving that notification.

## Related pages

* [No UAC Proxy](NoUACProxy.md)
* [Sandboxie Ini](SandboxieIni.md)
* [Use Sandboxie UAC](UseSandboxieUAC.md)
