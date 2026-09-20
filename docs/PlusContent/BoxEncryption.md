# Encrypted Sandboxes

Sandboxie Plus can store a sandbox root, including its registry hive, in a password-protected encrypted disk image. The current implementation uses ImBox and the cryptographic implementation from DiskCryptor; images created through SandMan use AES-XTS.

Encrypted storage is one layer of protection. It is separate from Sandboxie's runtime isolation and from the settings that restrict host access to sandboxed processes.

## At-rest encrypted storage

When the image is not mounted, the sandbox content is stored in its encrypted `.box` backing file. Starting a program in the sandbox mounts the image after the correct password is supplied and makes its filesystem available to Sandboxie. SandMan can unmount it when the last sandboxed process stops.

Encryption protects the backing storage while it is unmounted. While the image is mounted, programs in the sandbox and the Sandboxie components needed to operate it can access the mounted filesystem according to the active sandbox policy. Encryption does not replace file, registry, IPC, network, clipboard, GUI, or other resource controls.

Encrypted images require the ImDisk driver and a currently applicable Support Certificate. Damage to the image or its encryption header can make its content inaccessible, so encrypted sandboxes still require backups.

## Root protection while mounted

The mount dialog offers **Protect Box Root from access by unsandboxed processes**. When selected, SbieDrv restricts direct filesystem access to the mounted sandbox root from unrelated host processes. The sandbox that owns the root, SbieSvc, required Windows components, and an allowed session leader are exceptions needed to operate the box.

[ProtectAdminOnly](../Content/ProtectAdminOnly.md) controls whether a non-administrative SandMan or Sandboxie Control session leader receives that exception. **Force protection on mount** can make root protection mandatory for subsequent mounts.

Root protection applies to the mounted root path. It is not a universal data-flow control and does not prevent a sandboxed application from using other channels that its sandbox policy permits.

## Confidential-box protection

[ConfidentialBox](../Content/ConfidentialBox.md) is an independent runtime setting. It restricts unsandboxed host processes from obtaining handles to sandboxed processes and threads, subject to documented operational exceptions. `DenyHostAccess` supplies per-program allow or deny rules for the same protection path.

The **Black Box** preset combines encrypted backing storage with `ConfidentialBox=y`. Enabling **Encrypt sandbox content** on an existing sandbox does not, by itself, enable every confidential-box or image-protection setting.

[ProtectHostImages](../Content/ProtectHostImages.md) is another independent feature. It restricts sandboxed processes whose executable comes from the host from loading executable images from the sandbox. It does not encrypt storage or control host process handles.

## SandMan configuration

Configure encrypted storage under:

**Sandbox Options > General Options > File Options**

The relevant controls are:

- **Encrypt sandbox content** — stores the box root in an encrypted disk image.
- **Set Password** or **Change Password** — creates or updates the image password.
- **Force protection on mount** — prevents root protection and automatic unmount from being disabled in the mount dialog.

When mounting an image, SandMan also offers:

- **Protect Box Root from access by unsandboxed processes**.
- **Lock the box when all processes stop.**

For access to selected host files from inside the sandbox, configure the normal resource-access rules, such as [OpenFilePath](../Content/OpenFilePath.md), as appropriate. Those rules deliberately permit the specified access and should be reviewed as part of the box's data-flow policy.

## Security boundary

Encrypted storage, root protection, and confidential-process protection address different paths. Together they reduce several forms of offline and runtime host access, but they do not establish that data cannot leave a running sandbox. If a sandboxed application is allowed to use a network connection, an open host path, IPC, the clipboard, or another permitted channel, these settings do not block that channel merely because the box is encrypted or confidential.

## Version history

Encrypted sandbox support and `UseFileImage` were introduced in Sandboxie Plus 1.11.0 / Classic 5.66.0. Confidential process protection predates encrypted images; `ConfidentialBox` and `DenyHostAccess` were introduced in Sandboxie Plus 1.3.3 / Classic 5.58.3.

## Related pages

- [Black Box](black-box.md)
- [Confidential Box](../Content/ConfidentialBox.md)
- [Protect Admin Only](../Content/ProtectAdminOnly.md)
- [Protect Host Images](../Content/ProtectHostImages.md)
- [Box Preset Comparison](box-preset-comparison.md)
