# Hide Disk Serial Number

HideDiskSerialNumber is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```ini
[DefaultBox]
HideDiskSerialNumber=y
```

When enabled, Sandboxie substitutes the Windows **volume serial number** returned through the intercepted `GetVolumeInformationByHandleW` path. This is not the manufacturer's physical disk serial number. The replacement is either generated or supplied by [Disk Serial Number](DiskSerialNumber.md). Other disk and volume identification APIs may use different paths; this setting does not cover every disk identifier or WMI query.

Sandboxie calls the original Windows function and returns its Boolean result. Supplying a replacement serial does not convert an unsuccessful original call into success. A chosen replacement is cached in the sandboxed process for the original volume serial value. Changing a custom value does not replace an already-cached entry.

The runtime fallback is disabled when no effective value is configured. The Boolean lookup can be qualified by process image and can include applicable template or global configuration. Sandboxie reads the enable value and installs this hook during process initialization, so restarting affected sandboxed processes is the reliable way to apply a changed enable value or rebuild the replacement cache.

In **Sandbox Options > Advanced Options > Privacy**, **Hide Disk Serial Number** controls the direct box setting. An inherited effective value can differ from the checkbox state.
