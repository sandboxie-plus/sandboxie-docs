# NT Namespace Isolation

_NtNamespaceIsolation_ controls Sandboxie's isolation of NT directory objects used as containers for named kernel objects. It is enabled by default.

This setting concerns the directory-object namespace used by named objects. It is not a switch for every form of inter-process communication (IPC).

## Usage

To disable the normal namespace-isolation behavior for a box:

```ini
[DefaultBox]
NtNamespaceIsolation=n
```

## Current behavior

With namespace isolation enabled, Sandboxie mediates operations involving NT directory objects, including the directory creation and open paths used by named kernel objects. Sandboxie normally redirects these objects into the sandbox namespace.

When the sandbox copy of a directory is unavailable, the SbieDll `NtOpenDirectoryObject` fallback can open the corresponding host directory. With namespace isolation enabled, that fallback reduces the requested access to query, traversal, and read-control rights. This prevents the normal user-mode fallback from obtaining create or other modification rights on the host directory.

This behavior helps prevent a sandboxed process from creating conflicting names in the host namespace. The Sandboxie Plus 1.8.0 / Classic 5.63.0 release described the protection as improving security and preventing name squatting.

## Disabling namespace isolation

`NtNamespaceIsolation=n` permits less restrictive access to host NT directory objects. This can improve compatibility for unusual named-object namespace scenarios, but it weakens Sandboxie's directory-object virtualization and name-squatting protection.

Disabling this setting does not disable every IPC restriction or every form of IPC isolation. IPC path rules and other Sandboxie controls remain separate.

## Alternate IPC naming

`UseAlternateIpcNaming` is a separate advanced naming mode introduced for Application Compartment boxes:

```ini
[DefaultBox]
NoSecurityIsolation=y
UseAlternateIpcNaming=y
```

Instead of placing Sandboxie-redirected named kernel objects below the normal separate NT directory-object namespace, Sandboxie derives a sandbox-specific suffix and appends it to redirected object names. In this mode, SbieDll does not install its normal directory-object namespace hooks because the redirected names use existing namespaces.

The setting changes Sandboxie's naming strategy for redirected named kernel objects. It does not rename every IPC protocol or every Sandboxie service endpoint.

`UseAlternateIpcNaming` is intended for Application Compartment boxes. The project warns that using it with a standard isolated box can result in the driver blocking access. It is not an alias for `NtNamespaceIsolation=n`, although alternate naming avoids the normal separate directory-object namespace path.

## Version history

| Setting or change | Version |
| --- | --- |
| NT directory-object namespace virtualization and `NtNamespaceIsolation` | Sandboxie Plus 1.8.0 / Classic 5.63.0 |
| `UseAlternateIpcNaming` | Sandboxie Plus 1.17.0 / Classic 5.72.0 |

## Related pages

- [No Security Isolation](NoSecurityIsolation.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
