Sandboxie Plus offers a multitude of new functionality which improves security, compatybility and the overall sandboxing expirience.

Some of these features (*) are howeever only avaiable to users with a [Support Certificate](supporter-certificate) which can be obtained by [contributing to the sandboxie project](contribute.md) or purchased in our [online shop](https://xanasoft.com/shop/).

Some more features (**) are available to participants of the [Sandboxie-Insider](sandboxie-insider) program which.


#### [Rule Specificity](RuleSpecificity.md) *
 - With this option rules are prioritized based on their specificity (see changelog/docs for details) this way sub paths can be readable/writeable while parent parts are still protected.


#### [Security enhanced sandboxes](security-mode) *
 - Restrict syscall elevation to approved known safe / filtered sys calls
 - Limit access to device endpoints to known safe / filtered endpoints

#### [Privacy enhanced Sandboxes](privacy-mode) *
- With this applying a preset rule collection all locations potentially containing personal data can be protected. Applications running in boxes with personal data protection will see an empty PC with no user data on it.


#### [Compartment Mode](compartment-mode) *
 - This mode is intended to optimize compatibility at the cost of security, here sandboxie’s token-based isolation scheme is not used. Isolation is limited to the FS minifilter as well as registry and object callbacks. This has the potential to greatly improve compatibility with variouse applications.


#### Virtual Disk Integration **
 - [RamDisk support](ramdisksupport.md), available since the latest insider build, allows you to create a virtual disk in your system's memory, using the ImDisk driver, which can speed up file access and increase confidentiality as all box contents will be discarded when the disk is unmounted (manually or automatically on reboot). 
 - [Encrypted Box Image support](boxencryption.md) is currently in development and allows you to create encrypted sandboxed environments for an even greater protection of your confidential data. With this feature the box file root is being mounted from an AES-XTS encrypted box image, other ciphers are available as well. Upcoming additions to this root functionality will contain secure box passphrase handling and a driver extension to prevent applications not running in the encrypted sandbox from accessing the sandboxed files.



#### Enchanced network filering and redirection **
 - [Proxy injection](ProxySupport.md) is yet another feature which has been added in the insider builds, it allows to force any application to use a Socks 5 proxy instead of a direct connection. 
 - [DNS query logging, filtering and redirection](DNSFilter.md) feature allows you to block, or redirect DNS queries made by sandboxed programs for selected domains.



#### [WFP (Windows Filtering Platform) support](WFPSupport.md)
 - With this feature Sandboxie can be like an application firewall which applies the rules on a per box bases allowing the same application access to the internet in one box while blocking it in another.


#### Windows 11 context menu integration


#### Process/Thread handle filtering (obCallbacks)
 - Using this mechanism greatly improves on isolation of processes and provides enhanced security.


#### Win32 syscall hooking
 - With this feature win32 sys calls can get the same treatment as NT sys calls which helps with graphics and hw acceleration.


#### New UI with dark mode and much more
 - Sandboxie-Plus bring an entirely new Qt based UI sandman.exe
 - Customizable per box run menu
 - Global hotkey to terminate all boxes
 - INI section editor for easy configuration of advanced options
 - Box event triggers/scripts
 - Ability to stop selected applications from running globally, regardless of box presets


#### [Snapshots](BoxSnapshots.md)
 - Sandboxie-Plus can create box snapshots, with them it is possible to easily revert a box to a defined previous state.
 - Box set to auto delete will when available auto revert to the last snapshot allowing to benefit from a fresh clean box each time but with some preset configuration


#### [Enhanced debug/trace monitor](tracelog.md)


#### Fake admin privileges
 - Allows to make all processes in a box think thay have admin permissions and act accordingly, without the potential draw backs of granting them admin permissions


#### Box size monitor
 - Monitor and list box size in an own column


#### Start Menu integration
 - Integrate start menu entries from sandboxes into the host start menu


#### Sandbox SID isolation
 - Instead of using anonymous login SID use per box custom SID’s like Sandboxie/DefaultBox this way processes from separate boxes won’t be able accessing each other’s resources.


#### [Breakout Process](BreakOutProcess.md)
 - Allows to specifies which applications shall run unsandboxed when launched within the sandbox. A combination of this and ForceProcess allows for a simple priority system.

 - [Document BreakOut](breakoutdocument.md) is an extension to the already well-known Breakout mechanism to allow to open selected file types saved to an open file path from within the sandbox in an unsandbox instance of the associated application.  **


#### [USB drive sandboxing](usbsandboxing.md) **
- This feature allows you to automatically sandbox any USB drive that you plug into your computer, which adds an extra layer of protection to your system. 


#### EFS Support **
 - Support for EFS (Encrypted File System) protected files.


#### ARM64 support for windows 11 *
 - Support ARM64 natively
 - Support emulated x86
 - Support emulated x64 (ARM64EC)



