# Cover Boxed Windows

_CoverBoxedWindows_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) that asks Windows to exclude eligible sandboxed application windows from compatible capture paths. It does not make every sandboxed window universally uncapturable.

```ini
[DefaultBox]
CoverBoxedWindows=y
```

The default is `n`.

## How it works

Sandboxie intercepts the ANSI and Unicode `CreateWindowEx` paths in the sandboxed process. After a window is created successfully with a null parent/owner argument, Sandboxie calls the Windows `SetWindowDisplayAffinity` API with `WDA_EXCLUDEFROMCAPTURE` (`0x00000011`).

This applies to eligible parentless windows reached through those intercepted creation paths. Sandboxie does not recursively apply the affinity to child windows or to owned windows created with a non-null parent/owner argument. The current implementation does not check whether `SetWindowDisplayAffinity` succeeds and does not retry or apply a fallback if the call fails.

## Windows behavior and limitations

Microsoft documents that `SetWindowDisplayAffinity` requires a top-level window owned by the calling process and works only while the Desktop Window Manager is composing the desktop. It affects a specific set of public operating-system capture features rather than every capture technique.

`WDA_EXCLUDEFROMCAPTURE` provides its exclusion behavior starting with Windows 10 version 2004. On earlier supported Windows versions, Microsoft documents the value as behaving like `WDA_MONITOR`, which displays the window on a monitor but presents it without content elsewhere.

Windows display affinity is not a security feature or DRM guarantee. Capture results depend on Windows and the capture path being used. See Microsoft's [`SetWindowDisplayAffinity` documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowdisplayaffinity).

Project-specific limitations also apply:

- _CoverBoxedWindows_ does not currently work with Chromium-based browsers version 128 or later; [issue #4302](https://github.com/sandboxie-plus/Sandboxie/issues/4302) remains open.
- Console applications such as `cmd.exe` are not supported.
- Child, owned, or otherwise unhandled windows must not be assumed to receive display affinity.

## Configuration and runtime changes

_CoverBoxedWindows_ is a box setting. Normal template and global fallback can contribute its effective value when the box does not provide an overriding value.

The value is cached when the sandboxed process initializes its GUI hooks, and the affinity is requested when each eligible window is created. Changing the setting does not update an already running process or retrofit existing windows. Restart affected sandboxed applications after changing it; restarting SandMan, the service, or the driver is not normally required.

## SandMan

Open **Sandbox Options > Security Options > Box Protection** and use:

> Prevent processes from capturing window images from sandboxed windows

The project metadata classifies this setting as experimental.

## Related settings

- [Block Screen Capture](BlockScreenCapture.md) limits selected capture attempts initiated by sandboxed processes against the desktop or windows outside their sandbox.
- [Hide Borders From Capture](HideBordersFromCapture.md) applies separately to SandMan's border and label overlay.

## Version history

The feature was introduced as `IsProtectScreen` in Sandboxie Plus 1.13.2 / Classic 5.68.2 and received fixes in 1.13.3 / 5.68.3. It was renamed to `CoverBoxedWindows` in 1.13.6 / 5.68.6.
