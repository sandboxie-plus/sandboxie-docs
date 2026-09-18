# Host Injection

## Overview

Host injection lets Sandboxie load a trusted compatibility DLL into a selected host process without turning that process into a normally sandboxed process.

Normal Sandboxie injection loads SbieDll into a process that is becoming sandboxed, then performs the initialization needed for file, registry, IPC, network, GUI, and other sandbox controls. For a process selected by `HostInjectProcess`, Sandboxie reuses the low-level SbieDll bootstrap but enters a loader-only host-injection path. The target keeps its existing process identity and token, remains outside normal sandbox process isolation, and loads the configured `HostInjectDll*` entries.

The related injection mechanisms have different targets and purposes:

| Mechanism | Target | Runtime context | Purpose |
| --- | --- | --- | --- |
| Normal SbieDll injection | A process being sandboxed | Normal Sandboxie initialization | Installs the Sandboxie runtime and its isolation hooks |
| `InjectDll*` | A normal sandboxed process | The sandboxed process's token and restrictions | Loads an additional configured DLL |
| `HostInjectProcess` with `HostInjectDll*` | A selected external host process | The host process's existing identity | Loads a trusted compatibility DLL without applying normal sandbox initialization |
| `SboxHostDll.dll` | The Office Click-to-Run host target | Host-injection context | Provides the current Office token-compatibility behavior |

Sharing part of the loader does not make these mechanisms equivalent.

## Host-injected processes

A host-injected process remains an external host process. This path does not add it to the normal Sandboxie Job Object, expose it as a normal sandboxed process, or initialize the normal file, registry, IPC, network, GUI, and thread handling used by sandboxed programs. Its primary token is not replaced by the reduced sandbox token.

Sandboxie associates the process with an effective configuration so it can select the relevant host-injection DLL entries. This internal association is not a normal sandbox identity. If a process is selected by a normal sandbox or force rule, it is handled as a sandboxed process instead; host-injection matching applies only when the process has not already been assigned to the normal sandbox execution path.

## `HostInjectProcess`

The setting accepts an executable-name pattern and an optional Windows service name:

```ini
HostInjectProcess=program.exe
HostInjectProcess=program.exe|ServiceName
```

The executable portion is matched case-insensitively against the base image name, not a full path. Sandboxie's normal pattern wildcards can be used, and multiple entries can be configured.

The optional value after `|` is the service name used for service lifecycle and restart handling. It is not an alternative process selector and does not participate in the driver's executable match. A service name without an executable pattern is therefore not useful configuration.

Host-injection settings can enter a box's effective configuration through normal configuration and template inheritance. If multiple enabled boxes provide a matching rule, the process is associated with one matching configuration; Sandboxie does not merge host-DLL lists from several boxes. Avoid competing matches in multiple boxes. `GlobalSettings` may participate through normal configuration fallback, but it does not itself become the process's sandbox.

## Host injection flow

```text
host process starts
        |
        v
normal sandbox and force rules are evaluated
        |
        v
HostInjectProcess matches the executable
        |
        v
Sandboxie marks the process for host injection
        |
        v
SbieSvc performs the low-level SbieDll bootstrap
        |
        v
SbieDll enters host-injection loader mode
        |
        v
matching HostInjectDll* entries are loaded
        |
        v
host compatibility DLL initializes
```

The driver evaluates the process-start configuration and coordinates the host-injection decision. SbieSvc carries out the process-injection request. SbieDll then runs its minimal host loader rather than the full sandbox initialization, and the loaded host DLL supplies the application-specific compatibility behavior.

## `HostInjectDll` architecture variants

Use the setting that matches the target process architecture:

| Target process architecture | Setting |
| --- | --- |
| x86 | `HostInjectDll` |
| x64 | `HostInjectDll64` |
| Native ARM64 | `HostInjectDllARM64` |

The target process and corresponding SbieDll architecture select the list; the operating system architecture alone does not. Entries are repeatable, are loaded in configuration order, and are not generically deduplicated. This mapping should not be read as a guarantee of full ARM64EC or CHPE compatibility.

After loading a configured DLL, Sandboxie checks for an optional `InjectDllMain` export or the applicable decorated form. When present, the callback receives access to the SbieDll instance or context used by the injection mechanism. The export is optional for a configured DLL; `SboxHostDll.dll` uses it for initialization. See [SBIE DLL API](SBIEDLLAPI.md) for the existing public callback guidance.

## DLL path requirements

Current host-injection entries use a leading backslash to resolve the DLL relative to the Sandboxie installation directory:

```ini
HostInjectDll=\SboxHostDll.dll
```

The same form applies to the other architecture-specific settings. The current host loader rejects arbitrary absolute paths, entries containing `..`, and entries that do not identify a `.dll`. Ordinary relative paths should not be used as public `HostInjectDll*` syntax.

## Relationship to `InjectDll`

[`InjectDll`](InjectDll.md) and [`InjectDll64`](InjectDll64.md) load additional DLLs into normal sandboxed processes. Those DLLs run under the process's effective sandbox token and Sandboxie restrictions, and their accepted path forms differ from host injection.

`HostInjectDll*` instead loads a DLL into an external process selected by `HostInjectProcess`. The process retains its existing identity and does not enter the normal sandbox path. The current host loader accepts only the Sandboxie-installation-relative form described above.

SandMan has no dedicated editor for `HostInjectProcess` or `HostInjectDll*`; they are normally supplied by a compatibility template or manual INI configuration. **Sandbox Options > Advanced Options > Dlls && Extensions** manages supported `InjectDll*` add-on entries, not host-injection settings.

## Microsoft Office Click-to-Run

The current shipped configuration uses host injection for Microsoft Office Click-to-Run compatibility:

```ini
HostInjectDll=\SboxHostDll.dll
HostInjectDll64=\SboxHostDll.dll
HostInjectDllARM64=\SboxHostDll.dll
HostInjectProcess=OfficeClicktoRun.exe|ClickToRunSvc
```

Here, `OfficeClicktoRun.exe` selects the process, `ClickToRunSvc` identifies the Windows service for lifecycle handling, and the setting for the target architecture loads `SboxHostDll.dll`. The Office compatibility template also supplies related IPC rules for Click-to-Run and App-V communication.

The compatibility template is detected separately through the presence of the `ClickToRunSvc` service. Template detection or activation supplies the configuration; runtime matching still uses the `OfficeClicktoRun.exe` executable pattern.

In the current shipped configuration, Microsoft Office Click-to-Run is the only built-in production use of `HostInjectProcess` and `SboxHostDll.dll` found in the repository. The settings provide infrastructure that can support other trusted compatibility components, but `SboxHostDll.dll` itself is not a general-purpose host-redirection or virtualization subsystem.

### `SboxHostDll.dll`

`SboxHostDll.dll` verifies that it is running in the intended Office Click-to-Run executable context, initializes through `InjectDllMain`, and installs its Office compatibility hook. It does not provide Sandboxie's file, registry, environment, process, COM, RPC, or App-V virtualization.

### Token compatibility

The current DLL hooks `OpenProcessToken` for an identity-compatibility case between Office Click-to-Run and sandboxed Office processes.

When Office Click-to-Run requests a token for a valid sandboxed process whose token uses Sandboxie's Anonymous Logon or Sandboxie-specific identity, the DLL looks for a corresponding host-side process with the same logon SID. If it finds one, it can return that host token instead. If no suitable replacement is found, the result from the original API call is retained.

## Service and process lifecycle

For targets that are Windows services, Sandboxie includes synchronization logic that can restart a configured service when host injection becomes active or its process selection changes. The service name after `|` exists for this SCM lifecycle handling.

Only Windows services participate in that automatic synchronization. An ordinary host process that is already running is not retroactively injected. Changes only to the `HostInjectDll*` list can also require a manual restart because service synchronization primarily detects whether SbieDll is present.

After changing `HostInjectProcess` or `HostInjectDll*`, restart the affected target process. Sandboxie can synchronize configured Windows services, but manually restarting the affected service is the most reliable way to ensure a changed host-DLL list is applied. A system reboot is not normally required.

## Security considerations

Configure only trusted DLLs supplied with Sandboxie or deliberately installed by an administrator. A host-injected DLL executes inside the target process with that process's existing identity and privileges; the normal reduced sandbox token is not applied to the target through this path.

Host injection does not grant `SYSTEM`, elevate the target by itself, bypass Windows service security, or represent a sandbox escape. It is a deliberate compatibility mechanism for loading trusted code into a selected external process. Protected Process and PPL restrictions are not bypassed, so a target that Sandboxie cannot normally open or manipulate may not be injectable.

`ProtectHostImages` is a separate image-protection feature. It prevents boxed DLLs or images from being mapped into certain sandboxed processes whose executable image comes from the host; it does not control `HostInjectDll*`. `NotifyImageLoadDenied` likewise belongs to that image-protection mechanism.

## Failure behavior

Failure of the service-side process injection can produce a Sandboxie injection error such as `SBIE2335`. Invalid host-DLL entries may be skipped, and a missing DLL or one built for the wrong architecture may fail to load. There is no single guaranteed recovery outcome for every target and injection stage: the target may continue or fail according to where the error occurs.

For the Office token hook, failure to find a suitable host-side replacement retains the original `OpenProcessToken` result.

## Sandboxie Plus and Classic

The driver, SbieSvc, SbieDll, and SboxHostDll are shared runtime components. SandMan provides the current Plus UI for compatibility templates and supported `InjectDll*` add-on entries, but it has no dedicated host-injection editor. Sandboxie Control Classic can also consume compatible templates and manual INI configuration through the shared runtime; the user interfaces are not identical.

## Applying configuration changes

Host-injection selection occurs when a target process starts, and the selected DLLs are loaded during that startup path. Restart affected processes after changing the settings. For a service target, manually restart the service when practical to ensure both process-selection and DLL-list changes take effect. Restarting SandMan, SbieSvc, the driver, or Windows is not normally necessary solely for a configuration change.

## Version history

- Host injection, `HostInjectProcess`, `HostInjectDll*`, and the Office `SboxHostDll.dll` implementation were already present in the initial public 5.40 source release. Their exact earlier proprietary introduction version is not established.
- Sandboxie Plus 0.7.2 / Classic 5.49.0 tightened `HostInjectDll` path restrictions so arbitrary absolute host paths were not accepted and host DLLs remained under the Sandboxie installation directory.
- Sandboxie Plus 1.2.0 / Classic 5.57.0 extended the SboxHostDll token compatibility behavior for Sandboxie-specific SIDs.
- Sandboxie Plus 1.5.0 added ARM64 `InjectDll` and `HostInjectDll` support.
- Sandboxie Plus 1.15.9 / Classic 5.70.9 added further protection against path traversal using `..`.
- Sandboxie Plus 1.15.10 / Classic 5.70.10 changed validation of injected-DLL entries.
- Sandboxie Plus 1.15.11 / Classic 5.70.11 fixed SboxHostDll injection into `OfficeClickToRun.exe`.
- Sandboxie Plus 1.16.9 / Classic 5.71.9 improved Office Click-to-Run and duplicate-hook reliability.

## Related pages

- [Code Injection](CodeInjection.md)
- [Inject Dll](InjectDll.md)
- [Inject Dll 64](InjectDll64.md)
- [SBIE DLL API](SBIEDLLAPI.md)
- [Sandboxie Ini](SandboxieIni.md)
