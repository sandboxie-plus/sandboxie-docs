# Use Ram Disk

_UseRamDisk_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) (introduced in v1.11.0 / 5.66.0) that replaces the standard file system storage with a RAM-based virtual disk as the sandbox root directory.

> [!WARNING]
> Configure this setting on a per-sandbox basis. Applying it globally will force all sandboxes to use RAM disks, which may break existing sandboxes that rely on standard file system storage or cause compatibility issues with non-volatile sandbox configurations.

> [!NOTE]
> This setting requires an active [supporter certificate](https://sandboxie-plus.com/supporter-certificate/).

## Prerequisites

- Install the **ImDisk Toolkit** via the **Add-Ons Manager > Optional Add-Ons** tab in **Global Settings**.

    ![ImDisk Install](../Media/UseRamDisk1.png)

- Configure the [RamDiskSizeKb](RamDiskSizeKb.md) setting to define the RAM disk's size in kilobytes. Choose a value that aligns with your system's available memory and the needs of the applications you plan to run sandboxed.

- (Optional) Use the [RamDiskLetter](RamDiskLetter.md) setting to assign a specific drive letter for easier access to the RAM disk.

## Usage

```ini
[DefaultBox]

UseRamDisk=y
```

When this setting is enabled, the Sandboxie service creates a virtual disk entirely in system RAM. The RAM disk is mounted through the mount manager[^1] using the ImDisk virtual disk driver. All file I/O operations within the sandbox are redirected to the RAM disk rather than creating files directly on the host file system or persistent storage.

The RAM disk provides extremely fast file operations but is volatile - all data is lost when the RAM disk is unmounted or the system is restarted. This makes it ideal for temporary operations, testing, or malware analysis where persistence is not required.

## SandMan GUI

The RAM disk setting can be enabled through:

1. Right-click sandbox > `Sandbox Options`.
2. Navigate to `File Options` tab.
3. Enable the `Store the sandbox content in a Ram Disk` setting.

    ![Ram Disk Enable](../Media/UseRamDisk2.png)

## Technical Implementation

RAM disk mounting is handled by the service which verifies driver capabilities and available system memory before attempting to mount the virtual disk[^2]. The RAM disk I/O operations are managed by the `VirtualMemoryIO` class[^3] which interfaces with the ImDisk driver[^4].

If insufficient RAM is available or mounting fails, the sandbox will not start and an error is logged.

## Technical Notes

- Requires ImDisk driver support for virtual memory operations[^4].
- Mutually exclusive with [UseFileImage](UseFileImage.md).
- All data is volatile and lost when the RAM disk is unmounted.
- RAM usage is allocated from system memory pool using `VirtualMemoryIO` class[^3].
- No encryption or password protection available.
- No backup/restore functionality - data is inherently temporary.
- Performance significantly faster than file-based storage.
- Maximum size limited by available system RAM, defined by `RamDiskSizeKb`.

## Performance Considerations

- Ideal for temporary operations, testing, or malware analysis.
- Reduces disk I/O and wear on SSDs.
- May cause system instability if RAM disk size exceeds available memory.
- Monitor system memory usage when using large RAM disks.
- Perfect for scenarios where data persistence is not needed.

[^1]: `MountManager::AcquireBoxRoot` in `Sandboxie/core/svc/MountManager.cpp` - handles RAM disk mounting process.
[^2]: Driver capability checks performed in `MountManager::AcquireBoxRoot` before mounting virtual disks.
[^3]: RAM disk I/O operations handled by `VirtualMemoryIO` class in `SandboxieTools/ImBox/VirtualMemoryIO.cpp`.
[^4]: ImDisk driver headers and definitions in `SandboxieTools/ImDisk/inc/imdisk.h`.

Related [Sandboxie Ini](SandboxieIni.md), [RamDiskSizeKb](RamDiskSizeKb.md), [RamDiskLetter](RamDiskLetter.md), [UseFileImage](UseFileImage.md), [FileRootPath](FileRootPath.md)