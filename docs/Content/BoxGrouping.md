# BoxGrouping

`BoxGrouping` is a user-settings value available since Sandboxie Plus 1.9.1. It stores the per-user hierarchy used by SandMan to organize sandboxes into visual groups.

Box groups are user-interface metadata only. They do not alter sandbox isolation or contents, and sandboxes in the same group do not share settings. Visual nesting does not create configuration inheritance or parent and child sandboxes.

## Storage and scope

`BoxGrouping` is stored in [Sandboxie Ini](SandboxieIni.md), normally in the active Windows user's section:

```ini
[UserSettings_12345678]
BoxGrouping=:Browsers,DefaultBox
BoxGrouping=Browsers:ChromeBox,Private
BoxGrouping=Private:FirefoxBox
```

It is not a per-sandbox setting, is not stored under `[GlobalSettings]`, and does not use template inheritance. Each Windows user normally has a separate `[UserSettings_xxxxxxxx]` section and may therefore have a different hierarchy. Portable configurations may instead use `[UserSettings_Portable]`.

## Syntax

The general form is:

```ini
BoxGrouping=<parent>:<member1>,<member2>,...
```

For example:

```ini
BoxGrouping=:Box1,Group1
BoxGrouping=Group1:Box2,SubGroup
BoxGrouping=SubGroup:Box3
BoxGrouping=EmptyGroup:
```

- The text before the colon is the parent group.
- An empty parent represents the root level.
- Entries after the colon are the parent's immediate children.
- A child is a subgroup when that name also has its own `BoxGrouping=<name>:` entry.
- Repeated lines for the same parent extend its member list.
- An entry ending with a colon defines an empty named group.

SandMan supports nested groups. This configuration:

```ini
BoxGrouping=:Browsers,DefaultBox
BoxGrouping=Browsers:ChromeBox,Private
BoxGrouping=Private:FirefoxBox
```

represents:

```text
Browsers
├── ChromeBox
└── Private
    └── FirefoxBox

DefaultBox
```

The nesting is purely organizational. `Private` does not pass settings or restrictions to `FirefoxBox`.

## Root level and hierarchy normalization

An empty parent key represents the root. For example:

```ini
BoxGrouping=:DefaultBox,Browsers
```

places both `DefaultBox` and `Browsers` at the top level. SandMan may show this destination as `[None]`; `[None]` is not a real named group.

SandMan normalizes the hierarchy into a tree-like structure, where each item is intended to have one parent. The UI prevents moving a group into itself or one of its descendants. Malformed duplicate or cyclic data created by manual editing may be normalized automatically; the exact conflict resolution should not be relied upon.

## Ordering

`BoxGrouping` stores the member order used by SandMan's manual ordering mode. Other active sort modes, such as alphabetical or column sorting, may display the same hierarchy in a different order.

This order is display metadata. It does not control sandbox or program execution order.

## Managing groups in SandMan

SandMan manages groups directly in its main sandbox tree. Relevant operations include:

- **Sandbox > Create Box Group**;
- creating a group from the tree or group context menu;
- **Move Sandbox** and **Move Group**;
- **Move Up** and **Move Down**;
- drag and drop.

Moving a sandbox changes only its visual location and stored order. It does not move sandbox files, recreate the sandbox, restart its processes, or change runtime policy.

### Removing, renaming, and adding items

Removing a group does not delete its sandboxes. **Remove Group** removes the organizational node and moves its immediate sandboxes and subgroups to the removed group's parent level. If a top-level group is removed, its contents become top-level items.

Renaming a sandbox through SandMan updates its group reference. Renaming a group preserves its contents and updates its parent relationship.

A new sandbox that is not otherwise assigned appears at the root. When creation or import occurs with a target group selected, SandMan can place the sandbox in that group. Duplicating a sandbox currently preserves the source sandbox's group membership.

## Tree expansion state

Expanded and collapsed tree state is not stored in `BoxGrouping`. SandMan stores it separately as user-interface configuration.

The current startup behavior can be selected under **Global Settings > Interface Config > User Interface > Group state on start**, with modes including:

- **Remember previous state**;
- **Expand all groups**;
- **Collapse all groups**.

In short, `BoxGrouping` stores membership, hierarchy, and manual sibling order; tree expansion state is separate.

## No runtime or isolation effect

`BoxGrouping` does not affect:

- file, registry, or process isolation;
- program-start restrictions;
- resource limits or access rules;
- sandbox contents;
- configuration inheritance;
- execution order.

Each sandbox remains independently configured regardless of the group in which it appears. Visual hierarchy does not imply policy hierarchy: box groups do not provide group-wide settings, group templates, shared restrictions, or additional isolation.

## Manual editing and reload behavior

SandMan normally manages `BoxGrouping` automatically. Manual editing is possible, but malformed graphs may be normalized. SandMan must observe or reload the configuration change before the revised hierarchy appears. Sandboxed applications do not need to restart because grouping is UI-only.

Colons and commas are structural separators in the persisted format. Avoid `:` in manually created group names, and do not use commas; SandMan's UI rejects group names containing commas. The UI also rejects parentheses and control characters in group names.

## Sandboxie Plus and Classic

SandMan uses `BoxGrouping`. Sandboxie Control Classic and the legacy `Start.exe` box selector continue to use `BoxDisplayOrder`.

`BoxDisplayOrder` is a legacy layout format and is marked as superseded by `BoxGrouping` for the current SandMan layout. SandMan can use the legacy hierarchy as a fallback when no `BoxGrouping` mapping is available, but Plus and Classic do not continuously synchronize the two formats. Classic still consumes `BoxDisplayOrder`, so it should not be considered entirely obsolete.

See the [Sandbox Menu](SandboxMenu.md) and [Sandboxie Plus Migration Guide](PlusMigrationGuide.md) for the corresponding user-interface workflows.

## Export and backup behavior

`BoxGrouping` is user-interface configuration and is not intrinsic metadata of an exported sandbox. A normal box-only export and import does not carry the user's grouping hierarchy with the sandbox. A full `Sandboxie.ini` backup that includes the relevant user-settings section can preserve it.

## Version history

The current `BoxGrouping` storage format was introduced in Sandboxie Plus 1.9.1 as part of a rework of box-grouping configuration storage. Grouping functionality itself predates this setting. Later versions added or fixed nested grouping, renaming, drag and drop, tray hierarchy, ordering, and expansion-state persistence.
