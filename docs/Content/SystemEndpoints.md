# System Endpoints

Sandboxie permits some IPC and RPC communication with Windows system services while applying specialized message-level filters to sensitive endpoints. The settings on this page disable one of those endpoint-specific filters when required for compatibility.

They do not generically open LSA, SAM, or WPAD. Generic IPC reachability, normal Windows access checks, and unrelated Sandboxie restrictions remain separate.

Typical configuration is:

```ini
OpenLsaEndpoint=y
OpenSamEndpoint=y
OpenWPADEndpoint=y
```

All three settings are box-wide Boolean options, default to disabled, and are not executable-qualified. They can be inherited through the normal effective Sandboxie configuration, including templates.

## IPC reachability and endpoint filtering

Sandboxie handles generic IPC reachability and endpoint-specific request filtering as separate layers:

```text
sandboxed process
       |
       v
generic IPC path/object policy
       |
       +-- denied -> connection fails
       |
       v
endpoint reachable
       |
       v
endpoint-specific operation filter
       |
       v
request allowed or denied
```

[Open IPC Path](OpenIpcPath.md) can make an IPC object reachable, while [Closed IPC Path](ClosedIpcPath.md) can deny reachability. The `Open...Endpoint` settings documented here affect the later, specialized operation filter. Opening an IPC path does not inherently remove that filter, and an endpoint setting does not inherently make a closed IPC object reachable.

## OpenLsaEndpoint

```ini
OpenLsaEndpoint=y
```

The default is `n` (disabled).

Sandboxie handles the following fixed endpoint directly in SbieDrv:

```text
\RPC Control\LSARPC_ENDPOINT
```

By default, Sandboxie applies a deny-list to selected sensitive LSA RPC operations. The filter covers operations that modify policy or security state, auditing configuration, accounts and trusted domains, account rights and privileges, quotas and system-access state, and private-data state. It does not universally block LSA queries or enumerations.

`OpenLsaEndpoint` disables Sandboxie's specialized filter for sensitive operations on `LSARPC_ENDPOINT`. It does not grant unrestricted access to LSA or disable normal Windows access checks.

### Security history

The LSA endpoint filter was introduced in Sandboxie Plus 0.5.4 / Classic 5.46.0 in response to the issue later tracked as security issue ID-8 / CVE-2019-13502. The filter remains enabled by default; `OpenLsaEndpoint=y` is a compatibility relaxation for software that requires an operation the filter would otherwise deny.

## OpenSamEndpoint

```ini
OpenSamEndpoint=y
```

The default is `n` (disabled).

Sandboxie also handles this fixed endpoint directly in SbieDrv:

```text
\RPC Control\samss lpc
```

The normal SAM request filter covers sensitive mutation categories such as user and account creation or deletion, group and alias changes, membership changes, password changes, account attributes and policies, and security changes. It does not mean that every SAM request is denied.

`OpenSamEndpoint` disables Sandboxie's SAM endpoint request filter. It does not by itself expose all SAM data, bypass Windows access checks, or provide host credentials.

The filter and its compatibility setting were introduced in Sandboxie Plus 0.7.0 / Classic 5.48.0 after a security issue involving elevated sandboxed processes modifying account or password state.

### Chromium elevation services

The current Chromium elevation compatibility template combines settings in this pattern:

```ini
SandboxService=<service>
RunServiceAsSystem=<service>
OpenSamEndpoint=y
```

`SandboxService` places the elevation service in Sandboxie's sandboxed-service model, `RunServiceAsSystem` supplies the required source identity for that service, and `OpenSamEndpoint` removes the SAM filter required by the compatibility flow. `OpenSamEndpoint` alone does not implement DPAPI compatibility or grant access to host credentials. See [Sandboxed Services](SandboxedServices.md).

## OpenWPADEndpoint

```ini
OpenWPADEndpoint=y
```

The default is `n` (disabled). The setting was introduced in Sandboxie Plus 1.15.0 / Classic 5.70.0.

This setting concerns the dynamic RPC endpoint associated with Windows Web Proxy Auto-Discovery and `WinHttpAutoProxySvc`. Unlike the fixed LSA and SAM endpoints, the WPAD endpoint is discovered and registered at runtime:

```text
SbieDll
  |
  v
requests dynamic RPC endpoint resolution
  |
  v
SbieSvc / EpMapperServer
  |
  v
resolves the WPAD service endpoint
  |
  v
registers endpoint + filter with SbieDrv
  |
  v
driver applies the message filter
```

Sandboxie normally registers this endpoint with a filter for selected sensitive operations related to proxy configuration, policy, and credentials. With `OpenWPADEndpoint=y`, the endpoint is registered without that specialized filter.

`OpenWPADEndpoint` therefore allows WPAD operations that Sandboxie would otherwise filter. It does not provide unrestricted network, proxy, WinHTTP, or Internet access.

## Fixed and dynamic implementations

The settings have conceptually similar effects but use different implementation paths:

| Setting | Endpoint handling | Effect when enabled |
| --- | --- | --- |
| `OpenLsaEndpoint` | Fixed endpoint filtered directly in SbieDrv | Skips the specialized LSA operation filter |
| `OpenSamEndpoint` | Fixed endpoint filtered directly in SbieDrv | Skips the specialized SAM request filter |
| `OpenWPADEndpoint` | Dynamic endpoint resolved through SbieDll and SbieSvc, then registered with SbieDrv | Registers WPAD without its specialized message filter |

## BlockPassword relationship

[`BlockPassword`](BlockPassword.md) controls a separate legacy LSA authentication and password-related filter. Current runtime still consults it, although it was superseded for the modern password-change compatibility case by `OpenSamEndpoint`. It is not an alias for `OpenLsaEndpoint` or `OpenSamEndpoint`. `OpenLsaSSPI` has not been confirmed as a current INI setting.

## SandMan configuration

The controls are under **Sandbox Options > General Options > Isolation**:

| Setting | Current label |
| --- | --- |
| `OpenLsaEndpoint` | Open access to Windows Local Security Authority |
| `OpenSamEndpoint` | Open access to Windows Security Account Manager |
| `OpenWPADEndpoint` | Open access to Proxy Configurations |

The labels are broader than the exact operation-filter behavior described on this page. The controls load unchecked by default, write `y` when enabled, and remove the explicit key when disabled. They are disabled when `NoSecurityIsolation` / Application Compartment behavior is active. This UI state should not be interpreted as a guarantee that every endpoint path is unrestricted in that mode.

These controls are not currently offered by the New Box Wizard.

## Applying changes

The LSA and SAM settings are cached during IPC initialization for a sandboxed process. Restart affected sandboxed processes, or recreate the sandboxed process tree, after changing them.

Configure `OpenWPADEndpoint` before starting affected applications. Restarting the affected sandboxed process tree is recommended after changing it. The dynamic endpoint is resolved and registered separately, and its current caching behavior should not be treated as a guarantee that restarting only one application always rebuilds the global endpoint-filter state.

A SandMan, SbieSvc, or driver restart is not universally required by these settings.

## Failure behavior

LSA and SAM operations selected by their normal specialized filters are denied. If WPAD endpoint resolution or registration fails, the corresponding RPC or binding operation can fail; no unrestricted fallback has been established. Generic IPC policy can also deny communication before endpoint-specific filtering is reached. The observable error depends on the failed layer, so one error code does not describe every case.

## Sandboxie Plus and Classic

Runtime support is implemented in shared Sandboxie components. SandMan provides the controls described above, and compatible manual settings can be consumed by the shared runtime. This does not imply that Sandboxie Control Classic provides equivalent current controls.

## Version history

| Setting | Introduced |
| --- | --- |
| `OpenLsaEndpoint` | Sandboxie Plus 0.5.4 / Classic 5.46.0 |
| `OpenSamEndpoint` | Sandboxie Plus 0.7.0 / Classic 5.48.0 |
| `OpenWPADEndpoint` | Sandboxie Plus 1.15.0 / Classic 5.70.0 |

## Related pages

- [RPC Compatibility](RpcCompatibility.md)
- [Open IPC Path](OpenIpcPath.md)
- [Closed IPC Path](ClosedIpcPath.md)
- [Block Password](BlockPassword.md)
- [Sandboxed Services](SandboxedServices.md)
- [Sandboxie Ini](SandboxieIni.md)
