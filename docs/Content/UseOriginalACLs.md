# Use Original ACLs

_UseOriginalACLs_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.0 / 5.70.0. It changes security-descriptor handling for selected sandboxed file and directory creation and migration paths. Depending on the operation, Sandboxie can reuse security attributes supplied by the application or attempt to obtain security information from an existing source object.

The option is intended for compatibility with applications that depend on particular filesystem security attributes. When a suitable descriptor is available, Sandboxie attempts to add an allow Access Control Entry (ACE) for the process user. This does not guarantee that the final descriptor or effective access matches the original.

## Usage

```ini
[DefaultBox]

UseOriginalACLs=y
```

The runtime fallback is `n`: when no effective value is configured, the option is disabled. The sandboxed process's effective configuration can include direct box settings, applicable enabled templates, and `GlobalSettings` fallback. A direct box value can override an inherited enabling value:

```ini
[DefaultBox]

UseOriginalACLs=n
```

## SandMan UI

In **Sandbox Options > Security Options > Security Hardening > File ACLs**, the checkbox is **Use original Access Control Entries for boxed Files and Folders (for MSIServer enable exemptions)**.

The checkbox reads the direct box setting, not necessarily an effective value inherited from a template or `GlobalSettings`. Checking it normally writes `UseOriginalACLs=y`; unchecking removes ordinary direct values rather than writing `n`, so an inherited `y` can remain active.

A manually configured direct `UseOriginalACLs=n` can override inheritance, but a later settings save with the checkbox unchecked can remove that direct value. When using inherited configuration, distinguish the checkbox's direct setting from the effective runtime value.

## Technical Details

The enabled option does not select one universal descriptor-copying mechanism:

1. **New files and explicit new directories**: The ordinary sandbox-copy creation path duplicates the descriptor supplied through the application's creation request, then attempts the process-user ACE adjustment. It does not automatically query a corresponding host file or directory. If no descriptor is supplied, or duplication produces no descriptor, this enabled branch passes `NULL` rather than substituting `Secure_NormalSD`; native Windows default and inheritance processing can apply. With the option disabled, the examined branch selects `Secure_NormalSD`. Open paths, devices, and special cases can follow different handling[^1].

2. **Intermediate directories**: While constructing the sandbox copy path, Sandboxie attempts to open the corresponding source directories and query their security information. After a successful query, it attempts the process-user ACE adjustment and supplies the resulting descriptor to the destination operation. These branches can use `Secure_NormalSD` if the source cannot be opened or no usable queried descriptor is obtained. This fallback is specific to intermediate-directory creation, not every ACL-handling path[^2].

3. **Migrated files and directories**: Existing source objects use a source security query rather than the independent new-object descriptor path. The queried descriptor is adjusted when possible and supplied during destination creation. File contents and security handling are separate decisions: a migration policy can produce an empty copy, and directory migration through this helper is not a recursive copy of all children. An enabled security-query failure can abort the migration helper instead of falling back to `Secure_NormalSD`; the outer file-operation wrapper can apply additional retry behavior, so this does not establish one final application-visible error[^3].

4. **Reparse points**: A separate migration path handles reparse data and security information in separate operations. Its security query can use a reopened true-path handle, so copying the reparse data does not guarantee preservation of the link object's own permissions. Complete descriptor preservation and identical handling of every symbolic-link, junction, or other reparse type are not guaranteed[^3].

The examined source-object queries request DACL, SACL, and group information, but not the original owner. SACL retrieval is conditional: the security-query hook can retry without SACL information after selected access-denied failures, but not for every failure or path. Application-supplied descriptors follow a different path and can contain owner information. Supplying a descriptor also does not guarantee identical persisted permissions, because Windows security-descriptor assignment and inheritance rules still apply[^1][^2][^3].

## Security Implications

- **Compatibility**: The option may help applications that depend on particular filesystem ACLs or security descriptors, but does not guarantee successful creation or access.
- **MSI Installer Support**: The UI recommends considering [Msi Installer Exemptions](MsiInstallerExemptions.md) for MSIServer compatibility. The settings have independent consumers; neither is a functional prerequisite for the other, and neither guarantees that every installer will work.
- **Process-user access**: Sandboxie attempts to append an allow ACE requesting `GENERIC_ALL`. Existing deny entries are not deliberately removed. Effective access can still depend on those entries, access-token restrictions, integrity policy, privileges, and Windows object-security and inheritance rules[^4].
- **Isolation boundaries**: This option changes selected filesystem security descriptors. It does not replace Sandboxie's isolation mechanisms and should not be treated as an isolation-hardening guarantee.

## Implementation Notes

`Secure_Init` reads the effective setting into `Secure_CopyACLs`, process-local SbieDll state, during initialization. It is not a live global toggle and is not reevaluated for every filesystem operation[^5].

- `Secure_NormalSD` is Sandboxie's constructed normal descriptor, not a descriptor queried from the source object.
- `File_DuplicateSecurityDescriptor` validates and duplicates a supplied descriptor, converting it to self-relative format when necessary; duplication itself does not add ACEs[^1].
- `File_CreatePath`, also reached through `File_CreateBoxedPath`, attempts source-directory queries in both of its directory-creation loops. `File_MigrateFile` and `File_MigrateJunction` have their separate migration contracts[^2][^3].
- Those source queries request `DACL_SECURITY_INFORMATION | SACL_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION`; `OWNER_SECURITY_INFORMATION` is not included[^2][^3].
- `File_AddCurrentUserToSD` attempts to append an allow ACE for Sandboxie's recorded process-user SID with `GENERIC_ALL` and flags `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE`. It requires a usable DACL and SID, can fail, and its examined callers do not check the return status. The helper copies existing ACEs when possible, without explicit canonical reordering or duplicate-ACE suppression. Neither successful adjustment nor exact persisted ACE ordering is guaranteed[^4].

Saving and reloading configuration does not refresh this cached value in already initialized sandboxed processes. Restart affected sandboxed processes after changing the effective setting; this setting does not inherently require a Windows reboot or Sandboxie service restart[^5].

Changing the option does not retroactively rewrite existing sandbox files or directories, change previously copied descriptors, or automatically remigrate content. Restarting processes does not repair historical ACLs.

## Related Settings

- [MsiInstallerExemptions](MsiInstallerExemptions.md) - Separate service-token compatibility guidance for MSI installers.

[^1]: Ordinary creation in [file.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file.c): `File_NtCreateFileImpl` uses `ObjectAttributes->SecurityDescriptor`, supplied by the caller. `File_DuplicateSecurityDescriptor` duplicates that descriptor rather than querying a filesystem path.

[^2]: Intermediate directories in [file.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file.c): both `File_CreatePath` loops attempt source-directory security queries and select `Secure_NormalSD` when no descriptor remains. The query uses `Secure_NtQuerySecurityObject` in [secure.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/secure.c), which can retry selected queries without SACL information.

[^3]: Migration in [file_copy.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file_copy.c): `File_MigrateFile` handles files and directories; `File_MigrateJunction` separately handles reparse data. Both query selected source security information when enabled, omit owner information, and can return a security-query failure rather than substitute the normal descriptor.

[^4]: ACL adjustment in [file.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file.c): `File_AddCurrentUserToSD` attempts the allow-ACE addition; its status is ignored by the examined creation and migration callers. An allow entry does not guarantee [effective Windows access](https://learn.microsoft.com/en-us/windows/win32/secauthz/how-dacls-control-access-to-an-object), and [creation-time descriptor processing](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors-for-new-objects) can affect the final ACL.

[^5]: Initialization in [secure.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/secure.c): `Secure_Init` initializes `Secure_CopyACLs` through `SbieApi_QueryConfBool(NULL, L"UseOriginalACLs", FALSE)`. The configuration API resolves this NULL section through the sandboxed process's box context; the cached flag is process-local.
