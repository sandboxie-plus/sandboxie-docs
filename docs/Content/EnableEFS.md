# Enable EFS

_EnableEFS_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.0 / 5.70.0. It allows sandboxed processes to access files protected by the Windows Encrypting File System (EFS).

> [!NOTE]
> This setting requires an active advanced [supporter certificate](https://sandboxie-plus.com/supporter-certificate/)[^1].

## Usage

```ini
[DefaultBox]

EnableEFS=y
```

## Enabling via Sandboxie Manager GUI

You can enable the setting from the Sandboxie Manager (also known as SandMan) for a specific sandbox (or the DefaultBox) using the following steps:

1. Open SandMan.
2. Right-click the sandbox you want to configure, and choose "Sandbox Options".
3. In the settings dialog, select the "File Options" category on the left.
4. Switch to the "File Options" tab group (top tabs) and scroll to the "Disk/File access" section.
5. Check the option labeled "Allow sandboxed processes to open files protected by EFS".
6. Click "Apply" or "OK" to save the setting.

This mirrors the `EnableEFS=y` setting in the box section of [Sandboxie.Ini](SandboxieIni.md) but is more convenient when configuring a single sandbox via the GUI.

## Overview

The Encrypting File System (EFS) is a Windows feature that provides file system-level encryption. By default, Sandboxie blocks access to EFS-encrypted files and folders from within sandboxed processes to maintain security isolation. The `EnableEFS` setting allows you to override this restriction when needed.

## How It Works

When `EnableEFS` is enabled:

1. **EFS Detection**: Sandboxie detects when a sandboxed process attempts to access an EFS-encrypted file or folder[^2]
2. **Certificate Verification**: The system verifies that a valid advanced supporter certificate with encryption features is present[^3]
3. **Proxy Access**: Instead of blocking the access, Sandboxie uses a proxy mechanism to handle the file operation outside the sandbox[^4]
4. **Handle Duplication**: The file handle is created in the UserServer service and then duplicated back into the sandboxed process[^5]

## Security Considerations

- **Reduced Isolation**: Enabling EFS access reduces the security isolation of the sandbox, as it allows direct access to encrypted files that would normally be blocked
- **Path Validation**: The proxy service validates that the requested file path matches configured access rules before allowing the operation[^6]
- **Write Access Control**: Write operations to EFS files are subject to additional validation based on the sandbox's file access configuration[^7]

## Certificate Requirements

This feature requires an advanced supporter certificate that includes the encryption feature flag (`opt_enc`)[^8]. Without this certificate, attempts to use EFS will result in error message `SBIE6004`.

## Related Messages

- [SBIE2225](SBIE2225.md) - "An attempt was made to access an EFS file" - Warning logged when EFS access fails[^9]
- [SBIE6004](SBIE6004.md) - Certificate requirement error when advanced supporter certificate is not present

## Limitations

- Only works with files on hard disk volumes (paths starting with `\Device\HarddiskVolume`)[^10].
- Subject to the sandbox's file [resource access rules](ResourceAccess.md) (`OpenFilePath`, `ClosedFilePath`, etc.).

[^1]: Certificate verification is performed in `UserServer::OpenFile()` method checking for `CertInfo.active && CertInfo.opt_enc`
[^2]: EFS file detection occurs in `File_NtCreateFile12()` by checking if `(FileType & TYPE_EFS) != 0` where `TYPE_EFS` is defined as `FILE_ATTRIBUTE_ENCRYPTED`
[^3]: The certificate check validates both that a certificate is active and has the encryption option flag set: `!(CertInfo.active && CertInfo.opt_enc)`
[^4]: EFS proxy mechanism is implemented through `File_NtCreateFileProxy()` which sends requests to the UserServer service via `SbieDll_CallProxySvr()`
[^5]: Handle duplication is performed in the UserServer using `DuplicateHandle()` to transfer the file handle from the service process to the sandboxed process
[^6]: Path validation in UserServer checks that the path starts with `\Device\HarddiskVolume` and validates against file access rules using `SbieDll_MatchPathImpl()`
[^7]: Write access validation checks for write-related access flags, creation dispositions other than `FILE_OPEN`, and the `FILE_DELETE_ON_CLOSE` option
[^8]: The encryption feature flag `opt_enc` is defined in the certificate verification structure as part of Box Encryption and Box Protection features
[^9]: Error logging occurs when `File_NtCreateFileProxy()` fails with `SbieApi_Log(2225, TruePath)`
[^10]: Device path restriction implemented by checking `_wcsnicmp(path_buff, L"\\Device\\HarddiskVolume", 22) != 0` in UserServer