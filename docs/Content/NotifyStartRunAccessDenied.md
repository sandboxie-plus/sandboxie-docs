# Notify Start Run Access Denied

_NotifyStartRunAccessDenied_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It defaults to `y`.

```ini
[DefaultBox]
NotifyStartRunAccessDenied=y
```

When the sandbox's Start/Run restriction mechanism denies the relevant launch or access operation, this setting controls generation of [SBIE1308](SBIE1308.md). The message is normally emitted once per affected process. Disabling it does not permit a launch or alter the underlying Start/Run policy.

In Sandboxie Plus, open **Sandbox Options > Program Control > Start Restrictions** and use **Issue message 1308 when a program fails to start**. Sandboxie Control Classic exposes the corresponding option under [Sandbox Settings > Restrictions > Start/Run Access](RestrictionsSettings.md#startrun-access).

The value is cached in the sandboxed process state. Restart affected sandboxed processes after changing it for predictable behavior.

`AlertStartRunAccessDenied` is a separate global setting used by the program-alert mechanism. The two settings are independently consumed and can both generate SBIE1308 from different denial paths; they are not aliases.

See [Notification Settings](NotificationSettings.md) for the broader message model and [Alert Before Start](AlertBeforeStart.md) for the separate pre-launch confirmation feature.
