# No UAC Proxy

## Overview

**NoUACProxy** controls whether Sandboxie intercepts supported asynchronous RPC requests to the Windows Application Information (AppInfo) service and routes recognized elevation requests through its own UAC proxy. It is disabled by default, so Sandboxie's proxy handling is normally active.

```ini
[DefaultBox]
NoUACProxy=y
```

With `NoUACProxy=y`, Sandboxie's RPC wrappers skip their elevation recognition and proxy logic for these calls. The original native RPC call is then allowed to continue.

## What it does not mean

This setting does not disable Windows User Account Control, and it does not by itself block elevation requests. Whether the native UAC path succeeds depends on Windows and on the sandbox's RPC and resource-access configuration.

Conversely, `NoUACProxy=n` does not mean that Sandboxie intercepts every possible elevation mechanism. The current proxy recognizes supported asynchronous AppInfo/UAC RPC requests for process elevation and administrator-token requests.

## Boolean setting and compatibility template

The Boolean and the built-in template have different scopes:

```ini
NoUACProxy=y
```

disables Sandboxie's elevation-RPC interception. It does not add RPC access rules.

```ini
Template=NoUACProxy
```

enables the Boolean and also supplies UAC-related RPC port bindings intended to let the native route work in the template's compatibility scenario. Those additional bindings come from `Template_NoUACProxy`, not from the Boolean itself.

SandMan has no dedicated **NoUACProxy** checkbox. The built-in template is available under **Sandbox Options > App Templates > Templates** as **Open RPC Port Bindings for UAC**, in the **Miscellaneous** category. It can also be selected manually with `Template=NoUACProxy`.

## Application Compartment history

The Sandboxie Plus 1.0.4 / Classic 5.55.4 changelog stated that Application Compartment boxes enabled the template by default. Current SandMan code no longer auto-enables it when creating or selecting an Application Compartment preset; the former calls are commented out. Do not assume that choosing that box type currently enables **NoUACProxy** or its template.

## Relationship to other elevation settings

* [Use Sandboxie UAC](UseSandboxieUAC.md) controls the enhanced prompt inside Sandboxie's proxy. When `NoUACProxy=y` skips proxy interception, that prompt is not reached through the skipped path.
* [Apply ElevateCreateProcess Fix](ApplyElevateCreateProcessFix.md) can initiate a Windows `runas` request after `CreateProcess` reports that elevation is required. **NoUACProxy** determines whether Sandboxie's supported RPC interception participates in the resulting elevation path.

`UseSandboxieUAC=n` is not a substitute for `NoUACProxy=y`: the former skips only the enhanced prompt, while the latter skips Sandboxie's supported RPC elevation interception.

## Applying changes

The RPC hook reads **NoUACProxy** for each relevant request. After the configuration has been saved and reloaded, subsequent requests in an already-running process use the new effective value; restarting the process, SandMan, SbieSvc, or the driver is not normally required. An in-progress request is not changed retroactively.

## Version history

`NoUACProxy` and its accompanying template were introduced in Sandboxie Plus 1.0.4 / Classic 5.55.4.

## Related pages

* [Apply ElevateCreateProcess Fix](ApplyElevateCreateProcessFix.md)
* [No Security Isolation](NoSecurityIsolation.md)
* [Sandboxie Ini](SandboxieIni.md)
* [Use Sandboxie UAC](UseSandboxieUAC.md)
