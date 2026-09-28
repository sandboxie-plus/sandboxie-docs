# Open Clipboard

_OpenClipboard_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.7.5 / 5.49.8. It controls Sandboxie's standard clipboard data-operation hooks. The consumer fallback is `y`: if no effective value is configured, or if the effective value is `y`, this setting does not deny clipboard data operations. `OpenClipboard=n` denies hooked clipboard reads, writes, and clearing. Other Windows or Sandboxie restrictions can still affect clipboard access.

## Syntax

```ini
[DefaultBox]
OpenClipboard=n
```

This is a box-wide Boolean setting. Its effective value can also come from enabled templates or `GlobalSettings` through normal configuration lookup; it does not support a per-program selector.

## Behavior

In the standard hooked path, `OpenClipboard=n` denies `GetClipboardData`, `SetClipboardData`, and `EmptyClipboard`. The hooked `OpenClipboard` and `CloseClipboard` calls are not themselves denied by this setting. Applications should not rely on one particular Windows error code for a denied data operation.

Sandboxie's normal [Job Object](JobObjects.md) independently restricts clipboard reads. It does not apply the corresponding Job Object write restriction. When clipboard access is allowed by this setting, Sandboxie's GUI service can assist a hooked clipboard read that fails through the direct Windows path. The service checks the effective `OpenClipboard` value before returning data. These layers should not be confused with one another.

The data-operation hooks consult the setting when each operation occurs. After a configuration reload, a changed value can affect subsequent operations in already-running processes that have those hooks installed. Hook installation and Job Object participation are determined as processes start; changing related settings does not retroactively install hooks or reassign an existing process.

## Compatibility and limitations

In an ordinary [Application Compartment](NoSecurityIsolation.md), the standard `OpenClipboard` hook enforcement is not active, and the process is not assigned to Sandboxie's normal root Job Object. Clipboard access remains subject to Windows and other applicable restrictions.

With [`NoSandboxieDesktop=y`](NoSandboxieDesktop.md), the standard clipboard hooks and GUI proxy are not installed through this path, so `OpenClipboard=n` is not enforced by those hooks. Unlike Application Compartment, the normal Job Object clipboard-read restriction can remain active independently. The absent hooks do not block writes or clearing through `OpenClipboard=n`, although other restrictions may still apply.

This setting describes Sandboxie's standard clipboard handling paths; it is not a guarantee covering every Windows data-transfer API.

## SandMan interface

In Sandboxie Plus, the control is under **Sandbox Options > General Options > Restrictions** and is labeled **Block read access to the clipboard**. Checking it writes `OpenClipboard=n`; unchecking it removes the direct sandbox value. Despite the read-focused label, the standard hooks also deny clipboard writes and clearing when the effective setting is `n`.

SandMan disables this checkbox for Application Compartment. The checkbox manages the direct box value and may not show an effective value inherited from a template or `GlobalSettings`.

## Sandboxie Control Classic

The setting is handled by shared Sandboxie components in the standard path. Sandboxie Control Classic users can configure it through [Sandboxie Ini](SandboxieIni.md).
