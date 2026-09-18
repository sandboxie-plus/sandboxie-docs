# Notify Process Access Denied

_NotifyProcessAccessDenied_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.0.18 / Classic 5.55.18. It defaults to `n`.

```ini
[DefaultBox]
NotifyProcessAccessDenied=y
```

When enabled, Sandboxie issues [SBIE2111](SBIE2111.md) for supported explicit process or thread access requests denied by its process and IPC protection paths, including relevant denied `OpenProcess` and `OpenThread` requests. This does not mean that every possible process-handle failure produces SBIE2111.

The setting controls the notification only; it does not relax the underlying process-access restrictions.

In Sandboxie Plus, open **Sandbox Options > General Options > Restrictions > Other restrictions** and select **Issue message 2111 when a process access is denied**. No equivalent dedicated current Sandboxie Control Classic control was found.

The value is cached when the sandboxed process initializes. Restart affected sandboxed processes after changing it for predictable behavior.

See [Notification Settings](NotificationSettings.md) for the broader message model.
