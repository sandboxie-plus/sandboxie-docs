# Notify Direct Disk Access

_NotifyDirectDiskAccess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It defaults to `n`.

```ini
[DefaultBox]
NotifyDirectDiskAccess=y
```

When enabled, Sandboxie issues [SBIE1313](SBIE1313.md) when an attempt to open a disk device itself remains denied. It does not report every form of raw-disk activity or a request for a remaining path below the device.

This setting controls the notification only. It does not grant direct disk access or alter the policy that denied the request. Access-related settings such as [Allow Raw Disk Read](AllowRawDiskRead.md), [Open File Path](OpenFilePath.md), and [Open Pipe Path](OpenPipePath.md) are separate.

In Sandboxie Plus, open **Sandbox Options > General Options > File Options**, find **Disk/File access**, and select **Warn when an application opens a harddrive handle**. Sandboxie Control Classic has no equivalent dedicated current control.

The value is cached when the sandboxed process initializes. Restart affected sandboxed processes after changing it for predictable behavior.

See [Notification Settings](NotificationSettings.md) for the distinction between access policy, message generation, and presentation.
