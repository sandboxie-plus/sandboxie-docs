# RPC Compatibility

Sandboxie includes compatibility handling for applications that use Windows Remote Procedure Call (RPC). This handling helps sandboxed processes construct suitable bindings, resolve dynamic local endpoints, apply communication-timeout adjustments, and connect to selected host services without replacing the Windows RPC runtime.

These mechanisms are not a general RPC firewall. Generic IPC reachability, Windows access checks, endpoint-specific request filtering, and the identity of sandboxed service processes are separate parts of the overall model.

## Architecture overview

RPC compatibility spans several Sandboxie components:

```text
sandboxed application
        |
        v
SbieDll RPC binding interception
        |
        +-- optional binding preset and timeout decision
        |
        +-- optional dynamic endpoint request
                    |
                    v
             SbieSvc endpoint mapper helper
                    |
                    +-- Windows endpoint mapper or service process lookup
                    |
                    v
             SbieDrv dynamic-port registration and optional filter
                    |
                    v
             Windows RPC endpoint
```

Built-in templates provide the maintained mappings required by supported compatibility cases. Endpoint-specific security behavior for LSA, SAM, WPAD, and related services is documented under [System Endpoints](SystemEndpoints.md).

## RPC binding presets

`RpcPortBinding` provides advanced compatibility presets for RPC bindings. Each preset matches the calling module and an identifier supplied by the binding operation:

- For `RpcBindingCreateW`, the identifier is the binding template's object UUID.
- For `RpcBindingFromStringBindingW`, the configured pattern is matched against the complete string binding.

The object UUID used for this matching should not be confused with the RPC interface UUID used for endpoint lookup.

In short: **object UUID = which object; interface UUID = which operations; string binding = how to reach it.**

A schematic form is:

```ini
RpcPortBinding=<module>,<object-UUID-or-string-binding-pattern>[,Resolve=<port-id>][,TimeOut=y|n]
```

When a preset matches, Sandboxie can supply a local endpoint and adjust the communication timeout. `Resolve=<port-id>` requests an endpoint lookup using the mappings described below. In the `RpcBindingCreateW` path, endpoint substitution applies to local RPC bindings that do not already specify an endpoint.

If no preset matches, Sandboxie continues through the normal binding path. An unmatched preset does not deny access.

The parser also supports internal forms used by maintained templates. Prefer those templates rather than treating every supported form or endpoint identifier as a stable manual-configuration interface.

### Dynamic endpoint mappings

Two related settings supply the endpoint mapper helper with the information needed for `Resolve=`:

- `RpcPortBindingIfId` maps a logical port identifier to an RPC interface UUID. SbieSvc can then ask the Windows endpoint mapper for a matching current endpoint.
- `RpcPortBindingSvc` maps a logical port identifier to a Windows service name. SbieSvc identifies the service process and asks the driver for that process's current dynamic RPC port.

These settings are primarily maintained template and service-resolution plumbing. Interface UUIDs and service endpoint details can change with Windows and should not be copied blindly from templates.

## Dynamic-port filtering

`RpcPortFilter` supports request filtering for dynamically resolved ports that Sandboxie registers globally with the driver. SbieSvc reads the maintained filter entries and submits the resolved port and filter identifiers to SbieDrv. The driver accepts this registration through its service-only path, examines requests sent to the registered port, and rejects configured matches with access denied.

An optional function name in a filter entry is informational; current enforcement uses the configured request identifier, not that label. For supported special endpoints, an `Open<Name>Endpoint` option can suppress the corresponding filter when the endpoint is registered.

> [!WARNING]
> The request identifiers used by `RpcPortFilter` are protocol- and version-sensitive implementation details. Incorrect values can block legitimate RPC activity. Prefer Sandboxie's maintained templates instead of inventing entries or copying message identifiers as though they were a stable RPC authorization API.

`RpcPortFilter` does not filter every RPC endpoint and is not a general-purpose RPC firewall. See [System Endpoints](SystemEndpoints.md) for the supported endpoint-specific compatibility controls.

## RPC communication timeout

Sandboxie normally applies an RPC communication-timeout adjustment to binding handles. The current runtime default for `RpcMgmtSetComTimeout` is enabled when the setting is absent.

To disable the default adjustment explicitly:

```ini
[DefaultBox]
RpcMgmtSetComTimeout=n
```

This setting changes compatibility and timing behavior. It does not grant endpoint access, block an endpoint, or provide a firewall.

In SandMan, the control is under **Sandbox Options > Various Options > Compatibility** and is labeled:

> Disable the use of RpcMgmtSetComTimeout by default (this may resolve compatibility issues)

The checkbox is inverted relative to the setting:

- selected writes `RpcMgmtSetComTimeout=n`;
- cleared retains the normal enabled behavior.

### Calling-module override

`UseRpcMgmtSetComTimeout` is an advanced calling-module-qualified override used when the current binding has not already supplied its timeout decision. For example, maintained templates can select different timeout behavior for calls originating in a particular DLL.

`UseRpcMgmtSetComTimeout` allows different timeout behavior for calls originating in particular modules, such as a DLL. Sandboxie checks this setting before looking for a matching `RpcPortBinding` preset.

If the matching preset includes `TimeOut=`, that value overrides the module-specific decision. Otherwise, the module-specific decision remains in effect, even when a binding preset matches. If neither provides an override, Sandboxie uses the process's `RpcMgmtSetComTimeout` default.

## Sandboxed RpcSs startup

Sandboxie normally starts its sandbox-associated RpcSs when a process needs the sandboxed endpoint mapper. That RpcSs can in turn start the sandboxed DcomLaunch process through the special server-start flow. These are Sandboxie service executables associated with the box, not the unsandboxed host service instances.

`NoSandboxieRpcSs` causes the special server-start helper to return before starting sandboxed RpcSs or DcomLaunch for the relevant endpoint requests. It does not disable Windows RPC, block all RPC communication, or disable `RpcPortBinding`. No supported general user workflow for this option is documented, so it should be treated as internal compatibility behavior rather than a routine configuration control.

The identity used to launch sandboxed RpcSs is controlled separately. See [Sandboxed Services](SandboxedServices.md#runrpcssassystem).

## Applying changes

RPC timeout defaults are initialized in each sandboxed process, while module-specific binding decisions are made as bindings are created. Dynamic endpoints are also resolved and registered as needed. Restart affected sandboxed processes, or recreate the sandboxed process tree, after changing these settings so existing bindings and cached endpoint information are not reused.

Changes to the RpcSs launch identity require restarting the sandboxed RpcSs process. A SandMan, SbieSvc, or driver restart is not normally required solely for these configuration changes.

## Version history

| Setting or mechanism | Introduced |
| --- | --- |
| `RpcMgmtSetComTimeout` | Sandboxie Plus 0.6.7 |
| `UseRpcMgmtSetComTimeout` | Sandboxie Plus 0.7.1 |
| `RpcPortBinding`, `RpcPortBindingIfId`, and `RpcPortBindingSvc` | Sandboxie Plus 0.7.3 |
| `NoSandboxieRpcSs` | Sandboxie Plus 1.5.0 |
| `RpcPortFilter` | Sandboxie Plus 1.14.2 |

## Related pages

- [System Endpoints](SystemEndpoints.md)
- [Sandboxed Services](SandboxedServices.md)
- [Open IPC Path](OpenIpcPath.md)
- [Closed IPC Path](ClosedIpcPath.md)
- [Sandboxie Ini](SandboxieIni.md)
