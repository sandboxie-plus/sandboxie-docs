# USB Drive Sandboxing

USB Drive Sandboxing is SandMan automation built on Sandboxie's [forced-folder mechanism](../Content/ForceFolder.md). SandMan maintains `ForceFolder` entries for the mount points of qualifying USB-backed volumes. Programs launched from those forced locations are then handled by the designated sandbox.

This feature does not place the USB device itself inside a sandbox, virtualize USB device I/O, or sandbox every program that accesses files on the volume. Its security effect depends on which programs are forced and on the configuration of the designated sandbox.

## Qualifying storage

SandMan enumerates Windows volumes and their backing disks. A volume qualifies when at least one backing disk is reported through the `USBSTOR` enumerator. This can include USB flash drives, USB hard drives, and USB SSDs.

Qualification is not based only on a drive letter, the removable-media attribute, the filesystem, or the volume label. A normal network drive or a `SUBST`/remapped path therefore does not qualify merely because it appears as a drive. For a volume spanning multiple disk extents, the current implementation treats the volume as USB-backed if at least one backing disk is identified as `USBSTOR`.

## Configuration

USB Drive Sandboxing is global configuration and is disabled by default. Automatic maintenance requires an active applicable [Support Certificate](supporter-certificate.md).

```ini
[GlobalSettings]
ForceUsbDrives=y
UsbSandbox=USB_Box
```

`ForceUsbDrives=y` enables SandMan's automatic maintenance of USB forced-folder rules. When the setting is false or absent, SandMan does not rebuild the USB forced-folder list. It is not a low-level USB blocking policy. `UsbSandbox` names the sandbox that receives the generated rules; if it is absent, SandMan uses `USB_Box`.

If the designated sandbox does not exist, SandMan attempts to create it. A sandbox created by this operation is a normal sandbox, not a special USB security type. SandMan currently adds these settings to a sandbox that it creates successfully:

```ini
UseFileDeleteV2=y
UseRegDeleteV2=y
UseVolumeSerialNumbers=y
```

If creation fails, SandMan cannot update the missing sandbox's forced-folder rules. `UseVolumeSerialNumbers` controls how that sandbox stores paths and is separate from the volume serial numbers used for USB exclusions.

## Generated `ForceFolder` rules

For each qualifying volume that is not excluded, SandMan collects its current mount points and writes them as direct `ForceFolder` entries in the designated sandbox.

!!! warning
    USB refreshes replace the designated sandbox's direct `ForceFolder` list with the currently qualifying USB mount points. Do not use that direct list for unrelated persistent manual rules, and do not manually maintain USB drive letters there while automatic USB management is enabled. This replacement concerns the box's direct list; it does not imply that inherited or template configuration is rewritten.

    Disabling `ForceUsbDrives` or losing the required active certificate stops automatic maintenance but does not remove previously generated direct entries. Changing `UsbSandbox` makes subsequent refreshes maintain the new box, but generated direct entries in the former box are not cleaned automatically. Review and remove stale direct `ForceFolder` entries manually when disabling the feature or changing its designated sandbox.

The resulting rules affect programs launched from the forced locations according to normal `ForceFolder` behavior. They do not redirect every read or write performed by an otherwise unsandboxed host program.

## Excluding volumes

`DisabledForceVolume` is a repeatable global setting that excludes specific volumes from automatic USB sandboxing:

```ini
[GlobalSettings]
DisabledForceVolume=1234-ABCD
DisabledForceVolume=5678-EF90
```

Each value is the Windows volume serial number formatted by SandMan as `XXXX-XXXX` in uppercase hexadecimal. It is not a drive letter, volume GUID path, USB hardware ID, or physical drive firmware serial number.

Because an exclusion follows the Windows volume serial, changing a drive letter normally does not invalidate it. Reformatting or recreating the filesystem can change that serial, so the stored exclusion might no longer match.

## SandMan interface

Open **Global Settings > Program Control > USB Drive Sandboxing**. This page provides:

- **Automatically sandbox all attached USB drives** — enables or disables `ForceUsbDrives`.
- **Sandbox for USB drives:** — selects the designated sandbox.
- A volume list with **Volume** and **Information** columns. A checked USB-backed volume is included; clearing its checkbox stores its serial in `DisabledForceVolume`.

An excluded volume that is not currently connected can remain listed by serial as **Volume not attached**. The sandbox selector and volume list require an active applicable Support Certificate.

## Drive updates

SandMan rebuilds the generated rules when it refreshes drive information, including after relevant device-change notifications, and after USB settings are applied. SandMan must therefore be running to reflect newly attached or removed qualifying volumes automatically.

If SandMan is not running, previously generated `ForceFolder` entries remain in the configuration, but arrivals and removals are not recomputed by an independent USB policy engine.

## Version history

`ForceUsbDrives`, `UsbSandbox`, and `DisabledForceVolume` are listed as added in version 1.12.0; the corresponding release pair was Sandboxie Plus 1.12.0 / Classic 5.67.0. The automatic USB maintenance described on this page is implemented by SandMan. Current automatic USB sandboxing requires an active applicable Support Certificate and is not Insider-exclusive.
