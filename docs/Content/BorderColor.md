# Border Color

_BorderColor_ is a per-sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls the colored border and optional sandbox-name label that SandMan displays around applicable sandboxed windows. The border is a visual indicator only; it does not resize or reposition the application window or change the sandbox's isolation.

## Syntax

The current format is:

```ini
BorderColor=#hex_color_code,border_mode,border_width,border_color_alpha,label_mode[,label_font_size]
```

For example:

```ini
[DefaultBox]
BorderColor=#00FFFF,ttl,6,192,in,6
```

The color is specified as a six-digit hexadecimal value in #BBGGRR order: blue, green, then red.

* The hash mark prefixes a six-digit hexadecimal number.
* The first two digits specify the red component.
* The next two digits specify the green component.
* The last two digits specify the blue component.

The remaining fields have these meanings:

| Field | Values and behavior |
| --- | --- |
| `border_mode` | Selects when and where the border is shown. See [Border modes](#border-modes). |
| `border_width` | Border width in pixels. The current default is `6`. |
| `border_color_alpha` | Border opacity from `0` to `255`. The current default and invalid-value fallback is `192`. |
| `label_mode` | `no` hides the label, `out` places it above the border, and `in` places it within the border. |
| `label_font_size` | Optional reference size for the label. When omitted or invalid, it uses the border width. |

## Border modes

SandMan currently presents the main modes as follows:

| INI mode | SandMan label | Behavior |
| --- | --- | --- |
| `off` | **Border disabled** | Does not display the border. |
| `ttl` | **Show only when title is in focus** | Displays the border according to the title-focus behavior. |
| `on` | **Always show (focused window only)** | Displays the border for the focused applicable window. |
| `all` | **Show for all windows in this box** | Displays borders for all applicable windows in the sandbox. |

The `ttloutside`, `onoutside`, and `alloutside` variants use the corresponding mode but draw the border outside the application frame. SandMan identifies these entries with **(outside)** in the selector.

The runtime also accepts `ttllbl`, `onlbl`, and `alllbl`. These label-only forms show the sandbox name or alias without the colored border frame. Label-only mode uses non-outside placement; an `outside` suffix is not retained for that mode.

## Label placement

The `label_mode` field maps to these SandMan choices:

| INI value | SandMan label |
| --- | --- |
| `no` | **Don't show in border** |
| `out` | **Show above the border** |
| `in` | **Show within the border** |

The displayed text can be affected by the sandbox alias and global alias-display settings described in [Box Alias](BoxAlias.md).

## BorderInsideMaximized

_BorderInsideMaximized_ controls how an outside border or outside-positioned label is placed for maximized or arranged (snapped) windows. It is enabled by default.

When enabled, SandMan draws the overlay inside such a window when its outside placement would otherwise extend beyond the application frame. This changes only the border overlay placement; it does not alter the application window's size or position.

To disable the automatic inside placement:

```ini
[DefaultBox]
BorderInsideMaximized=n
```

The setting metadata lists _BorderInsideMaximized_ as added in version 1.18.1, while the feature is described in the Sandboxie Plus 1.18.2 / Classic 5.73.2 release notes.

## SandMan interface

The current controls are available under:

**Sandbox Options > General Options > Box Options > Appearance**

This area provides the border mode, color, width, opacity, label placement, label-only option, and label-size controls. For outside modes, **Inside when maximized or snapped** enables _BorderInsideMaximized_. Its tooltip explains that an outside border which would be clipped by the monitor edge is drawn inside maximized or snapped windows instead.

The current Sandboxie Plus border is a SandMan overlay. Appearance changes generally do not require restarting sandboxed applications, although SandMan must be running to display its overlay.

## Sandboxie Control Classic

Sandboxie Control Classic provides its established border controls under [Sandbox Settings > Appearance](AppearanceSettings.md). The available Classic controls may differ from the current SandMan modes and options; in particular, do not assume that every newer SandMan mode is exposed by the historical Classic interface.
