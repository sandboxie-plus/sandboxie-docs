# Registry Virtualization

Sandboxie does not maintain a complete independent clone of the host Registry. Normal virtualization combines sandbox registry changes with eligible host data, using registry access rules and deletion or relocation state to construct the application's view.

SbieDll performs the main logical path mapping and supported merge operations. SbieDrv provides separate Registry filtering and manages the sandbox hive's mount lifecycle together with SbieSvc. SandMan configures these mechanisms; it does not perform application registry merging.

## Registry roots and RegHive

The registry mount location and its backing file are different:

| Location | Purpose |
| --- | --- |
| [`KeyRootPath`](KeyRootPath.md) | Registry namespace where the sandbox hive is mounted. |
| `FileRootPath\RegHive` | Physical backing file beneath the sandbox file root. |

Changing either root does not automatically migrate existing sandbox content. See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) for root configuration and layout.

[Image-backed storage](UseFileImage.md) can change the physical storage carrying the sandbox file root and therefore `RegHive`, but `KeyRootPath` remains the Registry namespace where the hive is mounted.

## Logical and sandbox registry paths

Applications continue to use logical host-style registry names. Sandboxie maps the corresponding sandbox state beneath the mounted hive, for example:

```text
\REGISTRY\MACHINE\Software\Vendor
    -> <KeyRootPath>\machine\Software\Vendor
```

HKLM corresponds to the sandbox `machine` branch. For HKCU, the host-side current-user SID corresponds to the sandbox `user\current` branch. The filesystem's `SeparateUserFolders` option does not change this registry mapping.

HKCR is Windows' Classes view, not one independent uniform Sandboxie root. Windows' machine/per-user Classes merge and Sandboxie's sandbox-side Classes mapping are separate relationships. Sandbox customization can link `user\current\software\classes` to `user\current_classes` within the sandbox hive.

## Reading and writing keys

With normal virtualization, a read-only open of an existing host-only key can use the host key without first creating the corresponding sandbox key. A create operation can instead create sandbox-side structure even when its requested access is read-oriented.

Normal create and writable-open operations can materialize the relevant hierarchy inside the sandbox hive while leaving the host key unchanged. This does not clone all host values, the entire host subtree, or the exact host security descriptor. Host existence can still affect the logical create/open result.

A value write through a handle initially opened for host reading can be retried through the sandbox writable path when the native write is denied. This is conditional handling, not a promise that every failed operation is retried.

## Merged keys and values

A sandbox key can contain only sandbox changes rather than a full copy of its host counterpart:

```text
logical registry key
    +-- sandbox hive keys and values
    +-- eligible host keys and values
    +-- deletion / relocation state
```

This describes selected supported Registry data operations, not a universal synthetic object used by every Registry API.

- Sandbox-only values are visible in the sandbox view.
- Eligible host-only values remain visible when the selected access mode permits them.
- A same-named sandbox value takes precedence in the merged result.
- Supported subkey enumeration can combine host and sandbox names, coalescing same-named entries.
- Recognized deletion state can suppress host keys or values.

Registry queries are operation- and information-class-dependent. Some return native information from the opened object, some synthesize the logical key name, and selected full/cached information is calculated from the merged view. Enumeration is not one atomic snapshot of both layers, and metadata is not uniform across every API.

## Deletion and rename state

Registry V1 stores deletion markers inside `RegHive`, with different markers for keys and values. Registry V2 uses `RegPaths.dat` below the sandbox file root to record logical key/value deletion and key relocation state alongside the ordinary sandbox registry data. See [Virtualization Scheme V1 and V2](Delete-V2.md).

Registry V2 provides the path-state/relocation mechanism used by Sandboxie's sandboxed key-rename handling. This is not a guarantee that every rename succeeds or is atomic. V1 lacks that relocation mechanism, but this does not mean every native rename fails.

Recreating registry content can make new sandbox data visible again, but deletion-state and metadata handling are API-dependent, especially with V2. Do not rely on recreation as an exact restoration of the previous host view.

Sandbox processes load V2 path-state data and can detect some later changes to `RegPaths.dat`. These updates should not be treated as transactional, instantly coherent across every process, or durably atomic. The file is sandbox content, not a configuration file intended for manual editing.

## Registry access modes

The following describes the selected mode for ordinary hooked access:

| Effective mode | High-level behavior |
| --- | --- |
| Normal | Use normal sandbox registry virtualization and supported merge behavior. |
| [Open](OpenKeyPath.md) | Use the host Registry directly for the selected rule. |
| [Open for All](OpenConfPath.md) | Use the same direct-host model, with eligibility for boxed executables as well. |
| [Closed](ClosedKeyPath.md) | Deny a new hooked registry open/create when this mode wins. |
| [Read](ReadKeyPath.md) | Use the host Registry directly while active Registry filtering normally prevents host modification. |
| [Write / Box Only](WriteKeyPath.md) | Hide ordinary host data and use sandbox-side Registry state. |
| [Normal override](NormalKeyPath.md) | Restore normal virtualization when the Normal rule wins. |

The winning mode depends on process selectors and resource-rule matching; see [Rule Specificity](../PlusContent/RuleSpecificity.md).

Ordinary Open entries are normally subject to the boxed-executable eligibility restriction. Open for All is loaded outside that normal gate, but does not automatically win against another rule or bypass Windows permissions.

For a new hooked open/create, Closed is checked before the normal sandbox-copy path. A sandbox copy therefore does not automatically exempt that open from Closed. Already-open handles are separate.

Read selects the direct host path in SbieDll. In a standard sandbox with Registry filtering active, its read-only restriction normally depends on the driver. Disabling relevant filtering changes that enforcement assumption; native Windows permissions still apply.

Write / Box Only does not mean applications cannot read their sandbox-side data. More-specific accessible descendants can still affect the visible structure according to rule matching.

## WOW64 registry views

Sandboxie resolves the selected Windows 32/64-bit Registry view before constructing the sandbox counterpart. The canonical path can contain `Wow6432Node`, which can therefore appear in sandbox-side paths where appropriate. Not every Registry location has separate 32-bit and 64-bit storage.

## Hive lifecycle

During sandbox process initialization, Sandboxie prepares or accesses `RegHive`, mounts it at `KeyRootPath`, and associates the process with the shared mount. Multiple sandbox processes can share the same hive. References are released as processes end, and unload is coordinated when the hive becomes eligible.

Unload is not necessarily immediate after the last process exits. Busy state, remaining handles, failures, and lifecycle options can affect it. A corrupt or unloadable hive, a conflicting root/backing association, or storage failures can prevent successful registry initialization or affect later operations. See [SBIE1241](SBIE1241.md) for mount diagnostics.

`RegHive` and available `RegPaths.dat` participate as sandbox registry data in [snapshot workflows](../PlusContent/BoxSnapshots.md). This is separate from the logical host/sandbox merge used by application registry operations.

## Applying configuration changes

- Registry access-rule lists are initialized per process. Restart the affected sandbox process tree to apply rule changes reliably.
- `UseRegDeleteV2` is selected during process initialization. Restart affected processes after changing it; changing the setting is not an in-place conversion of a populated box's deletion state.
- `KeyRootPath` is established as part of the box/mount context. Stop affected box processes before changing it; changing the path does not migrate `RegHive` or its contents.
- `RegPaths.dat` may be reloaded after detected backing-file changes, without an immediate or bounded synchronization guarantee.

Existing registry handles continue to reference the object and access already opened. Configuration changes do not universally retarget or revoke them. A Windows reboot, SandMan restart, or service restart is not a blanket requirement for these changes.

## Security boundaries

Registry virtualization determines data presentation and storage. Registry rule selection, SbieDrv filtering, Windows security descriptors, and process-token isolation are separate mechanisms. The merged view is not by itself a complete host-protection boundary, and `RegHive` does not replace Windows access checks.

[Application Compartment](NoSecurityIsolation.md) can retain registry virtualization while changing security isolation. In that mode, [`NoSecurityFiltering`](NoSecurityFiltering.md) can disable the driver Registry filter; `DisableKeyFilter` can also affect that layer. This should not be read as disabling every SbieDll registry hook.

Open rules deliberately permit direct host Registry access where native permissions allow it. Normal-mode isolation assumptions must not be applied to those direct-access rules or to configurations that disable relevant enforcement.

## Related pages

- [Key Root Path](KeyRootPath.md) and [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md)
- [Virtualization Scheme V1 and V2](Delete-V2.md)
- [Rule Specificity](../PlusContent/RuleSpecificity.md)
- [Box Snapshots](../PlusContent/BoxSnapshots.md)
- [Use Object Name For Keys](UseObjectNameForKeys.md) for registry-name lookup compatibility
