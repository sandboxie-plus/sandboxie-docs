# Disable File Filter

_DisableFileFilter_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.9.0 / 5.51.0. It disables selected enforcement in Sandboxie's per-process driver file-filter layer (SbieDrv), not the separate file virtualization implemented by SbieDll.

## Usage

```ini
[DefaultBox]

DisableFileFilter=y
```

## Syntax

```ini
DisableFileFilter=<y/n>
```

Where:

- `y` bypasses the corresponding per-process driver file-policy checks.
- `n` is the consumer fallback and keeps those checks unless the combined `NoSecurityFiltering` condition below disables them.

## Behavior and boundaries

The driver file-filter callback remains registered. For an affected process, selected later policy checks are skipped, but earlier or independent checks can remain, including protected-root handling and file/process initialization checks. This setting does not unload the whole filter or remove every driver file check.

SbieDll file hooks and ordinary virtualization paths can remain active, including logical-to-sandbox path mapping, sandbox-copy creation, migration, and resource-rule matching. See [File Virtualization and Identity](FileVirtualization.md) for that separate layer.

Open and Read modes can select native host access attempts. Read's write restriction depends on driver enforcement. Closed can still be matched initially by SbieDll, but compatibility fallbacks mean that this is not a promise of final denial with the driver filter disabled. Retained DLL virtualization and rule matching do not provide equivalent independent security enforcement.

The setting does not itself grant Windows permissions, elevate the process, or remove token restrictions. Native operations remain subject to applicable Windows security checks and can still fail; direct host access or successful host writes are not guaranteed.

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

When [No Security Filtering](NoSecurityFiltering.md) is effective for a process in [Application Compartment](NoSecurityIsolation.md) mode, the driver enables the same file-filter disable state even if `DisableFileFilter=n`. This changes runtime state; it does not add `DisableFileFilter=y` to the configuration. `NoSecurityIsolation=y` alone does not disable this filter.

### Alternative Granular Controls

- **[DisableKeyFilter](DisableKeyFilter.md)**: Relaxes per-process driver Registry-key filtering.
- **[DisableObjectFilter](DisableObjectFilter.md)**: Relaxes the separate process/thread object-filter policy.
- **[NoSecurityFiltering](NoSecurityFiltering.md)**: Enables the file, Registry-key, and object-filter disable states for Application Compartment processes.
