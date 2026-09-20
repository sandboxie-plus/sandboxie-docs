# Confidential Box

_ConfidentialBox_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It enables additional protection for the processes and threads running in a sandbox.

```ini
[DefaultBox]
ConfidentialBox=y
```

The setting is disabled by default and requires a currently applicable Support Certificate.

## What it protects

With `ConfidentialBox=y`, the driver checks access rights requested by unsandboxed host processes when creating or duplicating handles to sandboxed processes or threads. This includes read-only and query access, not only rights that could modify or control the target.

This protection is scoped to process and thread handles. It does not encrypt files, protect the mounted box root, or automatically restrict network, clipboard, GUI, IPC, and other permitted data-transfer paths. Use [Box Encryption](../PlusContent/BoxEncryption.md) when encrypted backing storage is required.

Sandboxie retains operational exceptions for components and Windows processes needed to manage or run the sandbox. These include SbieSvc and Start, selected core or protected Windows processes, the process that is starting a target during its initialization, and an eligible SandMan or Sandboxie Control session leader. [ProtectAdminOnly](ProtectAdminOnly.md) determines whether that session-leader exception requires administrative access.

## DenyHostAccess

`DenyHostAccess` supplies program-specific rules for the same process/thread protection path. It can be used independently of `ConfidentialBox`.

```ini
[DefaultBox]
DenyHostAccess=monitor.exe,y
DenyHostAccess=audiodg.exe,n
```

The general syntax is:

```ini
DenyHostAccess=[host-program-or-group,]y|n
```

- `y` denies the matching unsandboxed host program.
- `n` allows the matching program through this particular protection check.
- With no program prefix, the value supplies the box-wide default. `DenyHostAccess=y` is therefore equivalent to a default deny rule.
- Program selectors use Sandboxie's [program-name matching](ProgramNamePrefix.md), including wildcards, and can refer to configured process groups.

Without `ConfidentialBox`, `DenyHostAccess` is evaluated when a host process requests process or thread rights beyond the read/query subset that Sandboxie normally permits. A matching deny rule rejects that handle request, while read-only access remains available.

With `ConfidentialBox`, the same check also covers read-only and query requests, and the default becomes deny for host programs. An explicit `DenyHostAccess=program.exe,n` entry can create a compatibility exception. The built-in **Less Confidential Box** template currently uses such an exception for `audiodg.exe`.

The operational exceptions described above still apply. `DenyHostAccess` is not a general filesystem rule and does not block the named executable from every form of interaction with the sandbox.

## Related settings

- [Box Encryption](../PlusContent/BoxEncryption.md) protects the sandbox's backing storage and can add mounted-root protection. It is independent of `ConfidentialBox`.
- [ProtectAdminOnly](ProtectAdminOnly.md) controls the session-leader exception for protected processes and for an encrypted root mounted with root protection.
- [ProtectHostImages](ProtectHostImages.md) restricts executable images loaded by certain sandboxed processes. It is a separate protection path.

## SandMan configuration

The controls are under:

**Sandbox Options > Security Options > Box Protection**

- **Protect processes within this box from host processes** writes `ConfidentialBox=y` when selected.
- **Allow useful Windows processes access to protected processes** enables the **Less Confidential Box** compatibility template.
- The host-process list and its **Allow Process** and **Deny Process** actions write `DenyHostAccess` entries.
- **When box root is protected require SandMan to run as Administrator in order to access the files** controls `ProtectAdminOnly`.

The UI's host-process editor accepts program names. More advanced program-group or wildcard rules can be configured manually.

## Applying changes

`ConfidentialBox` is recorded when each sandboxed process is initialized, so restart the affected sandboxed process tree after changing it. `DenyHostAccess` and the process-access part of `ProtectAdminOnly` are consulted during host access checks after configuration reload.

## Version history

`ConfidentialBox` and `DenyHostAccess` were introduced in Sandboxie Plus 1.3.3 / Classic 5.58.3. Encrypted sandbox images were added later, in Sandboxie Plus 1.11.0 / Classic 5.66.0.

## Related pages

- [Black Box](../PlusContent/black-box.md)
- [Box Encryption](../PlusContent/BoxEncryption.md)
- [Protect Admin Only](ProtectAdminOnly.md)
- [Protect Host Images](ProtectHostImages.md)
