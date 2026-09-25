# Sandbox Deletion and Removal Lifecycle

Deleting sandbox contents and removing a sandbox definition are different operations. SandMan performs both outside sandboxed applications; neither operation is controlled by the Delete V1/V2 file- or registry-virtualization settings.

| Operation | Result |
| --- | --- |
| **Delete Contents** (clean the box) | Discards or resets stored sandbox changes while retaining the sandbox definition. With retained snapshots, the resulting state may be a saved snapshot rather than an empty directory. |
| **Remove Sandbox** | Removes the sandbox definition. Ordinary manual removal first handles its stored contents; removal can fail if the storage is not empty. |

## Automatic content cleanup

[`AutoDelete=y`](AutoDelete.md) asks SandMan to clean the contents when it observes a previously active box reach zero running processes. The setting is off when absent. It does **not** itself remove the sandbox definition. On the normal box-close path, SandMan runs [`OnBoxTerminate`](SandManTriggers.md#onboxterminate) first, then checks `NeverDelete` and `AutoDelete`. If cleanup is eligible, [recovery](QuickRecovery.md) may offer recoverable files before deletion; cancelling that workflow stops this cleanup, while no visible recoverable files can allow it to continue silently. Recovery is not a guarantee that every valuable file will be found.

If cleanup proceeds, SandMan runs [`OnBoxDelete`](SandManTriggers.md#onboxdelete) before the normal content-cleanup operation. The trigger is host-side automation, not the command that performs deletion. SandMan can run cleanup through a waiting non-queued path or through a queued job. A startup cleanup option can also invoke box-closed handling for an already empty box.

## Snapshots and cleanup results

Automatic cleanup can discard only live changes and return the box to a retained active or default snapshot state. [`AutoDeleteSnapshotTarget`](AutoDeleteSnapshotTarget.md) selects that target for automatic cleanup; it does not turn on `AutoDelete`. Manual **Delete Contents** has its own snapshot choices, including whether to delete all snapshots. See [Box Snapshots](../PlusContent/BoxSnapshots.md).

Cleanup can fail after some content has changed; it is not a transaction with guaranteed rollback. The underlying folder deletion waits for access and retries failures, but can still return an error. A snapshot restore can fail separately.

## Automatic definition removal

`AutoRemove=y` is a separate box setting. SandMan consults it when content-cleanup completion is handled and then attempts to remove the definition. It does not start cleanup on box close by itself: with `AutoDelete=n`, closing the last process alone does not remove the box. A later manual SandMan cleanup can nevertheless reach the same removal transition.

The New Box Wizard's **Remove after use** option writes **both** `AutoDelete=y` and `AutoRemove=y`. With ordinary cleanup that leaves storage empty, this pairs content cleanup with definition removal. Snapshot-retaining cleanup may leave storage present, in which case the underlying removal operation refuses to remove the definition.

Do not treat cleanup and removal as an all-or-nothing transaction. A failed queued cleanup job does not reach the `BoxCleaned` completion transition; the non-queued waiting path can attempt the `AutoRemove` transition even when its cleanup progress reports an error. The underlying ordinary removal still rejects a box whose storage is not empty. Check the actual result before assuming the definition or data is gone.

## Protection settings

`NeverDelete=y` blocks automatic content cleanup and is checked by the ordinary full-cleanup and queued cleanup paths. `NeverRemove=y` guards the normal manual SandMan **Remove Sandbox** action. They protect different operations and are not filesystem access controls.

In **Sandbox Options > File Options > Box Delete options**, the tri-state **Protect this sandbox from deletion or emptying** checkbox maps as follows:

| Checkbox | Saved settings | Meaning |
| --- | --- | --- |
| Checked | `NeverDelete=y`, `NeverRemove=y` | Protect contents and the definition through their respective normal paths. |
| Partially checked | `NeverRemove=y`; `NeverDelete` off | Protect the definition through manual removal, but allow ordinary content cleanup. |
| Unchecked | Both off | Neither protection is selected. |

These protections have path-specific limits. For an ordinary box, `NeverDelete` can prevent the cleanup needed for manual removal. In the non-queued manual cleanup path, an `OnBoxDelete` command can run before the ordinary full-cleanup guard rejects a protected box. That path can also select a retained snapshot without passing through that `NeverDelete` guard; removal of an unmounted image-backed box has another special path. Do not use `NeverDelete` as a universal data-preservation guarantee. Conversely, the current `AutoRemove` transition after cleanup does **not** consult `NeverRemove`, even though normal manual removal does. A hand-written combination of `AutoRemove=y` and `NeverRemove=y` therefore has different results on the automatic and manual routes.

## Manual actions

For **Delete Contents**, SandMan asks for confirmation or offers a recovery window according to its preferences, terminates running sandboxed processes, and starts normal or snapshot-aware content cleanup. `OnBoxDelete` runs before that cleanup where applicable. The definition normally remains, but `AutoRemove=y` can initiate a subsequent removal attempt after cleanup.

For **Remove Sandbox**, SandMan asks for confirmation, handles mounted image storage, checks `NeverRemove` for an ordinary box, and requests cleanup in removal mode before removing the definition. This direct removal mode does not run `OnBoxDelete`. Ordinary removal requires empty storage; a failed cleanup or remaining image can prevent definition removal. Internal temporary/shadow objects have a separate path and are not a normal user-facing configuration option.

## Configuration and applying changes

These are box lifecycle settings, not image- or program-qualified resource rules. The current SandMan Boolean consumers for `AutoDelete`, `AutoRemove`, `NeverDelete`, and `NeverRemove` read box values directly and use `n` when absent; their calls do not request `GlobalSettings` or template fallback. `AutoDeleteSnapshotTarget` is read from effective configuration, including applicable global/template values, when automatic cleanup begins. The lifecycle switches are evaluated at their corresponding box-close, cleanup, or manual-removal event, so changing them does not normally require restarting sandboxed processes, the service, or Windows.

## Sandboxie Plus and Classic

This page describes current SandMan behavior. The older [Delete Settings](DeleteSettings.md) page preserves the Sandboxie Control / Classic interface. Classic's [`DeleteCommand`](DeleteCommand.md) selects its legacy deletion command and remains distinct from SandMan's pre-cleanup `OnBoxDelete` trigger.

## Version history

The older `AutoDelete` and `NeverDelete` settings have no established introduction version in current setting metadata. `AutoRemove` was added in Sandboxie Plus 1.7.1; `NeverRemove` in 1.10.1; and `AutoDeleteSnapshotTarget` in 1.18.2. These versions do not imply that the full lifecycle or Classic interface began in those releases.

## Related pages

- [Auto Delete](AutoDelete.md)
- [Never Delete](NeverDelete.md)
- [AutoDeleteSnapshotTarget](AutoDeleteSnapshotTarget.md)
- [Delete Settings](DeleteSettings.md)
- [Delete Sandbox](DeleteSandbox.md)
- [Quick Recovery](QuickRecovery.md)
- [SandMan Triggers](SandManTriggers.md)
- [Box Snapshots](../PlusContent/BoxSnapshots.md)
