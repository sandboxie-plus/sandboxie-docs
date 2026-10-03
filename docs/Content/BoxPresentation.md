# Box Presentation and Actions

`BoxIcon`, `CustomColor`, `DblClickAction`, and `PinToTray` are per-box SandMan presentation and interaction settings. They share a configuration surface but have different purposes: icon presentation, color preservation during preset changes, double-click actions, and tray-list filtering. They are not sandbox-isolation controls, and a box's color or icon is not proof of its security preset.

The current SandMan consumers read these values directly from the sandbox section. They do not request `GlobalSettings` fallback, enabled-template inheritance, or expanded effective-policy lookup, and do not support process/image or ProcessGroup selectors for these settings. A value present only in a template or `GlobalSettings` is not used here. A workflow that copies a value into the sandbox section creates a direct value that these consumers can use; this limitation does not apply to Sandboxie's configuration system generally.

The current Sandboxie Control Classic code has no dedicated consumers or equivalent controls for these four setting names. Their presence in an INI file does not provide the same Classic UI behavior.

## Custom box icons

`BoxIcon` can specify a Windows icon resource as `path,index`:

```ini
[ExampleBox]
BoxIcon=C:\Windows\System32\shell32.dll,0
```

Alternatively, configure an absolute image path manually:

```ini
[ExampleBox]
BoxIcon=C:\Icons\box.png
```

Direct images use Qt image handling; supported formats depend on the image support available in the build. `BoxIcon` is used in SandMan's main sandbox list/tree, Run Sandboxed box picker, Sandbox Options preview, and system-tray box list/menu, subject to the relevant icon-display preferences.

Custom icons, color-generated icons, box-type icons, and status overlays are separate presentation layers. If a custom icon cannot be loaded, fallback behavior differs by surface. The tray can try the target icon of a non-built-in `DblClickAction` before using the normal color/type icon; the main sandbox tree does not use that same fallback. An icon choice does not change the box type, security preset, or runtime enforcement.

Under **Sandbox Options > General Options > Box Options > Appearance**, open the color button's menu and select **Custom icon**. The icon picker stores a Windows resource selection as `path,index`; it is not a dedicated image-path editor. The color reset control resets the color, not `BoxIcon`.

## Keeping a custom color

```ini
[ExampleBox]
CustomColor=y
```

`CustomColor` does not define a color. The actual color remains in [`BorderColor`](BorderColor.md). `CustomColor=y` tells SandMan to preserve that color when changing **Box Type Preset**. Without the flag, changing the preset can apply the newly selected preset's color. A custom `BorderColor` can still be used without this flag; the flag concerns preservation during preset changes.

This setting does not enable the border, contain RGB values, or control border width or opacity. It also does not preserve the old security/isolation preset: changing **Box Type Preset** still changes the applicable preset controls even when the color is retained.

There is no checkbox labelled `CustomColor`. The color controls under **Sandbox Options > General Options > Box Options > Appearance** manage its state. Selecting or adjusting a custom color records `CustomColor=y` when applied; resetting to the preset color removes the flag when applied. With no direct value, the consumer's fallback is disabled.

## Double-click actions

`DblClickAction` selects the action for an applicable double-click on a sandbox:

```ini
[ExampleBox]
DblClickAction=!browse
```

Under **Sandbox Options > General Options > Box Options > Double click action:**, the editable selector provides:

| Value | SandMan label | Action |
| --- | --- | --- |
| `!options` | **Open Box Options** | Opens Sandbox Options. |
| `!browse` | **Browse Content** | Opens SandMan's sandbox-content browser. |
| `!recovery` | **Start File Recovery** | Opens the file-recovery window and scans; it does not enable Immediate Recovery. |
| `!run` | **Show Run Dialog** | Opens the Run Sandboxed dialog through `Start.exe`. |

An absent or empty value opens Sandbox Options. Selecting **Open Box Options** normally removes `DblClickAction` rather than storing `!options`. An unknown value beginning with `!` also opens Sandbox Options. **Ctrl + double-click** opens Sandbox Options regardless of the configured action.

A non-empty value that does not begin with `!` is command text forwarded to `Start.exe` for that sandbox, for example:

```ini
[ExampleBox]
DblClickAction="C:\Tools\example.exe" --example
```

This is not a [`RunCommand`](RunCommand.md) name, Run Menu caption, or program alias. The dispatcher does not resolve it against Run Menu entries, and the current selector does not automatically list those entries. It is not an unrestricted shell-language parser; do not assume pipelines or redirection are interpreted.

Invalid custom command text still causes a launch attempt, not an automatic fallback to Sandbox Options. Downstream launch errors can occur, and the configured value is not automatically deleted on failure. Changing the action in the interface can also update the custom-icon selection; review it before applying changes.

## Pinning boxes to the tray

```ini
[ExampleBox]
PinToTray=y
```

`PinToTray` marks the box as pinned for SandMan's tray-list filters. With no direct value, its consumer and checkbox fall back to unpinned. It does not create a separate notification-area icon for the sandbox.

The checkbox is under **Sandbox Options > General Options > Box Options**, labelled **Always show this sandbox in the systray list (Pinned)**. Checking it writes a direct `PinToTray=y`; unchecking it normally removes the direct scalar value. It does not display an inherited template/global value.

The SandMan preference `Options/SysTrayFilter` is configured under **Global Settings > Shell Integration > System Tray > Show boxes in tray list:**. It is a manager preference, not a `GlobalSettings` value inherited by these box consumers. Its absent-value fallback is **All Boxes**.

| Tray mode | Inactive, not pinned | Active, not pinned | Pinned |
| --- | --- | --- | --- |
| All Boxes | shown | shown | shown |
| Active + Pinned | hidden | shown | shown |
| Pinned Only | hidden | hidden | shown |

This assumes the box is otherwise enabled and available. Pinning does not force a disabled or unavailable box into the tray list; the checkbox's "Always" wording does not bypass those conditions.

## Applying changes

Apply changes in SandMan, or reload the configuration after editing it externally. These settings do not require restarting sandboxed applications.

- Changed `BoxIcon` values can appear when SandMan reloads/rebuilds the relevant presentation surface. Loaded icons are cached: replacing an external icon file without changing its configured path/string can leave the old icon visible. Restarting SandMan forces its icon caches to be rebuilt.
- Reopen Sandbox Options after external changes to `CustomColor` or the other settings so its controls reflect the new direct values. Color preservation applies when changing the preset in that interface.
- `DblClickAction` is read for each applicable sandbox double-click; the next gesture after applying/reloading the configuration can use the new action. Icon caching is separate from action dispatch.
- `PinToTray` is evaluated when the tray list/menu is rebuilt. Reopen it after applying/reloading changes; no SandMan restart is normally needed for pinning.

## Related pages

- [Border Color](BorderColor.md)
- [Box Alias](BoxAlias.md)
- [RunCommand](RunCommand.md)
- [File Recovery Architecture](RecoveryArchitecture.md)
- [Box Preset Comparison](../PlusContent/box-preset-comparison.md)
