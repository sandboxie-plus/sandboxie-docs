# Black Box

**Black Box** is the New Box Wizard option that combines two separate protections while retaining the selected base box type:

- [Encrypted sandbox storage](BoxEncryption.md), which places the sandbox root and registry hive in an encrypted disk image.
- [Confidential Box](../Content/ConfidentialBox.md), which restricts unsandboxed host processes from obtaining handles to sandboxed processes and threads.

In the normal New Box Wizard workflow, selecting **Encrypt Box content and set Confidential** adds `UseFileImage=y` and `ConfidentialBox=y` to the base configuration. These settings remain separate mechanisms: encryption primarily protects the backing storage while it is unmounted, whereas confidential-box filtering acts while sandboxed processes are running.

The base can be Standard, [Security Hardened](security-mode.md), or [Application Compartment](compartment-mode.md), each with or without [Data Protection](privacy-mode.md). After creation, **Box Type Preset:** selects among these six base combinations; encryption and Confidential Box are configured independently.

SandMan can display the combined encrypted/confidential presentation independently of the underlying base mode, including for an existing box configured with both settings. The wizard still chooses the border color from the selected base type, rather than inherently changing it to black. Colors and icons are not enforcement guarantees; see [Box Presentation](../Content/BoxPresentation.md).

Additional controls, including mounted-root protection, [ProtectAdminOnly](../Content/ProtectAdminOnly.md), `DenyHostAccess` exceptions, and [ProtectHostImages](../Content/ProtectHostImages.md), have their own scope and defaults.

Black Box does not mean that every communication or data-transfer path is blocked. Normal Sandboxie file, registry, IPC, network, clipboard, GUI, and other policies continue to determine which operations are permitted while the box is running.
