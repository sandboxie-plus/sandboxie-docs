# Lock Box To User

_LockBoxToUser_ is a setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.0 / 5.70.0. It controls whether Sandboxie restricts sandbox folder access to only the user who created the sandbox.

## Usage

```ini
[GlobalSettings]

LockBoxToUser=y
```

By default (when `LockBoxToUser` is not specified or set to `n`), Sandboxie creates sandbox folders with ACLs[^1] that allow access to all authenticated users on the system. This means any logged-in user can potentially access files stored in sandbox folders created by other users.

When `LockBoxToUser=y` is specified, Sandboxie creates sandbox folders with more restrictive ACLs that only allow access to:

- The user who created the sandbox.
- The SYSTEM account[^2] .
- Administrators group[^3].

This setting enhances security and privacy in multi-user environments by preventing unauthorized access to sandbox contents.

## Security Considerations

This setting was introduced to address a security vulnerability ([CVE-2024-49360](https://github.com/sandboxie-plus/Sandboxie/security/advisories/GHSA-4chj-3c28-gvmp)) where sandbox files were accessible to all users on a system.

> [!IMPORTANT]
> For this setting to be effective, ensure that your sandbox root folder path contains the `%USER%` macro so that each user gets a dedicated sandbox folder. The default path `\??\\%SystemDrive%\\Sandbox\\%USER%\\%SANDBOX%` includes this macro and is recommended for multi-user systems.

## Implementation Details

When `LockBoxToUser=y` is enabled, Sandboxie modifies the security descriptor creation process[^4] to use a more restrictive set of SIDs:

- **System Logon SID** (`S-1-5-18`): Allows SYSTEM account access.
- **Administrators SID** (`S-1-5-32-544`): Allows local administrators access.
- **User SID**: Allows the creating user access.

When disabled, the standard behavior grants access to:

- **Authenticated Users SID** (`S-1-5-11`): Allows all authenticated users access.
- **User SID**: Allows the creating user access.

[^1]: Access Control Lists (ACLs) are Windows security structures that define which users and groups can access specific resources and what permissions they have. They are part of the Windows security model that controls access to files, folders, registry keys, and other objects.

[^2]: The SYSTEM account (SID `S-1-5-18`) is a built-in Windows account with the highest privileges on the local computer. Sandboxie runs core components under this account and needs access to sandbox folders for proper operation.

[^3]: The Administrators group (SID `S-1-5-32-544`) contains user accounts that have administrative privileges on the computer. Members of this group can access sandbox folders for system maintenance and troubleshooting purposes.

[^4]: The security descriptor creation is handled in the `Secure_InitSecurityDescriptors()` function in `secure.c`, which queries the `LockBoxToUser` configuration setting and creates different ACL structures based on its value. When enabled, it creates a 512-byte ACL with restricted SIDs instead of the default 256-byte ACL with broader access permissions.