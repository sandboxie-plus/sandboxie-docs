# Protect Admin Only

_ProtectAdminOnly_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls whether Sandboxie's session leader must have administrative access to receive exceptions from protected-root and confidential-process checks.

```ini
[DefaultBox]
ProtectAdminOnly=y
```

The current runtime default is `y`. Set `ProtectAdminOnly=n` to permit the session leader through these checks without requiring administrative access.

## Encrypted-root behavior

When an encrypted box image is mounted with **Protect Box Root from access by unsandboxed processes**, the driver normally blocks unrelated host processes from opening the mounted root. The sandbox that owns the root, SbieSvc, required Windows components, and the permitted SandMan or Sandboxie Control session leader remain exceptions.

With `ProtectAdminOnly=y`, that session-leader exception is granted only when the session leader has administrative access. A non-administrative SandMan or Sandboxie Control instance is therefore blocked by the protected-root check. With `ProtectAdminOnly=n`, the session leader may receive the exception without being elevated.

This setting does not require ordinary sandboxed applications to run as administrators, and it is not a general Windows administrator policy or filesystem ACL. For encrypted-root access, it controls the session-leader exception only while root protection is active; its separate process/thread effect is described below.

## Confidential-process behavior

The same setting is consulted when [ConfidentialBox](ConfidentialBox.md) or `DenyHostAccess` would otherwise block a host process from opening a sandboxed process or thread. With `ProtectAdminOnly=y`, a non-administrative session leader is not exempt from that denial; an administrative session leader can be exempt. Other implementation-required system and Sandboxie exceptions remain separate.

## SandMan configuration

The control is under:

**Sandbox Options > Security Options > Box Protection**

Its current label is:

**When box root is protected require SandMan to run as Administrator in order to access the files**

The checkbox is selected when the setting is absent because the runtime default is enabled.

Changing the setting affects later process/thread access checks after configuration reload. If an encrypted root is already mounted, unmount and remount the box to apply the choice to its root protection.

## Version history

`ProtectAdminOnly` was introduced in Sandboxie Plus 1.16.4 / Classic 5.71.4 with a default of enabled. SandMan added the dedicated checkbox in Sandboxie Plus 1.16.8 / Classic 5.71.8.

## Related pages

- [Box Encryption](../PlusContent/BoxEncryption.md)
- [Confidential Box](ConfidentialBox.md)
