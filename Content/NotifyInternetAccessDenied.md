# Notify Internet Access Denied

_NotifyInternetAccessDenied_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), typically specified as _NotifyInternetAccessDenied=y_. It signals that Sandboxie should issue message [SBIE1307](SBIE1307.md) when programs are denied access to the Internet.

### Usage:

```ini
[DefaultBox]
NotifyInternetAccessDenied=y
```

This setting is added to the [DefaultBox] section to enable notifications for Internet access denials within the sandbox.

### Related Settings:

- [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access)
- [Sandboxie Control](SandboxieControl.md) setting: [Program Settings](ProgramSettings.md#page-2)
