# File Recovery Architecture

File recovery moves selected content from a sandbox to a host-accessible destination. Configuring a recoverable location does not grant a sandboxed program access to that host location; the recovery action is performed outside the sandbox after a user chooses what to recover.

## Recovery is split across components

| Component | Role |
| --- | --- |
| Automatic detection | With `AutoRecover=y`, SbieDll watches eligible file activity in a sandboxed process and reports recovery candidates. |
| Quick Recovery | SandMan separately scans configured locations when the recovery window is opened. It does not require `AutoRecover=y`. |
| Presentation | SandMan shows a recovery dialog or notification according to its preferences. |
| Destination | The user chooses the corresponding host folder or another folder. |
| Recovery operation | SandMan moves selected files from sandbox storage to the host destination. |

## Recoverable locations

Repeatable [`RecoverFolder`](RecoverFolder.md) entries identify locations or patterns for both automatic detection and Quick Recovery. A literal folder supplies a recursive Quick Recovery scan root. A wildcard entry instead filters candidate paths; it is not an instruction to recursively scan every path represented by the pattern. Effective entries may come from box configuration and enabled templates. Shell-folder references such as `%Personal%` can be expanded to usable paths.

## Automatic and Immediate Recovery

[`AutoRecover=y`](AutoRecover.md) initializes process-side detection using the effective `RecoverFolder` and [`AutoRecoverIgnore`](AutoRecoverIgnore.md) entries. A candidate must match a recoverable location and not match an ignore entry. Sandboxie reports an eligible, non-empty sandboxed file after the relevant file activity; this is not a promise of a prompt at the exact instant of creation. Detection does not itself move the file.

SandMan receives the recovery event and can open a dialog or present a notification. Its notification preference and temporary suppression can affect what the user sees. Automatic detection applies `AutoRecoverIgnore` regardless of the Quick Recovery ignore option.

The SbieDll fallback for an absent `AutoRecover` setting is disabled. Newly created boxes may explicitly enable it: the current SandMan new-box wizard offers Immediate Recovery checked by default, while Classic's new-box defaults write `AutoRecover=y`. Thus a product-created box and a box with no effective `AutoRecover` value need not behave alike.

## Quick Recovery

Opening [Quick Recovery](QuickRecovery.md) makes SandMan read the effective recovery locations and scan literal roots recursively. Wildcard entries filter candidates found through the scan. The window can also show all boxed files rather than only the configured recovery locations.

SandMan can apply `AutoRecoverIgnore` to the Quick Recovery list when [`UseAutoRecoverIgnoreForQuick`](UseAutoRecoverIgnoreForQuick.md) is enabled. The window's **Show All Files** or **Show Ignored** view can expose otherwise hidden files. This Quick-specific filtering does not replace the automatic detector's own ignore check.

The settings metadata describes `UseAutoRecoverIgnoreForQuick` with an `n` default, but the current SandMan consumer treats an absent value as enabled. An explicit `n` turns off its normal Quick-list filtering. This is a SandMan consumer default, not an SbieDll-wide runtime default.

## Destinations and moving files

**Recover to Same Folder** selects the corresponding location outside the sandbox; **Recover to Any Folder** lets the user choose another destination. SandMan keeps reusable destination history in a user setting (`SbieCtrl_RecoverTarget`) and its own last-target preference. These are not `RecoverFolder` box rules.

SandMan prepares the destination and uses a host-side move (`QFile::rename`) for the selected sandbox file. If a target already exists, it asks before overwriting; approving overwrite can remove the existing target before the move. A failed move is reported and the unrecovered sandbox source remains. Recovery is not guaranteed to be atomic or to roll back a previously approved overwrite.

SandMan may run an installed FileChecker add-on or configured [`OnFileRecovery`](SandManTriggers.md) commands before moving a file. A checker failure can stop that recovery unless the user explicitly overrides the warning. Checkers and user approval do not prove that recovered content is safe to open or run.

## Applying changes

Automatic detection and its folder/ignore lists initialize in each sandboxed process. Restart affected sandboxed processes after changing `AutoRecover`, `RecoverFolder`, or `AutoRecoverIgnore` when you need the automatic detector to use the new values. SandMan reads recovery locations when the recovery window is created, while Quick-list ignore settings are reloaded during scans and refreshes. Reopen the recovery window after changing `RecoverFolder` outside that window. These SandMan-side changes do not require restarting sandboxed processes for Quick Recovery.

## Classic and SandMan

The older [Recovery Settings](RecoverySettings.md), [Quick Recovery](QuickRecovery.md), and [Immediate Recovery](ImmediateRecovery.md) pages retain useful Sandboxie Control / Classic workflows and screenshots. Current Sandboxie Plus controls are under **Sandbox Options > File Recovery**, with separate **Quick Recovery** and **Immediate Recovery** sections. SandMan's presentation preferences are in **Global Settings > General Config**: **Recovery Options** contains recovery-window preferences, and **Notifications** contains **Show recoverable files as notifications**.

## Version history

Wildcard recovery patterns and `UseAutoRecoverIgnoreForQuick` were added in Sandboxie Plus 1.18.0 / Classic 5.73.0. This does not date the introduction of the older recovery settings.

## Related pages

- [Recover Folder](RecoverFolder.md)
- [Auto Recover](AutoRecover.md)
- [Auto Recover Ignore](AutoRecoverIgnore.md)
- [Use Auto Recover Ignore For Quick](UseAutoRecoverIgnoreForQuick.md)
- [Quick Recovery](QuickRecovery.md)
- [Immediate Recovery](ImmediateRecovery.md)
