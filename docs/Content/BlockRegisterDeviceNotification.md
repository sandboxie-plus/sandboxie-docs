# Block Register Device Notification

`BlockRegisterDeviceNotification` is a box-wide Boolean setting in [Sandboxie Ini](SandboxieIni.md). When enabled, it suppresses device-notification registrations made through selected USER32 APIs. The default is `n`.

```ini
[DefaultBox]
BlockRegisterDeviceNotification=y
```

## Runtime behavior

When the setting is enabled, Sandboxie installs user-mode hooks for:

- `RegisterDeviceNotificationA`;
- `RegisterDeviceNotificationW`;
- `UnregisterDeviceNotification`.

The intercepted ANSI and Unicode registration calls do not invoke the underlying Windows registration function. Sandboxie clears the last-error value and returns a successful-looking placeholder handle, so the application can believe that registration succeeded even though no registration was made through that call. The intercepted unregister function likewise clears the last-error value and reports success without performing a real unregister operation.

The placeholder handle is an implementation detail and should not be relied upon by applications.

## Scope and limitations

This setting suppresses registrations made through `RegisterDeviceNotificationA/W`; it is not a universal block on every device-change or Plug and Play notification mechanism. The current implementation does not establish that a sandboxed application can never receive `WM_DEVICECHANGE`, broadcast notifications, Configuration Manager notifications, service notifications, or kernel-level notifications through other paths.

In particular, the driver's separate Configuration Manager filter does not currently deny the function associated with `CMP_Register_Notification`. That path is distinct from the USER32 registration functions intercepted by this setting.

## Applying changes

The setting can be specified for a sandbox or inherited through normal template and global configuration resolution. It has no documented executable-qualified syntax.

Sandboxie reads the effective value while initializing GUI hooks in the sandboxed process. Changing the setting does not dynamically install or remove those hooks in a process that has already initialized. Restart affected sandboxed applications, or recreate the sandboxed process tree, after changing it. A SandMan, service, or driver restart is not normally required.

## SandMan configuration

SandMan does not currently provide a dedicated checkbox for `BlockRegisterDeviceNotification`. Configure it manually in the sandbox's INI section.

## Relationship to other device features

[`OpenDevCMApi`](OpenDevCMApi.md) controls a separate driver filter for selected mutating Device Configuration Manager operations. The two settings operate independently.

[USB Drive Sandboxing](../PlusContent/USBSandboxing.md) is SandMan host-side automation that detects qualifying USB-backed volumes and maintains forced-folder rules. `BlockRegisterDeviceNotification` does not control that automation and does not prevent SandMan itself from observing device changes.

## Version history

Current setting metadata lists `BlockRegisterDeviceNotification` as introduced in Sandboxie Plus 1.9.5 / Classic 5.64.5. The corresponding runtime change made the notification-registration hooks conditional on this setting. The same release's changelog records a fix related to `RegisterDeviceNotificationW` registrations using `DBT_DEVTYP_DEVICEINTERFACE`.

## Related pages

- [Open Device Configuration Manager API](OpenDevCMApi.md)
- [USB Drive Sandboxing](../PlusContent/USBSandboxing.md)
- [Sandboxie Ini](SandboxieIni.md)
