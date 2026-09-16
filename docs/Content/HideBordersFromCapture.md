# HideBordersFromCapture

_HideBordersFromCapture_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.17.3.

```ini
[DefaultBox]
HideBordersFromCapture=y
```

This setting applies to Sandboxie Plus's visual border overlay, not to the sandboxed application's content. Enabling it does not make the application's own window uncapturable.

## Capture behavior

Sandboxie Plus (SandMan) applies Windows display affinity to the separate window used for the colored border and sandbox name or alias label. When _HideBordersFromCapture_ is enabled, SandMan first requests `WDA_EXCLUDEFROMCAPTURE`. If Windows rejects that request, it falls back to `WDA_MONITOR`. When the setting is disabled, the overlay uses `WDA_NONE`.

`WDA_EXCLUDEFROMCAPTURE` asks compatible Windows capture paths to omit the overlay window and is supported starting with Windows 10 version 2004. On earlier Windows versions, Microsoft documents this value as behaving like `WDA_MONITOR`. The `WDA_MONITOR` fallback keeps the overlay visible on a monitor but may show it as blank elsewhere, while `WDA_NONE` applies no display-affinity restriction. Compatible OS-managed capture paths normally omit or blank the Sandboxie border overlay, but compatibility with every capture or recording tool is not guaranteed.

Because the colored frame and label share the same overlay, the display-affinity setting applies to both. The sandboxed application's content remains capturable unless another independent setting affects it.

Windows display affinity is not a DRM mechanism or security boundary. This option is intended to keep Sandboxie's visual border and label out of compatible screenshots or screen recordings; it does not provide screenshot protection for the sandboxed application.

For the Windows API semantics and limitations, see Microsoft's [`SetWindowDisplayAffinity` documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowdisplayaffinity).

## Default and configuration scope

The metadata default for _HideBordersFromCapture_ is disabled. An explicit per-box value takes precedence, followed by an explicit global value. If neither value exists, SandMan uses the box-local _CoverBoxedWindows_ value as the fallback. With neither setting enabled in the box, the effective behavior is off.

This fallback is specifically to the box-local _CoverBoxedWindows_ value; it does not use template or global inheritance of that setting. There is no documented per-program syntax for _HideBordersFromCapture_.

## Runtime behavior

Existing SandMan border overlays can have their display-affinity state updated dynamically, and the border subsystem refreshes existing overlays. Restarting the sandboxed application is normally unnecessary.

There is currently no dedicated checkbox for _HideBordersFromCapture_ in the normal Sandbox Options interface. Configure it through the INI configuration.

## Related settings

* [Sandboxie Ini](SandboxieIni.md)
* [Border Color](BorderColor.md) controls whether and how the visual border is displayed.
* [Cover Boxed Windows](CoverBoxedWindows.md) concerns capture and display-affinity behavior of sandboxed application windows, while _HideBordersFromCapture_ concerns SandMan's border and label overlay. The two settings do not have identical fallback or inheritance semantics.
* [Block Screen Capture](BlockScreenCapture.md) independently controls capture operations initiated by sandboxed processes. It does not control whether SandMan's overlay appears in compatible host-side capture paths.

## Version history

_HideBordersFromCapture_ was introduced in Sandboxie Plus 1.17.3 to separate border-overlay capture behavior from the broader _CoverBoxedWindows_ behavior. Its explicit metadata default remains disabled, subject to the runtime fallback described above.
