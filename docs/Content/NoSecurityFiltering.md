# No Security Filtering

_NoSecurityFiltering_ is an advanced compatibility setting for [Application Compartment](../PlusContent/compartment-mode.md) boxes. When it is effective, Sandboxie's driver disables its file, registry-key, and kernel-object filters for processes in the box.

> [!WARNING]
> This setting removes three central driver enforcement layers in a mode that already bypasses normal token restriction and Sandboxie Job Object assignment. Use it only for trusted applications whose compatibility requires these filters to be disabled.

## Prerequisite and syntax

```ini
[DefaultBox]
NoSecurityIsolation=y
NoSecurityFiltering=y
```

Both settings default to `n`. `NoSecurityFiltering` has its combined effect only while `NoSecurityIsolation=y` is active. It has no effect by itself in a standard-isolation sandbox.

## What it disables

With both settings enabled, the driver sets the same three internal filter-disable states controlled individually by:

- [Disable File Filter](DisableFileFilter.md);
- [Disable Key Filter](DisableKeyFilter.md);
- [Disable Object Filter](DisableObjectFilter.md).

The individual settings remain separate configuration keys. `NoSecurityFiltering` does not write or automatically add those keys to the sandbox configuration; it causes the equivalent three states to be enabled at runtime for an Application Compartment process.

The affected layers are specifically Sandboxie's driver-level:

- file filter;
- registry-key filter;
- kernel-object filter.

## What it does not mean

`NoSecurityFiltering` is not a universal switch for every Sandboxie hook, rule, or service. The setting should not be described as disabling all Sandboxie security or virtualization behavior. In particular, its current driver implementation does not itself disable every SbieDll hook, GUI restriction, network control, service behavior, or configuration rule.

Other mechanisms can therefore remain relevant, although the combination of Application Compartment and disabled driver filters provides substantially less protection than a standard sandbox.

## SandMan configuration

The control is under:

**Sandbox Options > Security Options > Security Isolation**

Its exact label is **Disable Security Filtering (not recommended)**. SandMan enables this checkbox only while **Disable Security Isolation** is selected.

## Version history

`NoSecurityFiltering` was introduced with Application Compartment in Sandboxie Plus 1.0.0 / Classic 5.55.0.

## Related pages

- [No Security Isolation](NoSecurityIsolation.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Disable File Filter](DisableFileFilter.md)
- [Disable Key Filter](DisableKeyFilter.md)
- [Disable Object Filter](DisableObjectFilter.md)
- [Sandboxie Ini](SandboxieIni.md)
