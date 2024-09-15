Sandboxie Plus user interface offers a multitude of new functionality which improves security, compatibility and the overall sandboxing experience.

Some of these features (*) are however only available to users with a [Support Certificate](../PlusContent/supporter-certificate.md) which can be obtained by [contributing to the Sandboxie project](https://github.com/sandboxie-plus/Sandboxie/blob/master/CONTRIBUTING.md) or purchased in our [online shop](https://xanasoft.com/shop/).

Some more features (**) are available to participants of the [Sandboxie-Insider](../PlusContent/Sandboxie-Insider.md) program.

#### [Rule Specificity](../PlusContent/RuleSpecificity.md) *
 - With this option rules are prioritized based on their specificity (see changelog/docs for details) this way sub paths can be readable/writeable while parent parts are still protected.


#### [Security enhanced sandboxes](../PlusContent/security-mode.md) *
 - Restrict syscall elevation to approved known safe / filtered syscalls
 - Limit access to device endpoints to known safe / filtered endpoints


#### [Privacy enhanced sandboxes](../PlusContent/privacy-mode.md) *
- With this feature, by applying a preset rule collection, all locations potentially containing personal data can be protected. Applications running in boxes with personal data protection will see an empty PC with no user data on it.


#### [Compartment Mode](../PlusContent/compartment-mode.md) *
 - This mode is intended to optimize compatibility at the cost of security, here Sandboxie’s token-based isolation scheme is not used. Isolation is limited to the FS minifilter as well as registry and object callbacks. This has the potential to greatly improve compatibility with various applications.


#### Virtual Disk Integration **
 - [RamDisk support](../PlusContent/RamDiskSupport.md), available since the latest insider build, allows you to create a virtual disk in your system's memory, using the ImDisk driver, which can speed up file access and increase confidentiality as all box contents will be discarded when the disk is unmounted (manually or automatically on reboot).
 - [Encrypted Box Image support](../PlusContent/BoxEncryption.md) is currently in development and allows you to create encrypted sandboxed environments for an even greater protection of your confidential data. With this feature the box file root is being mounted from an AES-XTS encrypted box image, other ciphers are available as well. Upcoming additions to this root functionality will contain secure box passphrase handling and a driver extension to prevent applications not running in the encrypted sandbox from accessing the sandboxed files.


#### Enhanced network filtering and redirection **
 - [Proxy injection](../PlusContent/ProxySupport.md) is yet another feature which has been added in the insider builds, it allows to force any application to use a Socks 5 proxy instead of a direct connection.
 - [DNS query logging, filtering and redirection](../PlusContent/DNSFilter.md) feature allows you to block, or redirect DNS queries made by sandboxed programs for selected domains.


#### [WFP (Windows Filtering Platform) support](../PlusContent/WFPSupport.md)
 - With this feature, Sandboxie can be like an application firewall which applies the rules on a per-sandbox basis, allowing the same application access to Internet in one box while blocking it in another.


#### Windows 11 context menu integration


#### Process/Thread handle filtering (obCallbacks)
 - Using this mechanism greatly improves on isolation of processes and provides enhanced security.


#### Win32 syscall hooking
 - With this feature, Win32 syscalls can get the same treatment as NT syscalls, which helps with graphics and HW acceleration.


#### New UI with dark mode and much more
 - Sandboxie-Plus bring an entirely new Qt based UI sandman.exe
 - Customizable per box run menu
 - Global hotkey to terminate all boxes
 - INI section editor for easy configuration of advanced options
 - Box event triggers/scripts
 - Ability to stop selected applications from running globally, regardless of box presets


#### [Snapshots](../PlusContent/BoxSnapshots.md)
 - Sandboxie-Plus can create box snapshots, with them it is possible to easily revert a box to a defined previous state.
 - Box set to auto delete will auto-revert when available to the last snapshot allowing to benefit from a fresh clean box each time but with some preset configuration


#### [Enhanced debug/trace monitor](../PlusContent/TraceLog.md)


#### Fake admin privileges
 - Allows to make all processes in a box think they have admin permissions and act accordingly, without the potential drawbacks of granting them admin permissions


#### Box size monitor
 - Monitor and list box size in an own column


#### Start Menu integration
 - Integrate start menu entries from sandboxes into the host start menu


#### Sandbox SID isolation
 - Instead of using anonymous login SID, it uses custom SIDs per-sandbox like Sandboxie/DefaultBox. This way, processes from separate sandboxes won’t be able accessing each other’s resources.


#### [Breakout Process](../Content/BreakoutProcess.md)
 - Allows to specify which applications shall run unsandboxed when launched within the sandbox. A combination of this and ForceProcess allows for a simple priority system.
 - [Document Breakout](../Content/BreakoutDocument.md) is an extension to the already well-known Breakout mechanism to allow to open selected file types saved to an open file path from within the sandbox in an unsandboxed instance of the associated application.  **


#### [USB drive sandboxing](../PlusContent/USBSandboxing.md) **
- This feature allows you to automatically sandbox any USB drive that you plug into your computer, which adds an extra layer of protection to your system.


#### EFS Support **
 - Support for EFS (Encrypted File System) protected files.


#### ARM64 support for Windows 11 *
 - Support ARM64 natively
 - Support emulated x86
 - Support emulated x64 (ARM64EC)
