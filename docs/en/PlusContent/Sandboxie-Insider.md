The Sandboxie Plus Insider Program provides early access to new features and functionality that are not yet available to the public.

To become a participant in the Insider Program and gain access to the private GitHub repository with new releases, you must contribute to the project in a meaningful way, such as by helping with documentation, development, providing translations, or by submitting exceptional bug reports. Alternatively, you can support the project on Patreon at the GREAT tier or above. All users with CONTRIBUTOR or HUGE certificates are automatically eligible.

The insider builds introduce several new features that are designed to improve the Sandboxie experience and enhance the security of your system:

 - [RamDisk support](../PlusContent/RamDiskSupport.md), available since the latest insider build, allows you to create a virtual disk in your system's memory, using the ImDisk driver, which can speed up file access and increase confidentiality as all box contents will be discarded when the disk is unmounted (manually or automatically on reboot).

 - [Encrypted Box Image support](../PlusContent/BoxEncryption.md) is currently in development and allows you to create encrypted sandboxed environments for an even greater protection of your confidential data. With this feature the box file root is being mounted from an AES-XTS encrypted box image, other ciphers are available as well. Upcoming additions to this core functionality will contain secure box passphrase handling and a driver extension to prevent applications not running in the encrypted sandbox from accessing the sandboxed files.

 - [Proxy injection](../PlusContent/ProxySupport.md) is yet another feature which has been added in the insider builds, it allows to force any application to use a Socks 5 proxy instead of a direct connection.

 - [DNS query logging, filtering and redirection](../PlusContent/DNSFilter.md) feature allows you to block, or redirect DNS queries made by sandboxed programs for selected domains.

 - [USB drive sandboxing](../PlusContent/USBSandboxing.md) is yet another new feature that has been added to the Insider builds. This feature allows you to automatically sandbox any USB drive that you plug into your computer, which adds an extra layer of protection to your system.

 - Insider builds include support for EFS, which is a feature in Windows that allows you to encrypt files and folders to protect them from unauthorized access.

 - [Document Breakout](../Content/BreakoutDocument.md) is an extension to the already well-known Breakout mechanism to allow to open selected file types saved to an open file path from within the sandbox in an unsandbox instance of the associated application.

Please note that:

- The Sandboxie Plus insider builds are not like the Windows insider builds which are buggy and rushed.
- The new things in the insider builds are limited to new functionality and new features.
- Experimental things that may impact compatibility are tested in the public GitHub preview channel.
- The Sandboxie Plus insider builds are based on stable final releases, with new functionality added on top.
- The insider builds are compiled with Qt6 and provided as a unified x64/ARM64 installer.
