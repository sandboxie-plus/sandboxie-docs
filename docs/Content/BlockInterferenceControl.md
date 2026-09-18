# BlockInterferenceControl

_BlockInterferenceControl_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.13.6. It is disabled by default and is currently marked as Experimental.

For example:

```ini
[DefaultBox]
BlockInterferenceControl=y
```

When enabled, this setting restricts selected cursor, foreground, activation, and topmost-window operations performed by sandboxed processes. It does not block every possible user-interface or input interaction and should not be treated as complete desktop isolation.

## Affected behavior

The setting restricts selected behavior associated with these Windows APIs:

- `SetCursorPos`
- `ClipCursor`
- `ShowCursor`
- `SetForegroundWindow`
- `SetActiveWindow`
- `BringWindowToTop`
- `SwitchToThisWindow`
- selected operations performed through `CreateWindowEx`, `MoveWindow`, and `SetWindowPos`

These APIs are not all handled in the same way. Some calls are blocked, while selected window-creation, positioning, and topmost requests are modified before being passed to Windows.

## Cursor behavior

_BlockInterferenceControl_ blocks direct cursor repositioning through `SetCursorPos`.

Creating or changing cursor confinement with `ClipCursor(rect)` is also blocked. `ClipCursor(NULL)` remains allowed so that an existing confinement can be released.

Requests to hide the cursor through `ShowCursor(FALSE)` are suppressed, while requests to show the cursor remain allowed.

This setting does not specifically block `SendInput`, raw input, mouse capture, cursor-shape changes, or every simulated-input mechanism. Some of those paths may be subject to separate Sandboxie protections.

## Foreground and window activation

The setting suppresses explicit calls through `SetForegroundWindow`, `SetActiveWindow`, `BringWindowToTop`, and `SwitchToThisWindow`.

These restrictions are not limited to unsandboxed target windows. The current behavior also applies when the target belongs to the same sandbox. `SetFocus` is not part of this setting.

## Topmost windows and z-order

For intercepted window-creation paths, Sandboxie removes the `WS_EX_TOPMOST` style. When taskbar covering is not allowed, selected `HWND_TOPMOST` requests through `SetWindowPos` are also reduced.

The setting limits selected topmost requests but does not block every ordinary z-order change. Window positioning and sizing requests may also be adjusted to keep sandboxed windows from covering the taskbar.

## Allowing taskbar coverage

The related setting:

```ini
AllowCoverTaskbar=y
```

relaxes some of the position and size restrictions that _BlockInterferenceControl_ applies around `MoveWindow`, `SetWindowPos`, and selected window-creation positioning.

_AllowCoverTaskbar_ does not disable all interference-control behavior. In particular, it does not restore the blocked foreground and activation APIs or every topmost request.

## Compatibility

Some blocked operations report failure to the application instead of being silently allowed. Programs that depend on the restricted behavior may therefore work differently inside the sandbox.

The Sandboxie project warns that this option may cause compatibility issues with games and does not recommend it for gaming boxes. Games may depend on cursor confinement, direct cursor movement, foreground activation, or fullscreen and topmost-window behavior. This warning does not mean that every game is incompatible.

## Runtime and scope

The setting is read when a sandboxed process initializes. Existing processes generally need to be restarted after changing the configuration; newly started sandboxed processes receive the new value.

It applies at sandbox and process level and has no documented per-program syntax. The restrictions are implemented primarily through user-mode API interception inside sandboxed processes rather than as kernel-enforced protection. Alternative APIs not covered by this setting should not be assumed to be blocked.

## Sandboxie Plus interface

The option is available under:

**Sandbox Options > General Options > Restrictions > Prevent interference with the user interface (Experimental)**

It is unchecked by default. Its tooltip warns that preventing mouse movement, bringing windows to the front, and similar operations is likely to cause issues with games.

When the option is enabled, the **Allow sandboxed windows to cover the taskbar** control becomes available.

## Version history

_BlockInterferenceControl_ was introduced in Sandboxie Plus 1.13.6. _AllowCoverTaskbar_ was added later as a compatibility option. The default for _BlockInterferenceControl_ has remained disabled.

## Related settings

- [Sandboxie Ini](SandboxieIni.md)
- [Block Screen Capture](BlockScreenCapture.md), which uses a separate screen-capture protection mechanism
- [BlockInterferePower](BlockInterferePower.md)
