# Token and Syscall Internals

## Overview

Processes in normal security-isolation boxes run with a restricted or reconstructed Windows primary token. Sandboxie also patches selected native-system-call stubs and routes those calls through SbieDrv so that the driver can inspect and mediate compatible operations.

For user-facing configuration of the current token-construction paths, see [Access Token Isolation](AccessTokenIsolation.md).

This token and syscall architecture is only part of Sandboxie's isolation model. File, registry, IPC, network, GUI, and other controls are implemented separately; see [Isolation Mechanism](IsolationMechanism.md). Application Compartment mode, configured through [No Security Isolation](NoSecurityIsolation.md), normally bypasses the primary-token replacement model described here.

## Components involved

- **SbieDrv** tracks sandboxed processes, replaces their primary tokens, mediates native system calls, and applies relevant kernel-side policy and filtering.
- **SbieSvc** coordinates early process injection and provides privileged helper functionality.
- **LowLevel / SbieLow** performs early injected setup and patches selected native-system-call stubs.
- **SbieDll** provides user-mode virtualization, compatibility hooks, and related initialization.

## Process startup

The current high-level startup flow is:

```text
Windows process creation
    |
    v
process callback identifies sandboxed process
    |
    v
early LowLevel / SbieDll injection is coordinated
    |
    v
first relevant image-load initialization
    |
    v
Sandboxie initializes sandbox subsystems
    |
    v
primary token is filtered/reconstructed
    |
    v
restricted/reconstructed token is assigned
    |
    v
earlier source token is retained for mediated operations
```

The driver process callbacks identify and record the sandboxed process, while SbieSvc coordinates low-level injection. The first relevant image-load notification then triggers initialization of the sandbox subsystems and the primary-token replacement path.

## Primary-token processing

Token processing has separate stages:

```text
original primary token
    |
    v
preliminary filtering
    |
    v
restriction / reconstruction
    |
    v
sandbox primary token
```

Preliminary filtering can remove or disable token properties before the later restriction or reconstruction stage. Consequently, the token supplied to that later stage—and the earlier source token retained after replacement—may already be preliminarily filtered. Advanced configuration can alter which stages are used, but the retained token should not be described universally as the original unrestricted token.

`SeFilterToken` is used by the current preliminary filtering stage. It is distinct from the internal `SepFilterToken` routine used by the legacy restriction path and is not legacy-only.

## Modern token reconstruction

Current normal configurations commonly use `Token_CreateToken`. This path is selected when `SepFilterToken` is unavailable, when `UseCreateToken` selects it, or when `SandboxieAllGroup` selects it. The current runtime default for `SandboxieAllGroup` makes modern reconstruction the common normal path.

Rather than modifying the source token object in place, the modern path constructs a new token from source-token information. It handles the token user, groups, privileges, integrity, owner, primary group, default DACL, token source, authentication and token statistics, and, where applicable, device groups and token security attributes. Normal reconstruction can substitute the token user, lower integrity, restrict groups, reduce privileges, and add Sandboxie-specific token groups.

The modern reconstruction path already creates the new token through dynamically resolved token-creation services, preferring `ZwCreateTokenEx` and falling back to `ZwCreateToken` where required. These are internal kernel services rather than ordinary user-facing configuration APIs.

## Legacy token filtering

The older restricted-token path remains in the implementation. It can be selected when `SepFilterToken` was resolved, the modern path was not selected, and advanced configuration did not bypass the restriction stage.

The legacy path uses internally resolved `SepFilterToken`, documented `SeFilterToken`, and internal `TOKEN`-structure information such as `RestrictedSidCount`, `RestrictedSids`, `UserAndGroups`, and `UserAndGroupCount`. The legacy token path still uses `SepFilterToken` and internal `TOKEN`-layout data, but it is not the normal path in current configurations.

## Retained source tokens

After successful primary-token replacement, Sandboxie retains a reference to the earlier source token in per-process state. Depending on preliminary filtering, this may be the original primary token or a preliminarily filtered source token.

For a mediated call, Sandboxie may temporarily impersonate a recorded thread impersonation token or the retained process source token. Temporary impersonation is normally cleared after the operation.

Sandboxie's current impersonation helper calls `PsImpersonateClient` at `SecurityIdentification`. When a higher effective impersonation level is required, it uses version-specific `ETHREAD` information supplied through DynData to adjust that level. This remains a current implementation-specific dependency on supported Windows versions; it is not merely a historical Windows XP workaround.

## Native syscall mediation

Sandboxie enumerates relevant native syscall exports and stubs. The injected low-level code patches selected stubs and routes calls through SbieDrv. The driver identifies the syscall entry, applies a Sandboxie-specific handler where one exists, or invokes the underlying kernel service as appropriate. During normal mediation, it may apply the temporary source-token or thread-token impersonation described above and clears that impersonation afterward.

Driver syscall metadata includes the syscall or service index, kernel service address, argument count, and handler or approval state. Address and argument-count information are still derived from service-table metadata. Native NT syscalls and Win32k syscalls use related but separate mechanisms; Win32k support is conditional and has separate dispatch structures.

Service-table information can come from several routes, including DynData, the exported `KeServiceDescriptorTable` where available, and architecture- or build-specific analysis involving `KeAddSystemServiceTable`. The historical description of Sandboxie always locating one unexported table solely by analyzing `KeAddSystemServiceTable` is therefore incomplete.

## Direct syscalls

A direct syscall that bypasses a patched NTDLL stub also bypasses that particular user-mode-to-driver mediation route. It does not, however, recover Sandboxie's retained source-token context. The call normally executes under the restricted or reconstructed sandbox primary token and remains subject to applicable Windows access checks and independent Sandboxie kernel enforcement.

The exact outcome depends on the syscall, token permissions, the active Sandboxie subsystem, and configuration. Direct syscalls therefore neither bypass all Sandboxie controls nor have one universal failure result.

In Application Compartment mode, primary-token replacement is normally bypassed, the retained process token used by this mechanism is not established through the normal path, and the low-level syscall hooks are disabled for that mode. SbieDll can still provide other virtualization and compatibility functions.

## Primary-token replacement

The image-load callback triggers the relevant process initialization; it does not itself overwrite a token pointer. Sandboxie first prepares the replacement token. During assignment, it temporarily clears the process's `PrimaryTokenFrozen` flag, calls `ZwSetInformationProcess` with `ProcessAccessToken`, and then restores the flag.

Access to `PrimaryTokenFrozen` uses version- and build-specific `EPROCESS` knowledge supplied through DynData on applicable systems. Sandboxie does not directly replace the primary-token pointer.

## Implementation-specific kernel dependencies

Sandboxie uses a mix of documented APIs, dynamically resolved routines, and build-sensitive implementation-specific kernel mechanisms.

| Dependency | Role and current scope |
| --- | --- |
| `ZwCreateTokenEx` / `ZwCreateToken` | Dynamically resolved token-creation services used by the current modern reconstruction path. |
| `SepFilterToken` and internal `TOKEN` layout | Used by the legacy token path; the modern path avoids these legacy layout dependencies. |
| Service descriptor-table information | Used to identify native services, addresses, and argument metadata for syscall mediation. |
| `ETHREAD` impersonation information | Used by the current impersonation helper when adjusting effective impersonation level. |
| `EPROCESS` process information | Includes `PrimaryTokenFrozen` and other build-sensitive fields involved in process initialization. |

Sandboxie also contains build-sensitive kernel compatibility code outside this token and syscall path, including clipboard and window-station handling.

## Dynamic data

DynData supplies build-specific knowledge about implementation-sensitive kernel structures and service tables. The driver can use built-in data or accepted, signed external data for newer builds.

If compatible DynData is unavailable, the driver can remain loaded, but affected boxes may be forced into Application Compartment behavior instead of receiving normal token isolation. Missing DynData therefore does not have one universal fail-closed or startup-failure outcome.

## Failure behavior

Failure to obtain a required source token, construct an essential sandbox token, or assign the replacement token can abort process initialization. Failure to resolve `SepFilterToken` selects the modern construction path, while an unavailable `ZwCreateTokenEx` can fall back to `ZwCreateToken`.

Failures during native or Win32k syscall initialization can prevent driver initialization. A failure to establish required temporary impersonation can terminate the affected sandboxed process. As described above, unavailable compatible DynData can instead cause compartment-mode fallback. These paths should not be summarized as one universal failure policy.

## Historical evolution

The original architecture used the legacy `SepFilterToken` / `SeFilterToken` path together with internal `TOKEN` offsets. Sandboxie Plus 1.0.7 / Classic 5.55.7-era development introduced experimental `CreateToken`-based reconstruction. By January 2, 2022, the source already contained `SbieCreateToken` using `ZwCreateTokenEx` with a `ZwCreateToken` fallback, although the original version of this page, created later in 2022, still discussed that change as a future direction.

Sandboxie Plus 1.13.0 / Classic 5.68.0 introduced the signed, updateable DynData architecture. Version 1.14.1 / 5.69.1 integrated the modern `UseCreateToken` / `SandboxieAllGroup` path, and version 1.17.0 / 5.72.0 made `SandboxieAllGroup` enabled by runtime default. That change made modern token reconstruction the common normal path while retaining the older path for configurations and systems that select it.

## Related pages

- [Access Token Isolation](AccessTokenIsolation.md)
- [Isolation Mechanism](IsolationMechanism.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Drop Admin Rights](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
