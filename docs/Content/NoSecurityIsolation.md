# No Security Isolation

_NoSecurityIsolation_ selects Sandboxie's **Application Compartment** mode. This mode favors compatibility by bypassing several security-isolation mechanisms used by a standard sandbox, but it does not disable every Sandboxie isolation or virtualization mechanism.

> [!WARNING]
> Application Compartment materially reduces isolation and is intended for trusted applications with compatibility requirements. File and registry virtualization can remain active, but virtualization alone should not be treated as a security boundary.

## Usage

```ini
[DefaultBox]
NoSecurityIsolation=y
```

The default is `n`. This is a box-wide setting.

## Token behavior

Application Compartment bypasses Sandboxie's normal restricted-primary-token replacement and normal impersonation-token validation and filtering paths.

This does not itself elevate a process. Instead, the process can retain the security context with which it was launched:

- an unelevated process remains unelevated;
- a process launched with an elevated token can retain that elevated context;
- the setting does not grant administrator or SYSTEM privileges.

This behavior overlaps with parts of the separate `OriginalToken` setting, but Application Compartment does not automatically add or enable `OriginalToken=y` in the sandbox configuration.

## Job Object behavior

Application Compartment processes are excluded from Sandboxie's normal root Job Object assignment. Consequently, the box-level process, memory, and CPU limits implemented through that Job Object do not apply in the usual way.

This does not prevent a process from belonging to a Job Object created or assigned by another component. For the complete Job Object model, see [Job Objects](JobObjects.md).

## Path-policy defaults

Application Compartment relaxes three specific Sandboxie path-policy defaults:

- the normal `AlwaysCloseForBoxed` behavior is not applied;
- the normal `DontOpenForBoxed` behavior is not applied;
- `ProtectHostImages` is not applied.

These changes do not mean that every resource rule is ignored. Other configured access rules, built-in template rules, and active filtering layers can still affect access.

Sandboxie also loads the built-in `TemplateAppCPaths` rules for Application Compartment processes. These are template path policies for this box type; they do not disable all resource isolation.

## Isolation that can remain active

In an ordinary Application Compartment configuration:

- file-system and registry virtualization can remain active;
- Sandboxie's file, registry-key, and kernel-object driver filters remain active unless disabled separately;
- configured file, registry, IPC, network, and GUI rules can still apply;
- named-object namespace handling remains subject to settings such as [Nt Namespace Isolation](NtNamespaceIsolation.md).

`NoSecurityIsolation=y` alone does not set Sandboxie's file-, key-, or object-filter disable states. The separate [No Security Filtering](NoSecurityFiltering.md) setting can disable those three driver filters while Application Compartment is active.

## Named-object namespace options

Application Compartment normally continues to use Sandboxie's named kernel-object redirection and NT directory-object namespace handling. Advanced configurations can use `UseAlternateIpcNaming=y` to change the naming strategy for Sandboxie-redirected named objects instead of using the normal separate directory-object namespace.

`UseAlternateIpcNaming` is intended specifically for Application Compartment boxes. It does not rename every IPC protocol or disable every IPC control. See [Nt Namespace Isolation](NtNamespaceIsolation.md#alternate-ipc-naming) for details.

## Unsupported DynData fallback

When compatible DynData is unavailable, current driver code can force the affected process into the reduced-isolation Application Compartment state and emit warning `MSG_1207`. This changes the driver's process state; it does not write `NoSecurityIsolation=y` to the sandbox configuration.

## SandMan configuration

Application Compartment can be selected as a box type in SandMan. The corresponding advanced setting is under:

**Sandbox Options > Security Options > Security Isolation**

The checkbox label is **Disable Security Isolation**. The current SandMan box-type selector calls the preset **Application Compartment**, while the New Box Wizard calls it **Application Compartment Box**. SandMan treats this mode as a supporter feature.

## Version history

Application Compartment and `NoSecurityIsolation` were introduced in Sandboxie Plus 1.0.0 / Classic 5.55.0. Sandboxie Plus 1.8.0 moved the built-in Application Compartment access rules into `TemplateAppCPaths`.

## Related pages

- [Application Compartment](../PlusContent/compartment-mode.md)
- [No Security Filtering](NoSecurityFiltering.md)
- [Nt Namespace Isolation](NtNamespaceIsolation.md)
- [Job Objects](JobObjects.md)
- [Sandboxie Ini](SandboxieIni.md)
