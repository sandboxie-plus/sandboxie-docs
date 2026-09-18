# Notify Internet Access Denied

_NotifyInternetAccessDenied_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It defaults to `y`.

```ini
[DefaultBox]
NotifyInternetAccessDenied=y
```

When Sandboxie's Internet-access policy denies a sandboxed process, this setting controls generation of [SBIE1307](SBIE1307.md). The message is normally emitted once per affected process. Disabling the message does not grant Internet access or otherwise change network policy.

In Sandboxie Plus, open **Sandbox Options > Network Options > Internet Access** and use **Issue message 1307 when a program is denied internet access**. Sandboxie Control Classic exposes the corresponding option under [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access).

The value is cached in the sandboxed process state. Restart affected sandboxed processes after changing it for predictable behavior.

This message switch is separate from [Prompt For Internet Access](PromptForInternetAccess.md), which can ask whether to grant a runtime exemption. See [Notification Settings](NotificationSettings.md) for the broader message model.
