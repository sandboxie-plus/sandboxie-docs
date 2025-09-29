# Ram Disk Letter

_RamDiskLetter_ is a global setting in [Sandboxie Ini](SandboxieIni.md) (introduced in v1.11.1 / 5.66.1) that specifies the drive letter to be assigned to the RAM disk created for use by sandboxes that have the [UseRamDisk](UseRamDisk.md) setting enabled. This setting allows users to define a specific drive letter for easier access to the RAM disk.

## Usage

To set the `RamDiskLetter`, add the following line to the Sandboxie configuration file under the `[GlobalSettings]` section:

```ini
[GlobalSettings]

# Example for assigning the drive letter R to the RAM disk
RamDiskLetter=R:\
```

## SandMan GUI

The RAM disk letter setting can be selected through:

1. Open the `Global Settings` window in the SandMan interface.
2. Navigate to `Add-Ons Manager` > `Add-On Configuration` tab.
3. Enable the `Assign drive letter to Ram Disk` setting and select a drive letter for the RAM disk.

    ![Ram Disk Letter](../Media/UseRamDisk3.png)

## Important Notes

- **Single Drive Letter**: Only one drive letter can be assigned to the RAM disk, and it will be used across all sandboxes that utilize the RAM disk feature.

- **Available Drive Letters**: Ensure that the specified drive letter is not already in use by another drive or partition on the system. If the drive letter is already assigned, the RAM disk may fail to mount, and an error will be logged.

- **Configuration Requirement**: The `RamDiskLetter` setting should be configured before enabling `UseRamDisk` in individual sandboxes to ensure proper assignment.

## Performance Considerations

- **Ease of Access**: Assigning a specific drive letter to the RAM disk can simplify access for applications and users, making it easier to reference the RAM disk in file paths.

## Related Settings

- [RamDiskSizeKb](RamDiskSizeKb.md) - Specifies the size of the RAM disk.
- [UseRamDisk](UseRamDisk.md) - Enables the use of a RAM disk for individual sandboxes.

By configuring the `RamDiskLetter` setting, users can enhance their Sandboxie experience by providing a consistent and easily accessible drive letter for the RAM disk.