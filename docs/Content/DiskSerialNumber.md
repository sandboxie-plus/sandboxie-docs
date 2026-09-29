# Disk Serial Number

_DiskSerialNumber_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.2 / 5.70.2. It provides a custom Windows **volume serial number** for software using the `GetVolumeInformationByHandleW` path intercepted by [Hide Disk Serial Number](HideDiskSerialNumber.md). It does not change the manufacturer's physical disk serial number or every way of identifying a disk.

## Syntax and examples

An unqualified value can be used as the general replacement, or a device name can select a specific volume:

```ini
DiskSerialNumber=1234-ABCD
DiskSerialNumber=HarddiskVolume1,1234-ABCD
```

For example, a box can configure different values for named volumes:

```ini
[DefaultBox]
HideDiskSerialNumber=y
DiskSerialNumber=HarddiskVolume1,1234-ABCD
DiskSerialNumber=HarddiskVolume2,5678-EF01
DiskSerialNumber=HarddiskVolume3,9ABC-DEF0
```

The device selector is the first component after `\Device\` in the NT path resolved for the queried handle; `HarddiskVolume1` is an example, not a permanent mapping to a drive letter. It is not a program-name selector. A matching device-specific value takes precedence over an unqualified value. Windows drive-letter listings, Disk Management, and volume-serial commands do not by themselves establish which NT name this hook will resolve or whether an application uses the intercepted API.

## Value format and behavior

Use hexadecimal digits, optionally separated by hyphens, for example `1234ABCD`, `1234-ABCD`, `12-34-AB-CD`, or `DEADBEEF`. Conventional examples above represent four bytes. Non-hexadecimal characters and odd numbers of digits are invalid. If no applicable valid custom value is available, Sandboxie generates a replacement on this path; it does not thereby promise a fallback to the host serial.

An effective `HideDiskSerialNumber=y` value is required for the hook to use these entries. The setting can be useful for deterministic testing or compatibility with software that reads the volume serial through `GetVolumeInformationByHandleW`, but it does not prevent identification through other disk or volume APIs or WMI classes.

The replacement is cached within each sandboxed process by the original volume serial, not by device path. Repeated queries for that original serial reuse the chosen value; volumes sharing an original serial can share the first cached replacement in that process. Changing a custom value does not update an existing cache entry. Restart the affected sandboxed process to rebuild its cache.

If the expected value is not observed, check that `HideDiskSerialNumber` is effectively enabled, the custom value is valid hexadecimal, the selected NT device name matches, and the application actually uses the intercepted by-handle API. A different query path will not demonstrate this setting's effect.

## Configuration availability

SandMan has a **Hide Disk Serial Number** checkbox under **Sandbox Options > Advanced Options > Privacy**, but no dedicated editor for custom `DiskSerialNumber` values was identified. Custom values can be configured in the INI. The checkbox shows a direct box value, while an effective enable value can also come from applicable template or global configuration.

## Related settings

- [Hide Disk Serial Number](HideDiskSerialNumber.md) enables this volume-serial substitution path.
- [Hide Firmware Info](HideFirmwareInfo.md) affects a separate SMBIOS query path.
- [Hide Network Adapter MAC](HideNetworkAdapterMAC.md) affects a separate network-address path.
- [Random Registry UID](RandomRegUID.md) affects selected boxed Registry values.
