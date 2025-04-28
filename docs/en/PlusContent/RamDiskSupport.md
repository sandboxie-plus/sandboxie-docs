# RamDiskSandboxes

## RAM Disk Support

By seamlessly interfacing with the [ImDisk Driver](../PlusContent/imdisk.md), Sandboxie Plus introduces a transformative way to allocate a portion of your system RAM for dynamic RAM Disks. This mechanism revolutionizes the speed and efficiency of your sandboxes, while also conferring distinct privacy advantages.

## Performance Amplification

The hallmark benefit of RAM Disk Support is the remarkable performance boost it offers. Sandboxes configured with a RAM Disk can harness the lightning-fast data access and processing capabilities of your system's RAM. This means that operations within the sandbox occur at unprecedented speeds, without the constraints of traditional storage mediums.

## Privacy Enhancement

Beyond the performance gains, RAM Disk Support lends an added layer of privacy to your sandboxing endeavors. Data stored in a RAM Disk is inherently volatile – once the system is powered off or the sandbox is closed, the data vanishes. This ephemeral nature of a RAM Disk significantly reduces the potential for data leaks, as there's no persistent storage where sensitive information could inadvertently reside.

## Integrating RAM Disk Support: Step by Step

To fully embrace the potential of RAM Disk Support, follow these straightforward steps:

### Updating Sandbox Configuration:

Open the **[Sandboxie Ini](../Content/SandboxieIni.md)** configuration file for the sandbox you wish to enhance. To enable the RAM Disk for this sandbox, include the following line within the respective sandbox's section:

    UseRamDisk=y

### Configuring Global Settings:

To enable RAM Disk Support across all your sandboxes, navigate to the [GlobalSettings] section within the **[Sandboxie Ini](../Content/SandboxieIni.md)** file. Allocate the appropriate memory for the RAM Disk by adding this line:

    RamDiskSizeKb=2097152

This value designates the maximum size of the RAM Disk in Kilobytes. For optimal results, allocate at least 1GB of RAM to the RAM Disk.

A key point to remember is the dynamic allocation of memory by RAM Disk Support. Unlike conventional storage, memory is utilized on-demand, ensuring optimal resource management. This intelligent allocation means you can allocate up to half of your system's physical RAM without encountering issues.
