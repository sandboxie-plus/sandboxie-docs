# Virtualization Scheme V1 and V2

Sandboxie offers two schemes for recording deletions and certain renames inside a sandbox. The scheme changes how sandbox-side file and registry state is represented; it does not change the basic rule that deleting a host-backed item inside the sandbox does not delete the host item.

## Settings

The filesystem and registry schemes are selected independently in [Sandboxie.ini](SandboxieIni.md):

```ini
UseFileDeleteV2=y
UseRegDeleteV2=y
```

`UseFileDeleteV2` selects the V2 filesystem scheme; `UseRegDeleteV2` selects the V2 registry scheme. Set either option to `n` to select V1 for that subsystem. The options can be set for a box or inherited from `[GlobalSettings]`; an explicit box-level `n` can override a global `y`.

## Version 1

The older V1 scheme remains supported. For files and directories, Sandboxie represents a deletion with a sandbox-side placeholder marked by a special **creation time**. When a host-backed directory is deleted, the sandbox-side directory can remain as the marked placeholder; the host directory is not changed. V1 also checks sandbox-side parent markers when resolving affected paths.

Registry V1 uses a different representation: a deleted sandbox copy of a key is marked through its **last-write time**. A deleted registry value is instead represented by a sandbox-side value with a special type. Files, keys, and values should therefore not be thought of as sharing one identical kind of dummy object.

## Version 2

V2 keeps path state separately from ordinary sandbox file and registry objects:

| Subsystem | Setting | Runtime-maintained state file |
| --- | --- | --- |
| Filesystem | `UseFileDeleteV2=y` | `FilePaths.dat` |
| Registry | `UseRegDeleteV2=y` | `RegPaths.dat` |

For the filesystem, `FilePaths.dat` records deleted-path state and relocation mappings. A deletion can mark a path in this metadata, and path lookups can recognize a deleted parent. Relocation mappings help Sandboxie continue to present underlying host content at a renamed sandbox-visible location, notably when a host-backed folder is renamed inside the box. Not every rename needs such a mapping.

For the registry, `RegPaths.dat` records deletion state for **both keys and values**, as well as key relocation mappings. Registry V2 provides the relocation handling used by Sandboxie's supported sandboxed `NtRenameKey` path. Neither data file is an INI setting or a file intended for manual editing.

The two files are sandbox content. Do not manually edit or remove them from a non-empty box to change its scheme or reset individual deletions. Their absence in a newly initialized V2 box does not, by itself, mean V2 is disabled; Sandboxie can create a missing state file as needed.

## Rename compatibility

V1's marker-based hierarchy could lose the expected view of host content after some sandboxed renames. For example, a reported case involved renaming a host-backed folder inside the box and no longer seeing its host-side children under the new name. V2's filesystem relocation state addresses that class of case. Registry V2 similarly enables Sandboxie's sandboxed key-rename handling. This does not mean every V1 rename fails or every rename creates relocation metadata.

## Raw settings and SandMan's paired scheme

Raw configuration can mix the two schemes, such as filesystem V2 with registry V1. SandMan's **Virtualization scheme** control instead treats them as a pair:

| SandMan display | Effective `UseFileDeleteV2` | Effective `UseRegDeleteV2` |
| --- | --- | --- |
| Version 1 | `n` | `n` |
| Version 2 | `y` | `y` |
| Indeterminate | Different values | Different values |

The table describes effective values, including inherited global settings, not necessarily two explicit lines in the box section. Selecting Version 2 writes both settings as `y`. Selecting Version 1 removes a local setting when its global fallback is already false, or writes an explicit local `n` when needed to override a global `y`.

### Two different defaults

These defaults apply at different layers:

* **Runtime fallback:** when an effective `UseFileDeleteV2` or `UseRegDeleteV2` value is absent, Sandboxie's runtime uses `false` for that setting, selecting V1 for that subsystem.
* **New Box Wizard:** current SandMan initially selects **Version 2** and writes both V2 settings when a box is created with that selection. The wizard can remember a user's chosen box-scheme default for later boxes, so a user who changes that default can have Version 1 preselected instead.

Thus a box with no effective V2 settings uses V1, while a newly created SandMan box normally has explicit V2 settings. V2 is the wizard's initial choice, **not** the low-level missing-setting default.

## Changing the scheme in SandMan

Open **Sandbox Options > File Options > Box Structure > Virtualization scheme**. SandMan offers **Version 1** and **Version 2** and shows **Indeterminate** when the effective file and registry choices differ.

> [!WARNING]
> SandMan enables the scheme control only when the sandbox is empty. Empty the sandbox before changing schemes through SandMan. Changing the raw INI settings of a populated box is not an in-place conversion of its existing deletion and relocation state.

The settings are read when a sandboxed process initializes its file and registry handling. Restart affected sandboxed processes after a scheme change; no SandMan, service, or driver restart is normally needed. SandMan still offers V1 as a compatibility choice.

## Snapshots

V2 state is part of sandbox content, including snapshot handling. Snapshot creation includes the available `FilePaths.dat` and `RegPaths.dat` data files, and snapshot merge has specific handling for filesystem V2 path state. This page does not prescribe manual manipulation of those files; see [Box Snapshots](../PlusContent/BoxSnapshots.md) for snapshot operations.

## Version history

| Release | Change |
| --- | --- |
| Sandboxie Plus 1.1.0 / Classic 5.56.0 | Introduced the V2 settings and state files, filesystem folder-rename improvements, and sandboxed `NtRenameKey` support with registry V2. |
| Sandboxie Plus 1.8.2 / Classic 5.63.2 | Fixed a reported `UseRegDeleteV2=y` compatibility issue. |
| Sandboxie Plus 1.10.1 / Classic 5.65.1 | Changed `FilePaths.dat` to normally persist drive-letter paths while retaining compatibility with older NT-path entries. |

## Related pages

* [Sandboxie Ini](SandboxieIni.md)
* [Box Snapshots](../PlusContent/BoxSnapshots.md)
