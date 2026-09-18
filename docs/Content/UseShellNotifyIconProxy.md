# Use Shell Notify Icon Proxy

_UseShellNotifyIconProxy_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls whether supported `Shell_NotifyIcon` operations are routed through Sandboxie's GUI proxy so that notification-area icons can be created or updated through the real desktop shell.

```ini
[DefaultBox]
UseShellNotifyIconProxy=y
```

The setting may also be disabled or limited to a program:

```ini
UseShellNotifyIconProxy=n
UseShellNotifyIconProxy=program.exe,y
UseShellNotifyIconProxy=program.exe,n
```

Negated image selectors can be used to apply a rule to every program except one:

```ini
UseShellNotifyIconProxy=n
UseShellNotifyIconProxy=!program.exe,y
```

## Default behavior

The default depends on the sandbox's window-access configuration:

- When [`OpenWinClass=*`](OpenWinClass.md) is active, proxying is enabled by default. An explicit `UseShellNotifyIconProxy=n` disables it.
- Without `OpenWinClass=*`, proxying is disabled by default. An explicit `UseShellNotifyIconProxy=y` enables it.

The proxy route also requires Sandboxie's GUI proxy service to be available. Application Compartment mode and `NoSandboxieDesktop=y` do not use that service, so this setting cannot force the proxy route in those modes.

## Compatibility scope

This is a notification-area or tray-icon compatibility setting. It can help when a sandboxed program's tray icon does not appear or cannot be updated correctly through the direct path.

It does not proxy all shell APIs or window messages, grant general access to host windows, or change the configured `OpenWinClass` rules.

If the proxy transport cannot be used successfully, Sandboxie can fall back to the direct native notification-icon path. Applications should not rely on one specific Windows error for every failure case.

## Applying changes

Sandboxie checks this setting when notification-icon calls are handled, but the surrounding GUI mode and proxy availability are established when the process initializes. Restart the affected application after changing this setting or related GUI configuration.

This setting has no dedicated control in SandMan or Sandboxie Control Classic. Configure it manually in `Sandboxie.ini` or through the INI editor.

## Version history

- Sandboxie Plus 1.17.5 / Classic 5.72.5 introduced the proxy for tray-icon compatibility with `OpenWinClass=*`.
- Sandboxie Plus 1.18.4 / Classic 5.73.4 added explicit enablement outside `OpenWinClass=*` while retaining the conditional default.

## Related configuration

- [Open Win Class](OpenWinClass.md)
- [Sandboxie Ini](SandboxieIni.md)
