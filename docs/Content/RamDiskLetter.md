# Ram Disk Letter

_RamDiskLetter_ is a global creation-time setting in [Sandboxie Ini](SandboxieIni.md) (introduced in v1.11.1 / 5.66.1) that optionally assigns a visible drive letter to the shared RAM-disk backend used by sandboxes with [UseRamDisk](UseRamDisk.md) enabled. It is not a separate drive-letter assignment for each box.

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

SandMan reads and writes the direct global value; effective configuration may also include applicable templates. It writes the canonical form shown above, such as `R:\`.

## Important Notes

- **Shared Drive Letter**: The configured letter refers to the shared RAM volume, not to an individual sandbox. A visible letter does not add an isolation or access-control boundary.

- **Optional Mapping**: Without an effective configured letter, the normal creation path still obtains a temporary free letter for creation/formatting and then attempts to remove that mapping. The sandbox can use its root junction without retaining a visible drive letter. A temporary free letter must still be available.

- **Available Drive Letters**: Use an unoccupied letter in the canonical `R:\` form. If an explicitly configured letter is invalid or already occupied during creation, that path does not automatically choose another letter and cannot proceed with the requested mount.

## Applying changes

Configure the desired letter before the shared RAM backend is newly created. Changing or clearing this setting, or reloading configuration, does not change the letter of an existing backend. A new value is used only when a later acquisition creates a new backend, not merely because a box is reopened. Preserve wanted volatile content before destroying the shared backend.

## Ease of access

Assigning a specific drive letter can make the RAM volume easier to browse and reference in file paths. It remains optional for normal sandbox operation.

## Related Settings

- [RamDiskSizeKb](RamDiskSizeKb.md) - Specifies the requested capacity of the shared RAM disk.
- [UseRamDisk](UseRamDisk.md) - Enables the use of a RAM disk for individual sandboxes.
