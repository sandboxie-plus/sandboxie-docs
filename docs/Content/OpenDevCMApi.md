# Open Device Configuration Manager API

`OpenDevCMApi` is a box-wide Boolean setting in [Sandboxie Ini](SandboxieIni.md). It disables Sandboxie's selective filter for certain mutating Windows Device Configuration Manager operations. The default is `n`.

```ini
[DefaultBox]
OpenDevCMApi=y
```

!!! warning
    Enabling this setting can allow an elevated sandboxed process to make host hardware-configuration changes that persist after the sandbox is deleted. It does not grant unrestricted access to all hardware, bypass Windows access checks, or disable other Sandboxie resource restrictions.

## What is filtered

With the default `OpenDevCMApi=n`, the Sandboxie driver examines device-control requests directed to the Configuration Manager API endpoint:

```text
\Device\DeviceApi\CMApi
```

Selected mutating operations are denied with an access-denied status. The current filter covers categories including:

- changing software-device properties or lifetime;
- registering software-device interfaces and changing their state or properties;
- setting device-node, device-interface, or device-class properties;
- setting device-class or device-node registry properties;
- setting device-node problem state;
- disabling device nodes or requesting removal of a device subtree;
- registering or unregistering device interfaces;
- creating or uninstalling device nodes;
- deleting device-interface, device-node, or device-class keys.

This is a selective deny list, not a complete block on the Configuration Manager API. Current query and read operations are generally passed through, including representative operations for enumerating devices or classes, reading properties, querying device-node status or depth, resolving interface aliases, validating device instances, and opening related registry keys. Other operations not selected by the filter also continue to the underlying Windows device-control path.

`OpenDevCMApi=y` skips this CMApi-specific mutation filter. The underlying operation is still subject to Windows permissions and any independent Sandboxie controls, so the setting does not guarantee that a requested hardware-management operation will succeed. It also does not itself change whether the CMApi device object can be opened.

## Why the filter exists

The filter was introduced for Security Issue ID-14 after [issue #552](https://github.com/sandboxie-plus/Sandboxie/issues/552) demonstrated that an elevated process could use Device Manager from inside a sandbox to remove host devices. Those changes affected the host and persisted independently of sandbox deletion.

Use `OpenDevCMApi=y` only as a compatibility exception for software that genuinely requires one of the filtered device-management operations.

## Compatibility

Sandboxie Plus 0.7.1 / Classic 5.48.5 refined the filter to fix webcam-access problems while keeping the selected mutation restrictions. Ordinary webcam access should therefore not be assumed to require `OpenDevCMApi=y`.

## Applying changes

The setting can be specified for a sandbox or inherited through normal template and global configuration resolution. It has no documented executable-qualified syntax.

The driver caches the effective value when initializing each sandboxed process. Restart affected sandboxed applications, or recreate the sandboxed process tree, after changing the setting. A SandMan, service, or driver restart is not normally required for newly started processes.

## SandMan configuration

The control is under:

**Sandbox Options > General Options > Isolation > Allow sandboxed programs to manage Hardware/Devices**

The checkbox is clear by default. Selecting it writes `OpenDevCMApi=y`, which is the less-restricted compatibility state. SandMan disables the control when **No Security Isolation** is selected.

## Relationship to other device features

[`BlockRegisterDeviceNotification`](BlockRegisterDeviceNotification.md) controls separate user-mode hooks for device-notification registration. It does not enable or disable the CMApi mutation filter.

[USB Drive Sandboxing](../PlusContent/USBSandboxing.md) is also independent. That feature is SandMan automation that maintains forced-folder rules for qualifying USB-backed volumes; it does not use `OpenDevCMApi` to virtualize or control the USB device.

## Version history

| Change | Version |
| --- | --- |
| CMApi mutation filter and `OpenDevCMApi` compatibility setting introduced | Sandboxie Plus 0.7.0 / Classic 5.48.0 |
| Webcam compatibility with the filter enabled improved | Sandboxie Plus 0.7.1 / Classic 5.48.5 |

## Related pages

- [Block Register Device Notification](BlockRegisterDeviceNotification.md)
- [USB Drive Sandboxing](../PlusContent/USBSandboxing.md)
- [Sandboxie Ini](SandboxieIni.md)
