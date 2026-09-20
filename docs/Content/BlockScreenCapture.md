# Block Screen Capture

_BlockScreenCapture_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) that limits selected capture attempts made by a sandboxed process against the desktop or windows outside the same sandbox. It covers selected common USER32 and GDI capture paths; it is not a complete screen-capture prevention mechanism.

```ini
[DefaultBox]
BlockScreenCapture=y
```

The default is `n`.

## What it intercepts

With normal GUI isolation active, Sandboxie intercepts these USER32 functions when _BlockScreenCapture_ is enabled:

- `GetDC`
- `GetWindowDC`
- `GetDCEx`
- `PrintWindow`
- `ReleaseDC`

For `GetDC`, `GetWindowDC`, and `GetDCEx`, a request targeting a null window handle, the desktop window, or a window outside the same sandbox receives a compatible memory DC backed by a dummy bitmap instead of the real display or window DC. `ReleaseDC` recognizes and releases these substitute DCs.

For the same outside targets, `PrintWindow` fails, returns zero, and sets the Windows error to access denied. Calls targeting a window in the same sandbox remain eligible for the normal API operation.

Sandboxie also intercepts the ANSI and Unicode `CreateDC` paths when they request the `DISPLAY` driver without a specific device, substituting a dummy DC. The current implementation does not hook `BitBlt` or `StretchBlt` themselves.

## Scope and limitations

This setting is experimental and may cause UI glitches. As the SandMan tooltip notes, it blocks only some common ways of obtaining a screen capture. It should not be treated as protection against every capture API, capture program, display driver, or recording technique.

When `OpenWinClass=*` is configured, SandMan disables the normal _BlockScreenCapture_ checkbox and Sandboxie does not install the principal USER32 interception path described above. The separate GDI display-DC interception can still be initialized if the setting is forced manually, but that partial behavior should not be treated as normal or complete capture protection.

## Configuration and runtime changes

_BlockScreenCapture_ is a box setting. Normal template and global fallback can contribute its effective value when the box does not provide an overriding value.

The value is cached when the sandboxed process initializes its GUI/GDI hooks. Restart affected sandboxed applications after changing it; restarting SandMan, the service, or the driver is not normally required.

## SandMan

Open **Sandbox Options > General Options > Restrictions** and use:

> Prevent sandboxed processes from capturing window images (Experimental, may cause UI glitches)

The tooltip states:

> This feature does not block all means of obtaining a screen capture, only some common ones.

## Related settings

- [Cover Boxed Windows](CoverBoxedWindows.md) asks Windows to exclude eligible sandboxed application windows from compatible capture paths.
- [Hide Borders From Capture](HideBordersFromCapture.md) applies to SandMan's separate border and label overlay.

These controls are independent and operate in different directions.

## Version history

The feature was introduced as `IsBlockCapture` in Sandboxie Plus 1.13.4 / Classic 5.68.4. It was renamed to `BlockScreenCapture` in 1.13.6 / 5.68.6, which also included Windows 7 and KeePass compatibility fixes.
