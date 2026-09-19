# Sandboxed Services

Sandboxie can intercept and emulate selected Windows Service Control Manager (SCM) operations so that certain services run as processes associated with a sandbox. This is a combination of SbieDll API interception, sandboxed service configuration and state, privileged operations performed by SbieSvc, and access to the real Windows SCM when a host-service operation is required.

It is not a complete clone or full virtualization of the Windows SCM. Sandboxie selectively intercepts and emulates SCM operations, keeps sandboxed-service configuration and state in the sandbox, and uses SbieSvc for privileged operations or communication with the real SCM.

## SandboxService

`SandboxService` selects services that should use Sandboxie's sandboxed-service model:

```ini
SandboxService=ServiceName
```

Multiple entries are supported:

```ini
SandboxService=ServiceOne
SandboxService=ServiceTwo
```

The default is an empty list. Service names are matched exactly and case-insensitively. Wildcards, negation, and executable-qualified forms are not supported.

`SandboxService` does not select SYSTEM identity by itself. It only affects whether the matching service is handled as a sandboxed service.

## What makes a service sandboxed

Sandboxie can classify a service as sandboxed when, among other internal paths:

- it was created within the sandbox and appears in the sandboxed service state;
- its name matches a `SandboxService` entry;
- Sandboxie has built-in handling for that service.

The built-in cases are implementation details and should not be treated as a general list of services supported by `SandboxService`.

## Starting a sandboxed service

When an intercepted `StartService` request targets a service classified as boxed, Sandboxie does not simply ask the host SCM to start the existing host instance. At a high level, the flow is:

```text
sandboxed StartService request
       |
       v
Sandboxie classifies service as boxed
       |
       v
virtual state -> START_PENDING
       |
       v
SbieSvc launches service executable through Sandboxie
       |
       v
service process becomes associated with the box
       |
       v
sandboxed service state -> RUNNING
```

The diagram summarizes Sandboxie's state handling rather than specifying exact Windows SCM timing.

An already running host service is not automatically moved into the sandbox, terminated, or adopted as the sandboxed instance. Whether a service supports a separate sandboxed instance depends on that service. If the service is missing or cannot be started through the sandboxed-service path, the operation fails rather than deliberately falling back to starting the real host service.

## Sandboxed SCM model

SbieDll intercepts service open, create, start, query, and dispatcher paths. Service configuration created inside a sandbox can be stored through virtualized registry state, and Sandboxie maintains synthetic handles or service state where required. SbieSvc performs privileged actions and communicates with the real SCM when an operation is intended for a host service.

This division allows a sandboxed process to use familiar SCM APIs without implying that every SCM behavior is fully virtualized.

## RunServiceAsSystem

`RunServiceAsSystem` selects a SYSTEM source identity for named sandboxed services:

```ini
RunServiceAsSystem=ServiceName
```

Multiple entries are supported. The default is an empty list. Matching is exact and case-insensitive; wildcards, negation, and executable-qualified forms are not supported.

`RunServiceAsSystem` changes the source identity used to launch a matching sandboxed service. It does not by itself move a host service into the sandbox. The service must separately be classified as sandboxed, for example through `SandboxService`.

## RunServicesAsSystem

The broad form is:

```ini
RunServicesAsSystem=y
```

Its default is `n` (disabled). When enabled, the service-start path can select SYSTEM identity broadly for sandboxed services, subject to current special-case logic.

The historical metadata wording that refers to RpcSs and DcomLaunch is not a complete description of current executable behavior. The setting is neither limited to those two names nor an unconditional guarantee that every sandboxed service will use SYSTEM regardless of special cases.

### Selective and broad forms

`RunServiceAsSystem=<name>` targets only named services. `RunServicesAsSystem=y` enables broader SYSTEM-source selection, so services not named by the selective setting can still use the broad path where current logic permits. Adding a selective entry does not cancel the global setting for other services.

The selective form is useful when only particular services require the SYSTEM source identity.

## RunRpcssAsSystem

`RunRpcssAsSystem` controls the source identity used when SbieSvc starts the sandbox-associated RpcSs process:

```ini
RunRpcssAsSystem=y
```

The default is `n`. An explicit `y` makes SbieSvc duplicate its SYSTEM source token for the sandboxed RpcSs launch. The resulting `SandboxieRpcSs` process remains associated with the sandbox; this setting does not start or adopt the unsandboxed host RpcSs service.

> [!WARNING]
> Starting sandboxed RpcSs from a SYSTEM source token increases the consequences of access that remains open to that process. Use this compatibility option only when required. It does not, by itself, remove RpcSs from the sandbox.

### Application Compartment and OriginalToken

Current service-launch logic can select the same SYSTEM-source path automatically when both of the following are true:

1. the caller is in Application Compartment mode or `OriginalToken=y` is configured; and
2. either `MsiInstallerExemptions=y` or `RunServicesAsSystem=y` is enabled.

Application Compartment alone therefore does not automatically make sandboxed RpcSs use a SYSTEM source token.

Sandboxed DcomLaunch is started through the sandboxed RpcSs/server flow. The explicit token-source decision above is made for the RpcSs launch; it should not be generalized into a separate, identical DcomLaunch token-selection rule.

### SandMan control

The control is under **Sandbox Options > Security Options > Advanced Security** with the label:

> Start the sandboxed RpcSs as a SYSTEM process (not recommended)

SandMan loads this checkbox from the explicit `RunRpcssAsSystem` value. In Application Compartment mode, it disables the direct control when either broad `RunServicesAsSystem` behavior or `MsiInstallerExemptions` already causes the automatic runtime condition described above.

For binding resolution, endpoint filtering, timeout behavior, and sandboxed RpcSs startup architecture, see [RPC Compatibility](RpcCompatibility.md).

## What "as SYSTEM" means

For this service-start path, Sandboxie obtains a source token from SbieSvc, which runs as LocalSystem, duplicates a primary token, adjusts its session, and uses it to launch the sandboxed service process. Sandboxie also applies its service-side privilege stripping by default where applicable.

"Run as SYSTEM" therefore describes the source identity used to start the sandboxed service. It does not mean an unrestricted LocalSystem process running outside the sandbox.

In a normal isolation box:

- the process remains associated with the sandbox;
- the normal Sandboxie token and isolation pipeline can still apply;
- file, registry, IPC, and other isolation mechanisms remain separate.

`NoSecurityIsolation` / Application Compartment changes later token and isolation behavior, so the settings on this page do not guarantee one identical final token under every box mode.

## Related special cases

[Msi Installer Exemptions](MsiInstallerExemptions.md) can alter MSIServer handling, and CryptSvc has current special-case behavior. These mechanisms are related to service identity but are not general replacements for the settings documented here.

## Chromium elevation template

The current `Chromium_Elevation` template uses this pattern:

```ini
OpenSamEndpoint=y

SandboxService=MicrosoftEdgeElevationService
RunServiceAsSystem=MicrosoftEdgeElevationService

SandboxService=MicrosoftEdgeDevElevationService
RunServiceAsSystem=MicrosoftEdgeDevElevationService

SandboxService=MicrosoftCopilotElevationService
RunServiceAsSystem=MicrosoftCopilotElevationService

SandboxService=GoogleChromeElevationService
RunServiceAsSystem=GoogleChromeElevationService

SandboxService=GoogleChromeDevElevationService
RunServiceAsSystem=GoogleChromeDevElevationService

SandboxService=BraveElevationService
RunServiceAsSystem=BraveElevationService
```

The template supplies three separate parts of the compatibility flow:

`SandboxService`
: Routes the named elevation service through Sandboxie's sandboxed-service model.

`RunServiceAsSystem`
: Uses the SYSTEM source identity only for that named elevation service.

`OpenSamEndpoint`
: Removes the SAM message filter required by this compatibility flow. See [System Endpoints](SystemEndpoints.md).

The template moved from broad `RunServicesAsSystem=y` behavior to selective `RunServiceAsSystem=...` entries. This limits SYSTEM-source selection to the named elevation services instead of applying the broad setting to other sandboxed services.

The template is maintained by Sandboxie and normally does not need to be copied manually.

## DPAPI relationship

Sandboxie has separate DPAPI compatibility and proxy handling. Recent Chromium elevation work adjusted the identity used for DPAPI scenarios involving services running as SYSTEM.

`OpenSamEndpoint` does not implement DPAPI and does not decrypt credentials. Compatibility still depends on the effective Windows identity, Windows DPAPI rules, Chromium behavior and policy, app-bound encryption or related mechanisms, and the availability and configuration of the elevation service. The settings on this page do not guarantee access to host credentials.

## Failure behavior

The sandboxed-service path has no general fallback that starts the real host service after a boxed launch fails:

- a nonexistent or unavailable service fails to start;
- driver services and unsupported non-Win32 service types are rejected by the boxed-service path;
- an already running host instance is not automatically adopted;
- failure to obtain or duplicate the SYSTEM source token, or to create the sandboxed process, causes the service start to fail;
- no intentional fallback to a different, less-restricted host token was identified.

The exact Windows error can depend on the point of failure.

## Applying changes

`SandboxService` is evaluated during service classification and start operations. A new value can affect later starts, but it does not move an already running service instance.

`RunServiceAsSystem` and `RunServicesAsSystem` are relevant when the service process is started. Changing either setting does not retroactively replace an already assigned service token.

Restart the affected sandboxed service or process after changing service identity settings. Recreate the sandboxed process tree when a clean configuration test is required. A SandMan, SbieSvc, or driver restart is not normally required.

## SandMan configuration

The broad setting is exposed under **Sandbox Options > Security Options > Advanced Security** with the label:

> Do not start sandboxed services using a system token (recommended)

The checkbox has inverted semantics relative to `RunServicesAsSystem`:

- when selected, broad `RunServicesAsSystem=y` behavior is disabled;
- when cleared, SandMan can write `RunServicesAsSystem=y`.

`SandboxService` and `RunServiceAsSystem` have no dedicated current SandMan controls; they are manual or template settings. The New Box Wizard does not expose these controls.

## Sandboxie Plus and Classic

The runtime is implemented in shared Sandboxie components. SandMan provides the current `RunServicesAsSystem` control, while `SandboxService` and `RunServiceAsSystem` remain manual or template settings. This does not imply equivalent current controls in Sandboxie Control Classic.

## Version history

| Setting or change | Introduced |
| --- | --- |
| `RunServicesAsSystem` | Sandboxie Plus 0.5.4 / Classic 5.46.0 |
| `RunServiceAsSystem` | Sandboxie Plus 0.5.4b / Classic 5.46.1 |
| `SandboxService` | Sandboxie Plus 0.5.5 / Classic 5.46.4 |
| `RunRpcssAsSystem` | Sandboxie Plus 0.9.7 |
| Chromium elevation and DPAPI compatibility work | Sandboxie Plus 1.18.0 / Classic 5.73.0 era |
| Selective Chromium elevation template | Sandboxie Plus 1.18.1 / Classic 5.73.1 |

These service settings predate their current Chromium elevation use.

## Related pages

- [RPC Compatibility](RpcCompatibility.md)
- [System Endpoints](SystemEndpoints.md)
- [Service Programs](ServicePrograms.md)
- [Start Service](StartService.md) — a lifecycle/startup setting, not an equivalent of `SandboxService`
- [Msi Installer Exemptions](MsiInstallerExemptions.md)
- [Sandboxie Ini](SandboxieIni.md)
