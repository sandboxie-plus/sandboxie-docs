# Use Ram Disk

_UseRamDisk_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.11.0 / 5.66.0. It instructs Sandboxie to mount a RAM-based virtual disk as the sandbox root instead of using direct file system storage.

**Note:** This setting should be configured per sandbox rather than globally. Setting it globally will force all sandboxes to use RAM disks, which may cause system memory exhaustion and break existing sandboxes that rely on standard file system storage or persistent data.

Before enabling `UseRamDisk`, ensure that RAM disk support is installed in the `Global Settings` under the `Add-Ons Manager` tab. Additionally, you must configure the [RamDiskSizeKb](RamDiskSizeKb.md) setting to specify the size of the RAM disk in kilobytes. This value must be set according to the available system memory and the requirements of the applications you intend to run within the sandbox. The drive letter for the RAM disk can be assigned using the [RamDiskLetter](RamDiskLetter.md) setting, allowing for easier access to the RAM disk.

## Usage:

```ini
[DefaultBox]

UseRamDisk=y
```

When this setting is enabled, the Sandboxie service creates a virtual disk entirely in system RAM. The RAM disk is mounted through the mount manager[^1] using the ImDisk virtual disk driver. All file I/O operations within the sandbox are redirected to the RAM disk rather than creating files directly on the host file system or persistent storage.

The RAM disk provides extremely fast file operations but is volatile - all data is lost when the RAM disk is unmounted or the system is restarted. This makes it ideal for temporary operations, testing, or malware analysis where persistence is not required.

## SandMan GUI Operations

The RAM disk option can be enabled through:

1. Right-click sandbox > `Sandbox Options`
2. Navigate to `File Options` tab
3. Enable the `Store the sandbox content in a Ram Disk` option

## Technical Implementation

RAM disk mounting is handled by the service which verifies driver capabilities and available system memory before attempting to mount the virtual disk[^2]. The RAM disk I/O operations are managed by the `VirtualMemoryIO` class[^3] which interfaces with the ImDisk driver[^4].

If insufficient RAM is available or mounting fails, the sandbox will not start and an error is logged.

**Technical Notes:**

- Requires ImDisk driver support for virtual memory operations[^4]
- Mutually exclusive with [UseFileImage](UseFileImage.md)
- All data is volatile and lost when the RAM disk is unmounted
- RAM usage is allocated from system memory pool using `VirtualMemoryIO` class[^3]
- No encryption or password protection available
- No backup/restore functionality - data is inherently temporary
- Performance significantly faster than file-based storage
- Maximum size limited by available system RAM, defined by `RamDiskSizeKb`

**Performance Considerations:**

- Ideal for temporary operations, testing, or malware analysis
- Reduces disk I/O and wear on SSDs
- May cause system instability if RAM disk size exceeds available memory
- Monitor system memory usage when using large RAM disks
- Perfect for scenarios where data persistence is not needed

[^1]: `MountManager::AcquireBoxRoot` in `Sandboxie/core/svc/MountManager.cpp` - handles RAM disk mounting process
[^2]: Driver capability checks performed in `MountManager::AcquireBoxRoot` before mounting virtual disks
[^3]: RAM disk I/O operations handled by `VirtualMemoryIO` class in `SandboxieTools/ImBox/VirtualMemoryIO.cpp`
[^4]: ImDisk driver headers and definitions in `SandboxieTools/ImDisk/inc/imdisk.h`

Related [Sandboxie Ini](SandboxieIni.md), [RamDiskSizeKb](RamDiskSizeKb.md), [RamDiskLetter](RamDiskLetter.md), [UseFileImage](UseFileImage.md), [FileRootPath](FileRootPath.md)