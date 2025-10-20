# DisableForceRules

`DisableForceRules` is a per-box setting (introduced in v1.9.1 / 5.64.1) that disables all "force" rules for that box. When set, the driver will skip processing `ForceFolder`, `ForceProcess` and `ForceChildren` entries defined in the box, effectively preventing automatic sandbox-forcing based on those rules.

This setting is primarily useful when you want a box to exist but not participate in automatic forcing decisions (for example, when using the box only for manual runs or special-case operations).

## Syntax

Set this under a box section in the Sandboxie configuration:

```ini
[DefaultBox]

DisableForceRules=<y|n>
```

Valid values:

- `y` — enabled: the box's force rules are ignored.
- `n` — disabled (default): the box's force rules are evaluated when building force lists.

## Behavior

- When the driver enumerates configuration sections to build the in-memory force rules it calls `Conf_IsBoxEnabled` and then checks `DisableForceRules`. If `DisableForceRules` is set for a box, that box is skipped for force-rule processing and none of its `ForceFolder`, `ForceProcess` or `ForceChildren` entries will be used.[^1]

- Other settings that affect whether a box is considered at all include box enablement for the current SID/session — a box not enabled for the current user/session is not considered during force list creation.[^2]

- `DisableForceRules` does not remove the box or alter other non-force behavior; it only prevents the driver from adding that box's force entries to the runtime force lists.

## Examples

Disable force rules for a box named `NoAutoForce`:

```ini
[NoAutoForce]

DisableForceRules=y
```

Leave force rules enabled (default):

```ini
[MyBox]

DisableForceRules=n
```

## GUI (Sandboxie Manager / SandMan)

Toggle `Disable Force Rules` from the Sandboxie Manager (SandMan) UI in either place:

- Context menu -> Sandbox Presets -> Disable Force Rules
	- Right-click a sandbox in the box list, open the "Sandbox Presets" submenu and toggle the "Disable Force Rules" item.
- Box options -> Force tab
	- Right-click a sandbox, choose "Sandbox Options", switch to the "Force Programs" under "Program Control" tab and check/uncheck the "Disable forced Process and Folder for this sandbox" checkbox, then save.

These UI controls map directly to the `DisableForceRules` box setting and update it immediately for the selected box.[^4][^5]

## Implementation notes (driver behavior)

- The driver calls `Process_CreateForceData` to build an in-memory list of `FORCE_BOX` entries for each enabled box. During creation it iterates config sections and skips any box where `Conf_Get_Boolean(section, L"DisableForceRules", 0, FALSE)` returns true.[^1]

- Skipping a box in `Process_CreateForceData` means none of its `ForceFolder`, `ForceProcess` or `ForceChildren` lists are added to the runtime `boxes` list used by `Process_GetForcedStartBox` and related checks.

## See also

- [ForceProcess](ForceProcess.md) — force processes by name or path.
- [ForceFolder](ForceFolder.md) — force processes by folder path or pattern.
- [ForceChildren](ForceChildren.md) — parent-based forcing rules (children of matching parents are forced).

## Footnotes

[^1]: See how `Process_CreateForceData` loops all config sections and `if (Conf_Get_Boolean(section, L"DisableForceRules", 0, FALSE)) continue;` to skip boxes with the setting enabled.

[^2]: Conf_IsBoxEnabled is used to decide whether a box is active for the current SID/session before any force lists are built for it.

[^3]: The driver checks global/session-level flags such as `AllowForceSystem` and session-based force-disabled flags when deciding whether processes can be forced; `DisableForceRules` only affects per-box inclusion in force lists.

[^4]: The presets menu toggle is implemented in SandMan's `SbieView.cpp` (`m_pMenuPresetsForce`) and calls `SetBoolSafe("DisableForceRules", ...)` to change the setting.

[^5]: The box options dialog reads/writes the checkbox `ui.chkDisableForced` in `OptionsForce.cpp` and persists the `DisableForceRules` setting when the options are saved.
