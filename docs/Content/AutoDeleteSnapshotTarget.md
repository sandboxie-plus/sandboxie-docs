# AutoDeleteSnapshotTarget

*AutoDeleteSnapshotTarget* is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.18.2. It selects the retained snapshot state to which SandMan returns after automatically deleting a sandbox's contents.

This setting does not enable automatic deletion and does not delete the selected snapshot. It matters only when [Auto Delete](AutoDelete.md) is enabled and the sandbox has retained snapshots.

## Usage

```ini
[DefaultBox]
AutoDelete=y
AutoDeleteSnapshotTarget=Current
```

The valid values are `Current` and `Default`. Boolean values such as `y` and `n` are not valid.

## Restore targets

### Current

`AutoDeleteSnapshotTarget=Current` returns the sandbox to its currently active snapshot state after automatic deletion. The active state may also be the empty-box state. Live changes made above that state are discarded, while the saved snapshot tree is retained.

### Default

`AutoDeleteSnapshotTarget=Default` returns the sandbox to the snapshot marked as the default. If no default snapshot is configured, it returns to the empty-box state. The default snapshot is not deleted, and all saved snapshots remain available.

For example:

```text
Empty state
└── Snapshot A (default)
    └── Snapshot B (active)
        └── live unsaved changes
```

With `Current`, the live changes are discarded and Snapshot B remains active; Snapshots A and B remain saved. With `Default`, the live changes are discarded and Snapshot A becomes the active default state; Snapshot B also remains saved.

> [!WARNING]
> Automatic deletion permanently discards live files and registry changes above the selected target state. Saved snapshot history is retained unless you separately choose to delete all snapshots. Quick Recovery can provide an opportunity to recover eligible files before deletion, but it is not universal protection against data loss.

## Default and invalid values

There is no single fixed fallback when this setting is absent or invalid. Normal synchronous automatic cleanup returns to the active state, while asynchronous or silent cleanup returns to the default state. Invalid values, including `y` and `n`, use the same context-dependent legacy behavior. Configure `Current` or `Default` explicitly when predictable behavior is required.

## Automatic and manual deletion

This setting affects SandMan's automatic deletion path only. Automatic cleanup is still triggered when the last sandboxed process terminates, as controlled by [Auto Delete](AutoDelete.md).

Manual **Delete Contents** operations use their own snapshot behavior and do not use this setting to choose between the current and default states. An explicit request to delete all snapshots also bypasses this setting and can remove the saved snapshot history.

*AutoDeleteSnapshotTarget* does not control creating or switching snapshots, choosing the default snapshot, deleting individual snapshots, or merging snapshots. See [Box Snapshots](../PlusContent/BoxSnapshots.md) for snapshot management.

## Recovery behavior

Before automatic deletion, Sandboxie's normal recovery handling may offer an opportunity to recover eligible files. This setting does not change recovery folders, file eligibility, [Auto Recover](AutoRecover.md), or [Quick Recovery](QuickRecovery.md) filtering; it only selects the retained state used after deletion.

## Sandbox Options

In Sandboxie Plus, open **Sandbox Options > File Options > Box Delete options**. Enable **Auto delete content changes when last sandboxed process terminates**, then choose a target under **After automatic deletion, restore from snapshot:**

- **Active snapshot** writes `AutoDeleteSnapshotTarget=Current`.
- **Default snapshot** writes `AutoDeleteSnapshotTarget=Default`.

The target control is enabled when automatic deletion is enabled and does not require an existing snapshot. Here, **Active snapshot** may represent the empty active state.

## Applying changes

SandMan reads this setting when automatic deletion begins. A saved change therefore applies to the next eligible automatic deletion; restarting SandMan, restarting sandboxed applications, or recreating snapshots is not required.

## Sandboxie Plus and Classic

This snapshot-target option belongs to the SandMan/Sandboxie Plus snapshot workflow. Sandboxie Classic uses a different deletion path and does not provide this Sandbox Options behavior.

## Failure behavior

Automatic deletion may report an error if the selected target no longer exists, restoring its data fails, or content cannot be deleted. The operation does not promise transactional rollback, and not every failure during automatic or silent cleanup is guaranteed to produce an interactive dialog.

## Version history

Sandboxie Plus 1.18.2 introduced the explicit `Current` and `Default` choices to make the target selection consistent across automatic-cleanup implementations.

## Related configuration

- [Auto Delete](AutoDelete.md)
- [Box Snapshots](../PlusContent/BoxSnapshots.md)
- [Quick Recovery](QuickRecovery.md)
- [Auto Recover](AutoRecover.md)
- [Sandboxie Ini](SandboxieIni.md)
