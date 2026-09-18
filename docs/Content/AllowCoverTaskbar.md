# AllowCoverTaskbar

_AllowCoverTaskbar_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.14.2. It is disabled by default.

```ini
[DefaultBox]
BlockInterferenceControl=y
AllowCoverTaskbar=y
```

This setting only has an effect when `BlockInterferenceControl=y`. When interference control is disabled, _AllowCoverTaskbar_ is effectively inert.

## Behavior

_AllowCoverTaskbar_ is a compatibility option for selected restrictions imposed by _BlockInterferenceControl_. It is not an independent taskbar-access feature and does not grant general permission to interact with the Windows taskbar.

With `BlockInterferenceControl=y` and `AllowCoverTaskbar=n`, Sandboxie may adjust selected window position, size, and z-order requests associated with taskbar coverage. Enabling _AllowCoverTaskbar_ skips those specific adjustments for relevant intercepted operations involving `CreateWindowExW`, `MoveWindow`, and `SetWindowPos`.

The setting does not disable the rest of _BlockInterferenceControl_. Restrictions on foreground activation, the `BringWindowToTop` API, direct cursor repositioning, cursor confinement, and cursor hiding remain active. It also does not restore the initial `WS_EX_TOPMOST` style removed from intercepted window creation by _BlockInterferenceControl_.

The current application-window restriction logic uses the Windows primary-display work area rather than a fully per-monitor taskbar model. Do not rely on it to model every secondary-monitor taskbar, window spanning multiple monitors, or unusual shell or appbar arrangement exactly.

## Runtime behavior

_AllowCoverTaskbar_ is read when a sandboxed process initializes. Restart already-running sandboxed processes after changing the setting; newly started processes receive the new value. There is no documented per-program syntax for this setting.

## Sandboxie Plus interface

The option is available at **Sandbox Options > General Options > Restrictions > Other restrictions** under the label **Allow sandboxed windows to cover the taskbar**.

The checkbox is unchecked by default and is enabled only when **Prevent interference with the user interface (Experimental)** is enabled. It has no dedicated tooltip.

## Version history

_AllowCoverTaskbar_ was introduced in Sandboxie Plus 1.14.2 as a compatibility option for _BlockInterferenceControl_. Its default remains disabled.

## Related settings

* [Sandboxie Ini](SandboxieIni.md)
* `BlockInterferenceControl` is the direct dependency of this setting.
* [Border Exclude Taskbar](BorderExcludeTaskbar.md) independently controls Sandboxie Plus's visual border overlay; it does not alter application-window restrictions.
