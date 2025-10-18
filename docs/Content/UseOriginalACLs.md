# Use Original ACLs

_UseOriginalACLs_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.0 / 5.70.0. This setting preserves the original Access Control Lists (ACLs) on files and folders when they are copied or created within the sandbox, rather than applying Sandboxie's default security descriptor. When enabled, files maintain their original security permissions while adding the current user to the ACL with full access rights.

## Usage

```ini
[DefaultBox]

UseOriginalACLs=y
```

## Technical Details

When `UseOriginalACLs=y` is set, Sandboxie modifies its file operation behavior in several key areas:

1. **File Creation**: Instead of using the standard `Secure_NormalSD` security descriptor, the system duplicates the security descriptor from the original file location and adds the current user with full access rights[^1].

2. **Directory Creation**: When creating directories, the system queries the security descriptor of the source directory and applies it to the sandbox copy while ensuring the current user has access[^2].

3. **File Copying**: During file copy operations, both regular files and reparse points (symbolic links, junction points) preserve their original security descriptors[^3].

## Security Implications

- **Enhanced Compatibility**: Applications that rely on specific ACL configurations will function correctly within the sandbox
- **MSI Installer Support**: Particularly beneficial for MSI installers that require specific ACL permissions (hence the UI note about MSIServer exemptions)
- **User Access Guarantee**: The current user is always added to the ACL with `GENERIC_ALL` permissions, ensuring sandbox functionality is maintained[^4]

## Implementation Notes

The setting is controlled by the global variable `Secure_CopyACLs` which is initialized during DLL startup[^5]. When active, the system:

- Queries source file security descriptors using `DACL_SECURITY_INFORMATION | SACL_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION`.
- Duplicates the security descriptor to self-relative format if necessary.
- Adds an Access Control Entry (ACE) for the current user with inheritance flags `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE`.

## Related Settings

- [MsiInstallerExemptions](MsiInstallerExemptions.md) - Often used together for MSI installer compatibility

[^1]: File creation logic in `file.c`: When `Secure_CopyACLs` is true, `File_DuplicateSecurityDescriptor` duplicates the original security descriptor and `File_AddCurrentUserToSD` adds the current user with full permissions.

[^2]: Directory creation in `file.c`: The system opens the source directory with `FILE_READ_ATTRIBUTES`, queries its security descriptor, and applies it to the new directory after adding current user access.

[^3]: File copy operations in `file_copy.c`: Both regular file copying and reparse point copying preserve original ACLs by querying the source security descriptor with `NtQuerySecurityObject`.

[^4]: ACL modification in `file.c`: `RtlAddAccessAllowedAceEx` adds the current user with `GENERIC_ALL` permissions and inheritance flags `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE`.

[^5]: Initialization in `secure.c`: `Secure_CopyACLs = SbieApi_QueryConfBool(NULL, L"UseOriginalACLs", FALSE)` sets the global variable during DLL initialization.