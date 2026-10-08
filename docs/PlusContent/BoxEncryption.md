# Encrypted Sandboxes

Sandboxie Plus can store a sandbox root, including its registry hive, in an encrypted disk image. The normal service workflow uses ImBox and a DiskCryptor-derived cryptographic implementation with AES-XTS. This changes the physical backing beneath the file root, not Sandboxie's logical file virtualization.

Encrypted storage is one layer of protection. It is separate from Sandboxie's runtime isolation and from the settings that restrict host access to sandboxed processes.

## At-rest encrypted storage

When the image is not mounted, content stored inside it remains in the encrypted `.box` backing file. SandMan can prompt and pre-mount it before launching a program. Other startup paths can attempt service-side acquisition without an interactive password prompt and can fail if the image cannot be unlocked. Automatic unmount depends on the current mount option and successful Registry/root release and device cleanup.

This at-rest boundary does not automatically cover `Sandboxie.ini`, external header backups, recovered/exported files, host metadata, or every external application side effect.

Encryption protects the backing storage while it is unmounted. While the image is mounted, programs in the sandbox and the Sandboxie components needed to operate it can access the mounted filesystem according to the active sandbox policy. Encryption does not replace file, registry, IPC, network, clipboard, GUI, or other resource controls.

Encrypted images require an available ImDisk device/driver and a currently applicable active Support Certificate with the encryption feature. ImDisk supplies the virtual disk; ImBox supplies the encryption backing. Damage to the image or its encryption header can prevent access, so encrypted sandboxes still require backups.

## Password and header model

The standard Sandbox Options creation workflow expects a password. However, the low-level service can select encrypted backing with empty password input; encryption alone does not establish that a meaningful password was chosen. The normal workflow does not provide a reusable password vault or store the mount password in `Sandboxie.ini`.

Changing the password updates header/key-protection metadata rather than re-encrypting the entire payload. A header backup contains sensitive encryption material and is not a content backup. Restoring a matching older header overwrites the current header and can restore older password/key metadata; changing the password does not automatically invalidate all previous matching header backups. Neither recovery nor transactional rollback is guaranteed. See [Use File Image](../Content/UseFileImage.md) for password and header procedures.

## Root protection while mounted

The mount dialog offers **Protect Box Root from access by unsandboxed processes**. It requests a separate SbieDrv restriction on relevant new filesystem opens beneath the mounted disk root from unrelated host processes. Exceptions include the owning sandbox, SbieSvc, `csrss.exe`, and an allowed session leader. Previously obtained handles are not universally revoked; kernel-mode and other paths skipped by this check are outside its coverage. Windows filesystem permissions remain separate.

[ProtectAdminOnly](../Content/ProtectAdminOnly.md) controls whether the session-leader exception also requires administrative access; it is not a general exception for every administrator or SYSTEM process. [Force protection on mount](../Content/ForceProtectionOnMount.md) constrains SandMan's reviewed mount workflow to request protection, not every service caller. A protection request can fail without failing the image mount, so protected mounting is not a fail-closed host-access guarantee. The normal mount query does not establish successful protection registration.

Root protection applies to the mounted root path. It is not a universal data-flow control and does not prevent a sandboxed application from using other channels that its sandbox policy permits.

## Confidential-box protection

[ConfidentialBox](../Content/ConfidentialBox.md) is an independent runtime setting. It restricts unsandboxed host processes from obtaining handles to sandboxed processes and threads, subject to documented operational exceptions. `DenyHostAccess` supplies per-program allow or deny rules for the same protection path.

The New Box Wizard's **Black Box** option combines encrypted backing storage with `ConfidentialBox=y` while retaining the selected base box type. Enabling **Encrypt sandbox content** on an existing sandbox does not, by itself, enable every confidential-box or image-protection setting.

[ProtectHostImages](../Content/ProtectHostImages.md) is another independent feature. It restricts sandboxed processes whose executable comes from the host from loading executable images from the sandbox. It does not encrypt storage or control host process handles.

## SandMan configuration

Configure encrypted storage under:

**Sandbox Options > File Options > File Options**

The relevant controls are:

- **Encrypt sandbox content** — stores the box root in an encrypted disk image.
- **Set Password** or **Change Password** — creates or updates the image password.
- **Force protection on mount** — constrains SandMan's mount dialog to request root protection. It must not be relied on to force automatic unmount for every mount; the current manual path can leave the disabled auto-lock option off.

When mounting an image, SandMan also offers:

- **Protect Box Root from access by unsandboxed processes**.
- **Lock the box when all processes stop.**

For access to selected host files from inside the sandbox, configure the normal resource-access rules, such as [OpenFilePath](../Content/OpenFilePath.md), as appropriate. Those rules deliberately permit the specified access and should be reviewed as part of the box's data-flow policy.

## Security boundary

Encrypted storage, root protection, and confidential-process protection address different paths. Together they reduce several forms of offline and runtime host access, but they do not establish that data cannot leave a running sandbox. If a sandboxed application is allowed to use a network connection, an open host path, IPC, the clipboard, or another permitted channel, these settings do not block that channel merely because the box is encrypted or confidential.

## Version history

Encrypted sandbox support and `UseFileImage` were introduced in Sandboxie Plus 1.11.0 / Classic 5.66.0. Confidential process protection predates encrypted images; `ConfidentialBox` and `DenyHostAccess` were introduced in Sandboxie Plus 1.3.3 / Classic 5.58.3.

## Related pages

- [Use File Image](../Content/UseFileImage.md)
- [Force Protection On Mount](../Content/ForceProtectionOnMount.md)
- [Black Box](black-box.md)
- [Confidential Box](../Content/ConfidentialBox.md)
- [Protect Admin Only](../Content/ProtectAdminOnly.md)
- [Protect Host Images](../Content/ProtectHostImages.md)
- [Box Preset Comparison](box-preset-comparison.md)
