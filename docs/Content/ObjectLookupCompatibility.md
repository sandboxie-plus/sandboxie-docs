# Object Lookup Compatibility

`UseDriverObjLookup` and `UseObjectNameForKeys` are advanced compatibility settings for how Sandboxie obtains names from existing object and registry-key handles. Both are disabled by default. They change name resolution inside Sandboxie, not the rules that grant or deny access to files, registry keys, or named objects.

## Object-name lookup in Sandboxie

Some Sandboxie path-processing operations need the name associated with an open handle. Sandboxie's internal `Obj_GetObjectName` helper normally asks Windows for `ObjectNameInformation` through `NtQueryObject`. Other internal file, IPC, and selected security-object paths also use this helper. This is distinct from Sandboxie's hook for an application's own `NtQueryObject` calls: enabling `UseDriverObjLookup` does not reroute every such call through the driver.

## UseDriverObjLookup

In a standard sandbox, `UseDriverObjLookup=y` makes Sandboxie's internal object-name helper ask the Sandboxie driver to resolve a handle's name instead of using its normal user-mode `NtQueryObject` lookup:

```ini
[DefaultBox]
UseDriverObjLookup=y
```

This is an opt-in workaround for specific handle and I/O conditions under which an object-name query can hang, notably a synchronous pipe handle with a pending read. It is not a general performance option or a guarantee against every object-lookup problem. The driver resolves the supplied handle's name using its own object-name path, with special handling for some file objects. If that lookup fails, the helper returns the failure; it does not retry the native `NtQueryObject` path.

Application Compartment does not enable this driver-assisted helper path, even if `UseDriverObjLookup=y` is configured. Its `Obj_GetObjectName` calls continue to use the native path.

## UseObjectNameForKeys

When a registry operation supplies a `RootDirectory` key handle and a relative name, Sandboxie obtains the root key's full name before appending the relative part. By default, `Key_GetName` obtains that root name through `NtQueryKey(KeyNameInformation)`. `UseObjectNameForKeys=y` instead sends this root-handle lookup through `Obj_GetObjectName`:

```ini
[DefaultBox]
UseObjectNameForKeys=y
```

The option does not replace all `NtQueryKey` calls or change registry access rules. When an operation has no root handle, this choice is not involved in constructing its path.

The alternative was retained for compatibility after an earlier `NtQueryObject`-based root lookup was reverted: it had addressed a case where `NtQueryKey` could fail for some keys, but caused problems on Windows 10 version 1803 and older. That is historical context, not a recommendation to enable it on a particular Windows version today.

## How the settings interact

| `UseObjectNameForKeys` | `UseDriverObjLookup` | Registry root-handle name lookup |
| --- | --- | --- |
| `n` | Either value | `NtQueryKey(KeyNameInformation)`. The driver setting can still affect other internal `Obj_GetObjectName` callers. |
| `y` | `n` | `Obj_GetObjectName`, using native `NtQueryObject(ObjectNameInformation)`. |
| `y` | `y`, standard sandbox | `Obj_GetObjectName`, using the driver-assisted lookup. |
| `y` | `y`, Application Compartment | `Obj_GetObjectName`, using native `NtQueryObject`; the driver-assisted helper path remains disabled in this mode. |

Neither setting requires the other to be enabled. A failed selected lookup is returned as a failure to its caller rather than automatically switching to the other lookup method.

## Applying changes

These are box-wide yes/no settings, not executable-qualified or process-group rules. The effective value can come from the box, `[GlobalSettings]`, or an applicable enabled template. Sandboxie reads each value while initializing its DLL in a sandboxed process, so restart affected sandboxed processes after changing it. A driver, service, or Windows restart is not normally required for the new process to read the changed configuration.

SandMan has no dedicated checkbox for either setting and does not list them among the built-in advanced-option suggestions. Its **Sandbox Options > Advanced Options > Miscellaneous > Add Option** field accepts a manually entered option name; the examples above also show the direct `Sandboxie.ini` form.

## Version history

- `UseObjectNameForKeys` was added as an opt-in compatibility setting in Sandboxie Plus 0.8.8 / Classic 5.50.8.
- `UseDriverObjLookup` was added for the rare object-name-query hang scenario in Sandboxie Plus 1.10.3 / Classic 5.65.3.

## Related pages

- [Sandboxie Ini](SandboxieIni.md) explains box configuration and inheritance.
- [Key Root Path](KeyRootPath.md) describes where a sandbox registry hive is mounted; it does not select a root-handle lookup method.
- [NT Namespace Isolation](NtNamespaceIsolation.md) concerns isolation of named-object directories, not lookup of an existing handle's name.
