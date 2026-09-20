# Black Box

**Black Box** is the SandMan preset that combines two separate protections:

- [Encrypted sandbox storage](BoxEncryption.md), which places the sandbox root and registry hive in an encrypted disk image.
- [Confidential Box](../Content/ConfidentialBox.md), which restricts unsandboxed host processes from obtaining handles to sandboxed processes and threads.

The preset configures `UseFileImage=y` and `ConfidentialBox=y`. These settings remain separate mechanisms: encryption primarily protects the backing storage while it is unmounted, whereas confidential-box filtering acts while sandboxed processes are running.

Additional controls, including mounted-root protection, [ProtectAdminOnly](../Content/ProtectAdminOnly.md), `DenyHostAccess` exceptions, and [ProtectHostImages](../Content/ProtectHostImages.md), have their own scope and defaults.

Black Box does not mean that every communication or data-transfer path is blocked. Normal Sandboxie file, registry, IPC, network, clipboard, GUI, and other policies continue to determine which operations are permitted while the box is running.
