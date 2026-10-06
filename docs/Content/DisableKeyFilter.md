# Disable Key Filter

_DisableKeyFilter_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.9.0 / 5.51.0. It disables selected enforcement in Sandboxie's per-process driver Registry-key filtering layer (SbieDrv), not the separate Registry virtualization implemented by SbieDll.

## Usage

```ini
[DefaultBox]

DisableKeyFilter=y
```

## Syntax

```ini
DisableKeyFilter=<y/n>
```

Where:

- `y` bypasses the corresponding per-process driver Registry-key policy checks.
- `n` is the consumer fallback and keeps those checks unless the combined `NoSecurityFiltering` condition below disables them.

## Behavior and boundaries

The Registry callback remains registered. For ordinary sandboxed open/create requests, the process flag skips its normal driver path-policy enforcement. Other Registry handling, process initialization, and sandbox-hive setup remain separate; this setting does not disable the hive or remove every Registry check.

SbieDll Registry initialization and hooks can remain active, including logical-to-sandbox path mapping, sandbox Registry hierarchy creation, supported merged views, and resource-rule matching. See [Registry Virtualization](RegistryVirtualization.md) for that separate layer.

Open and Read modes can select direct native host paths. Read's write restriction depends on driver enforcement. Closed can still be matched initially by SbieDll, and Write / Box Only can still influence covered virtualization paths. However, compatibility fallbacks mean that an initial Closed denial is not a promise of final denial with the driver filter disabled. Retained DLL virtualization and rule matching do not provide equivalent independent security enforcement.

The setting does not itself grant Registry permissions, elevate the process, or remove token restrictions. Native operations remain subject to applicable Windows security checks and can still fail; successful host Registry writes or key creation/opening are not guaranteed.

## Security Implications

> [!WARNING]
> Disabling this independent driver enforcement layer substantially weakens protection. Use it only for trusted applications with a specific compatibility requirement, not for untrusted software. Continued DLL virtualization is not a substitute for the disabled enforcement.

## Configuration scope

The driver reads an effective box Boolean: enabled templates and `[GlobalSettings]` fallback can contribute. If no effective value is configured, the consumer fallback is `n`. This consumer does not support program/image, ProcessGroup, or negated selectors.

## Applying changes

The effective filter state is stored for each sandboxed process during process creation. Configuration reload does not rewrite this state for existing processes.

Start new affected processes after changing the effective value; restart the affected sandboxed process tree when testing the change consistently. A SandMan, service, driver, or Windows restart is not normally required for this setting.

## Related Settings

### Master Override

When [No Security Filtering](NoSecurityFiltering.md) is effective for a process in [Application Compartment](NoSecurityIsolation.md) mode, the driver enables the same Registry-key filter-disable state even if `DisableKeyFilter=n`. This changes runtime state; it does not add `DisableKeyFilter=y` to the configuration. `NoSecurityIsolation=y` alone does not disable this filter.

### Alternative Granular Controls

- **[DisableFileFilter](DisableFileFilter.md)**: Relaxes per-process driver file filtering.
- **[DisableObjectFilter](DisableObjectFilter.md)**: Relaxes the separate process/thread object-filter policy.
- **[NoSecurityFiltering](NoSecurityFiltering.md)**: Enables the file, Registry-key, and object-filter disable states for Application Compartment processes.
