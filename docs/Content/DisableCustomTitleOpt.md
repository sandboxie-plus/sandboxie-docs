# Disable Custom Title Optimization

_DisableCustomTitleOpt_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). Despite its name, it does not disable an application's custom title bar. It disables Sandboxie's avoidance optimization for custom or client-drawn title bars.

Its practical effect is to let Sandboxie attempt to add the `[#]` or sandbox-name title marker to windows that would normally be skipped.

```ini
[DefaultBox]
DisableCustomTitleOpt=y
```

The setting may also be disabled or limited to a program:

```ini
DisableCustomTitleOpt=n
DisableCustomTitleOpt=program.exe,y
```

## Default behavior

When the setting is absent or set to `n`, Sandboxie uses a geometry-based heuristic to identify likely custom or client-drawn title bars and avoids modifying their titles. Applications built with frameworks such as Delphi VCL, Qt, or Electron are examples that may use such title bars; Sandboxie does not identify those frameworks by name for this decision.

With `DisableCustomTitleOpt=y`, Sandboxie skips that avoidance check and continues normal title-marker processing. A marker is not guaranteed because the window must still pass the other title eligibility checks.

## Compatibility considerations

The avoidance behavior was introduced because changing titles on some custom or client-drawn windows could trigger excessive Desktop Window Manager repaint activity and high CPU usage. Enabling _DisableCustomTitleOpt_ can reintroduce that problem in affected applications, but it does not imply that every VCL, Qt, Electron, or other custom-title application will be affected.

This setting controls only Sandboxie's title-marker and title-modification path. It does not control:

- colored sandbox borders or border overlays;
- window-class renaming;
- tray-icon decoration;
- the application's own custom title bar.

[`BoxNameTitle`](BoxNameTitle.md) and other independent title rules continue to apply.

## Applying changes

The setting is read when the process initializes its GUI title handling. Restart the affected application after changing it.

This setting has no dedicated control in SandMan or Sandboxie Control Classic. Configure it manually in `Sandboxie.ini` or through the INI editor.

## Version history

- Sandboxie Plus 1.17.6 / Classic 5.72.6 introduced the custom-title avoidance behavior to address excessive DWM repaint activity.
- Sandboxie Plus 1.17.8 / Classic 5.72.8 added _DisableCustomTitleOpt_ as an opt-out.

## Related configuration

- [Box Name Title](BoxNameTitle.md)
- [Sandboxie Ini](SandboxieIni.md)
