# RamDiskSandboxes

## RAM Disk Support

Sandboxie Plus can store sandbox contents on a RAM-backed virtual disk through ImBox and the [ImDisk Driver](../PlusContent/imdisk.md). Sandboxes using RAM backing share one volume, with a separate directory for each box.

## Performance Amplification

RAM-backed storage can benefit some temporary-file workloads. Performance depends on the workload and system memory pressure; it does not guarantee faster operation than persistent storage.

## Privacy Enhancement

Content stored only on the shared RAM disk is volatile and is lost when that backend is actually destroyed. Ending sandboxed processes, closing one sandbox, or closing SandMan does not itself establish that the shared RAM disk has been destroyed. Recover or export wanted files to persistent storage beforehand; do not rely on RAM-only content surviving a reboot.

Volatility does not guarantee that data cannot reach a page file or other persistent storage, and it is not a guarantee of secure erasure.

## Integrating RAM Disk Support: Step by Step

For prerequisites and detailed storage behavior, see [Use Ram Disk](../Content/UseRamDisk.md).

### Updating Sandbox Configuration:

Add the following line to the intended sandbox's section in **[Sandboxie Ini](../Content/SandboxieIni.md)**:

    UseRamDisk=y

### Configuring Global Settings:

In the `[GlobalSettings]` section of **[Sandboxie Ini](../Content/SandboxieIni.md)**, set the requested capacity of the shared RAM disk:

    RamDiskSizeKb=2097152

This example requests 2097152 KiB (2 GiB). It sets the shared capacity used when a new backend is created; it does not automatically enable RAM backing for every sandbox or resize an existing RAM disk. See [Ram Disk Size Kb](../Content/RamDiskSizeKb.md) for creation limits and applying changes.

Data memory is committed progressively as the backing is populated. The configured capacity is not an immediate reservation of that much physical RAM. Choose it according to the intended workloads and available system resources, leaving room for Windows and applications. Monitor both system memory and free space on the shared volume; allocating half of physical RAM is not universally safe.
