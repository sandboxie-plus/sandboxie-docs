# File Virtualization and Identity

Sandboxie's normal filesystem virtualization presents a logical file path while the file's contents and metadata can come from different backing layers. A useful conceptual lookup order is:

```text
live sandbox state
    |
    v
active snapshot
    |
    v
parent snapshots
    |
    v
host or other resolved backing
```

Deletion and relocation state can suppress or redirect lower layers. Access rules can replace normal merged virtualization with another mode, and not every Windows API follows an identical path. This is a lookup model, not an invariant physical directory layout.

## Logical paths and sandbox storage

A sandboxed application normally continues using its logical path, while files created or migrated into the live sandbox are physically stored under the effective file-container root. The logical file and its sandbox representation can therefore reside on different volumes. See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) and [File Root Path](FileRootPath.md) for storage configuration.

Selected intercepted file-name and final-path queries translate sandbox-backed handles back toward the application's logical path. This does not guarantee that every API hides the physical sandbox path.

## Reading, creating, and modifying files

When no live sandbox representation shadows the path, an eligible read-only open can use the resolved backing object directly without first copying it into the live sandbox. That backing can be a host file, a snapshot, or another resolved or relocated source. Access mode, deletion state, snapshots, and compatibility paths can change the outcome; not every read uses this direct path.

An operation requiring mutable sandbox-local state generally needs a live representation. For an existing backing file, Sandboxie may migrate information into that representation before completing the operation. For a new logical file with no visible lower backing, the normal virtualized path creates the object in sandbox storage rather than creating the corresponding host file.

Once a usable live representation exists, it normally shadows the corresponding lower-layer object for ordinary virtualized access. The live file supplies its own contents and metadata for the relevant operation; Sandboxie does not merge its bytes with those of the lower file. Metadata-query fallback behavior is not identical across all APIs.

## Migration decisions

Migration is not always a full-content copy. Depending on the operation and policy, Sandboxie may create a copy containing the existing data, a representation without the previous contents, metadata or directory state, or specialized reparse-point state. For example:

- An ordinary modification can require copying existing contents.
- An overwrite can preserve metadata without first preserving the old contents.
- A delete-only open with delete-on-close can avoid copying file contents.
- Creating a directory representation does not recursively copy its children.

Streams and reparse points have specialized handling; this model is not a promise that every object type is copied identically.

When full-content migration is being considered, migration rules and the current size/prompt policy determine whether Sandboxie copies the contents, creates an empty representation, declines migration, or follows the applicable fallback. [File Migration Settings](FileMigrationSettings.md) covers configuration; [Copy Always](CopyAlways.md), [Copy Empty](CopyEmpty.md), and [Don't Copy](DontCopy.md) describe the individual migration rules. [Copy Newer](CopyNewer.md) is a separate refresh mechanism for an existing live copy.

When Sandboxie declines a requested content migration, [Copy Block Deny Write](CopyBlockDenyWrite.md) determines whether that path is denied or Sandboxie can retry the resolved backing with write/delete capabilities removed. The reduced-access retry can still fail, and the backing may be a snapshot or relocated source rather than the current host file. This refusal handling is not a fallback for every migration error.

Creating the representation or migrating data can fail. Native permissions and sharing behavior remain relevant, and migration is not a universal transaction that rolls back every intermediate filesystem change after a failure.

## Merged view, deletion, and snapshots

Directory enumeration can combine entries from live sandbox state, snapshot layers, and the host/backing layer. For the same logical name, the upper visible layer normally wins. Deletion state can suppress an entry that still physically exists below it. The resulting merged view lets an application use one logical namespace even though storage is distributed.

Deleting an existing host-backed file inside a normally virtualized sandbox does not require deleting the host object. Sandboxie records sandbox-side state that makes the lower object appear absent in the sandboxed view. V1 and V2 store that state differently; see [Virtualization Scheme V1 and V2](Delete-V2.md). This does not promise identical deletion visibility through every metadata API.

With [Box Snapshots](../PlusContent/BoxSnapshots.md), live changes sit above the active snapshot, and its parent snapshots can supply older backing. The host or other resolved backing is reached only when higher visible state does not supply or suppress the logical object. Modifying a snapshot-backed object can create or migrate a new live representation. Snapshot management and cleanup workflows are documented on the snapshot page.

## Effective file-access modes

| Effective mode | Architectural result |
| --- | --- |
| [Normal](NormalFilePath.md) | Use normal merged virtualization: lower backing can be read and mutable state is kept sandbox-side. |
| [Open](OpenFilePath.md) | Access the true/host path directly instead of normal copy virtualization for the matching operation. |
| [Closed](ClosedFilePath.md) | Deny the matching logical access before the ordinary copy path. |
| [Read](ReadFilePath.md) | Use direct true-path access for the read-oriented mode while applicable write enforcement remains separate. |
| [Write](WriteFilePath.md) | Hide ordinary lower backing data and operate on the sandbox/copy side. |

These are high-level effects after the effective rule has been selected. Rule precedence and nested exceptions are documented separately in [Rule Specificity](../PlusContent/RuleSpecificity.md). Closed access should not be interpreted as making every possible metadata query invisible, and these modes do not grant or bypass Windows ACL permissions.

Virtualization decides where logical state is read or stored. Sandboxie's access policy determines permitted operations and whether normal virtualization applies. Windows/filesystem permissions govern native access to the physical objects. Copy-on-write alone is not a complete security boundary.

## File identity and File IDs

A file presented on one logical volume can physically reside in sandbox storage on another. Returning raw physical File IDs everywhere can make identity and open-by-ID behavior inconsistent with that namespace. Sandboxie therefore adjusts IDs in selected query paths and has inverse handling for supported open-by-ID cases. This is compatibility and identity handling, not permission enforcement, encryption, or anonymization.

### Query coverage and backing identity

File ID virtualization is partial and API-dependent. Selected handle-based, name-based, and merged-directory query paths can adjust IDs as part of the virtualized view, but coverage is not uniform across every Windows information class or enumeration path. Current handling recognizes File-ID-bearing forms including `FileInternalInformation`, `FileAllInformation`, `FileIdInformation`, `FileStatInformation`, `FileStatLxInformation`, and `FileStatBasicInformation`; this list is not a guarantee that every query API accepts every form.

In the covered handle-query path, a direct host handle normally retains its native File ID, while a live or snapshot-backed boxed handle can receive Sandboxie's adjusted identity. A newly created sandbox-only file derives its identity from its own physical filesystem object; Sandboxie does not assign it a globally synthetic path-based ID. Migration does not promise to retain the host file's previous ID.

Directory-enumeration IDs should not be assumed identical to those returned by every handle- or name-based query. Current enumeration paths provide no universal cross-API identity guarantee: neither all host entries remaining native nor all entries being transformed is a safe assumption.

### Stability and open by ID

The transformation is deterministic for the underlying ID, but Sandboxie does not allocate a separate persistent synthetic identifier for each logical path. Do not rely on identity remaining stable across recreation, migration or CopyNewer replacement, snapshot switching, moving or recreating sandbox storage, recovery to the host, or filesystem changes. Restarting a process, SandMan, or the service does not itself introduce a new random identity seed in this mechanism.

For the supported open-by-ID path, Sandboxie can retry identity resolution and convert the result back into a logical path, after which ordinary sandbox path/rule handling applies. This does not bypass file rules or Windows access checks, or guarantee reopening the same physical snapshot layer originally queried.

Current handling does not establish universal 128-bit File ID round-trip semantics across every filesystem and query family, particularly where the higher portion of an identifier is significant. Applications should not assume all File ID APIs expose one fully synthetic, mutually interchangeable identity.

### Volume information

File-ID adjustment and volume information are separate mechanisms. Some file metadata can still reflect the physical backing volume, while selected volume queries may be redirected toward the logical drive. Sandboxie does not provide a completely synthetic filesystem volume identity.

## Applying configuration changes and lifecycle

Live migrated or created filesystem state persists in sandbox storage until changed, deleted, or reset through the relevant workflow. Deletion and snapshot state are also persistent sandbox state, subject to their own mechanisms.

Migration rules and limits are initialized and cached for sandboxed processes. Restart affected sandboxed processes after changing those settings to ensure the new values are used; this does not mean every migration-related decision is cached. An existing open handle continues referring to the object it already opened, rather than being retargeted by a configuration change. File ID transformation itself does not require a SandMan restart.

## Related pages

- [Use File Image](UseFileImage.md): image-backed storage changes the physical backing of sandbox file storage, not the logical backing-versus-live virtualization model described here.
- [File Recovery Architecture](RecoveryArchitecture.md): recovery is a separate host-side operation that moves a physical sandbox representation to a host destination. It does not grant the sandboxed process direct host-write permission or promise File ID preservation.
- [No Security Isolation](NoSecurityIsolation.md) and [Application Compartment](../PlusContent/compartment-mode.md): this mode changes important isolation/filtering behavior but does not globally remove SbieDll file virtualization.
