# Sandbox Roots and Volume Layout

Sandboxie uses separate roots for a box's file container, mounted registry hive, and named-object namespace. These settings select locations and layout; they do not themselves grant access to host files, registry keys, or IPC objects. The paths below are defaults, not an invariant description of every configured box.

## The three sandbox roots

| Root | Default | Purpose |
| --- | --- | --- |
| [`FileRootPath`](FileRootPath.md) | `\??\%SystemDrive%\Sandbox\%USER%\%SANDBOX%` | File container holding redirected files and the `RegHive` file. |
| [`KeyRootPath`](KeyRootPath.md) | `\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%` | Registry location where that hive is mounted. |
| [`IpcRootPath`](IpcRootPath.md) | `\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%` | NT namespace root for sandboxed named objects; its default includes the session. |

The root strings are expanded for the box and normalized, including conversion of suitable DOS file paths to NT paths and removal of duplicate or trailing backslashes. Useful substitutions include `%SANDBOX%`, `%USER%` (or `%USERNAME%`), `%SID%`, and `%SESSION%`; file locations can also use `%SystemDrive%`, `%SBIEHOME%`, and appropriate shell-folder variables. `%BOXNAME%` is **not** a supported alias for `%SANDBOX%` in this root expansion path. Expansion does not make an arbitrary registry, IPC, or file-root value valid.

## File-root selection and legacy fallback

Sandboxie first looks for an effective `FileRootPath`. Only if none is available does it look for an effective, deprecated [`BoxRootFolder`](BoxRootFolder.md), append `\Sandbox\<box name>`, and use that as the file root. If neither setting is available, it uses the built-in default above. “Effective” includes the box's settings, applicable enabled templates, and `[GlobalSettings]` fallback: a global `FileRootPath`, for example, wins over a box-local `BoxRootFolder`. Use `FileRootPath` for new configurations.

## File layout

With the default layout, a box's file root can contain:

```text
FileRootPath\
  drive\C\...                 local files on drive C:
  user\current\...           current user's profile files
  user\all\...               shared/all-users profile files
  user\public\...            public profile files, where available
  share\server\share\...     network-share files
  RegHive                     sandboxed registry hive
```

Other drives appear under their own letters. Windows may also maintain files associated with `RegHive`. The [Sandbox Hierarchy](SandboxHierarchy.md) page explains the normal redirection examples; the settings below can change the file-side folder names without changing the host paths applications use.

## User-profile layout

[`SeparateUserFolders`](SeparateUserFolders.md) defaults to `y`. When enabled, Sandboxie maps recognized profile paths to portable `user\current`, `user\all`, and, where available, `user\public` locations. With `n`, it does not initialize those special profile mappings, so an ordinary local profile path follows the drive layout, such as `drive\C\Users\...`. This does not change Windows profiles or account permissions.

## Drive identity in the sandbox

`UseVolumeSerialNumbers` defaults to `n`. With `y`, a known drive letter is followed by the Windows filesystem volume serial when one can be read: `drive\C` becomes, for example, `drive\C~1234-ABCD`. The letter remains part of the name; if the serial is unavailable or zero, no suffix is added. This helps distinguish removable volumes that reuse a letter, but is not a guarantee against every collision or a security boundary. It does not use a physical disk's firmware serial, hide disk identity, or change the `share` layout.

## Volumes without drive letters

`UseVolumeGuidWhenNoLetter` defaults to `n`. For a volume mounted in directories but not assigned a drive letter, the default layout uses the first mounted directory as the box location for that volume and maps its other mount points there. With `y`, Sandboxie can instead use a folder of the form `drive\{volume-guid}` and map the mounted directories to it. A normal drive-letter mapping still takes precedence; the GUID setting is not a new layout for all drives. Its result depends on the volume and mount points Windows exposes.

## Changing roots or layout

Changing a root or layout setting changes where future operations look for or place sandbox data; it does **not** automatically move existing content. In particular, switching `SeparateUserFolders` or `UseVolumeSerialNumbers` on a populated box can leave files under the previous folder names. SandMan disables both checkboxes when the box is not empty. Use layout options on an empty box. If existing data must be preserved, handle it separately; changing these settings does not migrate it. Changing `FileRootPath` in configuration alone does not relocate the old file container. Changing `KeyRootPath` while the old hive is mounted can also conflict with the hive already in use.

Recovery path mapping uses the layout currently recognized for the box; content left under an older layout is not migrated by changing these settings. Cleanup behavior is a separate topic.

## Verbose volume checks

`EnableVerboseChecks` defaults to `n`. Its metadata and historical changelog describe an optional warning (`SBIE2227`) about short-name (8.3) creation on the containing volume. In the current implementation, the hive-mounted handler passes the **registry** root, not the file root, to a DOS-path conversion before the volume check. The normal `KeyRootPath` cannot pass that conversion, so the 8.3 test and warning are not reached for ordinary boxes even with `EnableVerboseChecks=y`. Do not rely on this option as a working check of the file-container volume. If the test is reached through an unusual configuration, it queries the volume's short-name-creation state, not whether particular 8.3 names already exist.

## Applying changes

The root paths are resolved when Sandboxie constructs the box path information. The three DLL file-layout options are read when a sandboxed process initializes its file handling. Existing initialized processes do not rebuild those mappings merely because the configuration changes; restart affected sandboxed processes, and avoid changing a mounted or populated box in place. Device-change notifications can refresh drive-letter information within a process, but do not re-read the option values.

SandMan exposes global root defaults at **Global Settings > Advanced Config > Sandboxie Config** and offers per-box root entries in **Sandbox Options > Advanced Options > Miscellaneous > Add Option**. The New Box wizard also offers a file-container location. The two main file-layout checkboxes are under **Sandbox Options > File Options**. `UseVolumeGuidWhenNoLetter` and `EnableVerboseChecks` have no dedicated checkboxes; advanced configuration can be entered manually.

## Version history

- `SeparateUserFolders=n` was added in Sandboxie Plus 0.2.2 / Classic 5.41.2.
- `UseVolumeSerialNumbers=y` was added in Plus 0.8.0 / Classic 5.50.0 to help avoid mixing data from removable volumes reusing a letter.
- `EnableVerboseChecks=y` became the opt-in form of the historical `SBIE2227` check in Plus 1.7.2 / Classic 5.62.2; the current runtime limitation above takes precedence over that historical description.
- `UseVolumeGuidWhenNoLetter=y` became the opt-in GUID layout in Plus 1.13.1 / Classic 5.68.1 after the newer no-letter layout was reverted.

## Related pages

- [File Root Path](FileRootPath.md), [Box Root Folder](BoxRootFolder.md), [Key Root Path](KeyRootPath.md), and [Ipc Root Path](IpcRootPath.md) cover the individual root settings.
- [Separate User Folders](SeparateUserFolders.md) and [Sandbox Hierarchy](SandboxHierarchy.md) explain the ordinary file layout in more detail.
- [Sandboxie Ini](SandboxieIni.md) explains box and global configuration.
