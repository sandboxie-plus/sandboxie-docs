# Notification Settings

Sandboxie notification settings generally control whether an SBIE message is generated when a particular event occurs. They do not change the policy that allowed or denied the operation. For example, disabling `NotifyInternetAccessDenied` suppresses its denial message; it does not grant Internet access.

Message generation is also separate from presentation. SandMan or Sandboxie Control Classic may show a generated message in a log, popup, or other interface according to their own presentation settings. Only some notification settings have dedicated user-interface controls.

The settings on this page are implemented by several Sandboxie components rather than one notification subsystem. Some are cached when a sandboxed process initializes, while others are read when the event occurs. The Boolean settings covered here do not have executable-qualified syntax.

Typical box setting:

```ini
[DefaultBox]
NotifyInternetAccessDenied=y
```

Typical global setting:

```ini
[GlobalSettings]
NotifyForceProcessEnabled=y
```

## Reference

| Setting | Default | Scope | Trigger or message | Applying changes / UI notes |
| --- | --- | --- | --- | --- |
| `AlwaysShowReminder` | `n` | Global | Support/reminder dialog scheduling; not an SBIE event message | See [Support reminder](#support-reminder). |
| `NotifyBoxProtected` | `n` | Protected box | SBIE1318 when a host process is denied access to a protected sandboxed process | Event-time; SandMan checkbox, which currently changes only this setting. |
| `NotifyDirectDiskAccess` | `n` | Box | [SBIE1313](SBIE1313.md) for certain denied attempts to open a disk device directly; not every denied disk-access request | Cached for the sandboxed process. See [Notify Direct Disk Access](NotifyDirectDiskAccess.md) for exceptions. |
| `NotifyForceProcessDisabled` | `n` | Global | [SBIE1301](SBIE1301.md) when a process that matches a force rule is not forced because forcing is temporarily disabled | Event-time; global Program Alerts checkbox. |
| `NotifyForceProcessEnabled` | `n` | Global | SBIE1321 when a process matches forcing and is assigned to a sandbox | Event-time; global Program Alerts checkbox. |
| `NotifyImageLoadDenied` | `y` | Box | SBIE1305 when [Protect Host Images](ProtectHostImages.md) blocks a boxed image or DLL from being mapped into a protected host-image process | Event-time; SandMan checkbox. |
| `NotifyInternetAccessDenied` | `y` | Box | [SBIE1307](SBIE1307.md) when Sandboxie's Internet-access policy denies a process; normally once per affected process | Cached for the process. See [Notify Internet Access Denied](NotifyInternetAccessDenied.md). |
| `NotifyMsiInstaller` | `y` | Box | SBIE2194 when an MSI installer starts without the recommended [Msi Installer Exemptions](MsiInstallerExemptions.md) behavior enabled | Evaluated during process startup. No dedicated SandMan checkbox was found. |
| `NotifyNoCopy` | `n` | Box | SBIE2113, SBIE2114, or SBIE2115 for the documented file-migration cases | Cached for the process. See [Notify No Copy](NotifyNoCopy.md). |
| `NotifyProcessAccessDenied` | `n` | Box | [SBIE2111](SBIE2111.md) for supported explicit process or thread access requests denied by Sandboxie's protection paths | Cached for the process. See [Notify Process Access Denied](NotifyProcessAccessDenied.md). |
| `NotifyRootProtected` | `n` | Global | SBIE1317 when access to a protected sandbox root by another process or box is denied | Read when the denial occurs. There is no functioning dedicated SandMan checkbox for this setting. |
| `NotifyStartRunAccessDenied` | `y` | Box | [SBIE1308](SBIE1308.md) when the box's Start/Run restriction mechanism denies the relevant operation; normally once per affected process | Cached for the process. See [Notify Start Run Access Denied](NotifyStartRunAccessDenied.md). |
| `AlertStartRunAccessDenied` | `y` | Global | [SBIE1308](SBIE1308.md) from the separate global program-alert denial path | Event-time; global Program Alerts checkbox; independent of `NotifyStartRunAccessDenied`. |

## Policy, generation, and presentation

A notification setting controls message generation only. It does not disable the underlying disk, network, process, launch, image-loading, or sandbox-protection rule. Likewise, `NotifyForceProcessDisabled` and `NotifyForceProcessEnabled` report decisions made by the force mechanism; they do not switch forcing on or off.

After a component generates an SBIE message, SandMan or Sandboxie Control Classic decides how to present it. SandMan's general popup and message-log options are under **Global Settings > General Config > Notifications**. Suppressing a popup is different from disabling generation of the source message.

The SandMan checkbox **Issue message 1318/1317 when a host process tries to access a sandboxed process/the box root** is broader than its current configuration handling: it reads and writes `NotifyBoxProtected`, which controls SBIE1318. `NotifyRootProtected` separately controls SBIE1317 and has no functioning dedicated checkbox in the current interface.

`NotifyImageLoadDenied` is similarly separate from enforcement. Turning its message off does not disable [Protect Host Images](ProtectHostImages.md), and the message is specific to image mapping denied by that protection rather than every failed DLL load.

`NotifyMsiInstaller` does not report every MSI launch. It produces its warning when the installer starts without the recommended [Msi Installer Exemptions](MsiInstallerExemptions.md) behavior enabled. It is separate from other MSI or COM failure messages.

## Applying changes

Restart affected sandboxed processes after changing settings that are cached in process state:

- `NotifyDirectDiskAccess`
- `NotifyInternetAccessDenied`
- `NotifyNoCopy`
- `NotifyProcessAccessDenied`
- `NotifyStartRunAccessDenied`

The following settings are currently queried when their event occurs and can affect later events after the normal configuration update or reload, without rebuilding the affected process state:

- `NotifyBoxProtected`
- `NotifyImageLoadDenied`
- `NotifyRootProtected`
- `NotifyForceProcessDisabled`
- `NotifyForceProcessEnabled`
- `AlertStartRunAccessDenied`

Restarting the affected process tree remains the most predictable approach when several notification settings are changed together.

## Start/Run messages and confirmation

`NotifyStartRunAccessDenied` and `AlertStartRunAccessDenied` are independent settings. Both can generate SBIE1308, but they are consumed by different denial paths. Disabling either setting only suppresses its corresponding message; it does not undo the denial.

[Alert Before Start](AlertBeforeStart.md) is different. It can request confirmation before an eligible sandbox launch, and the user's answer can determine whether that launch proceeds. It is not merely a switch for suppressing an informational SBIE message.

## Support reminder

`AlwaysShowReminder` is a global setting that affects the scheduling of Sandboxie's support/reminder dialog. It defaults to `n` and does not generate an SBIE event message or participate in allow/deny policy.

## User-interface availability

SandMan exposes the following controls:

- **Sandbox Options > General Options > File Options > Disk/File access > Warn when an application opens a harddrive handle** controls `NotifyDirectDiskAccess`.
- **Sandbox Options > Network Options > Internet Access > Issue message 1307 when a program is denied internet access** controls `NotifyInternetAccessDenied`.
- **Sandbox Options > General Options > Restrictions > Other restrictions > Issue message 2111 when a process access is denied** controls `NotifyProcessAccessDenied`.
- **Sandbox Options > Program Control > Start Restrictions > Issue message 1308 when a program fails to start** controls `NotifyStartRunAccessDenied`.
- **Sandbox Options > Security Options > Box Protection > Issue message 1318/1317 when a host process tries to access a sandboxed process/the box root** controls `NotifyBoxProtected`. Despite the label, it does not save `NotifyRootProtected`.
- **Sandbox Options > Various Options > Dlls & Extensions > Image Protection > Issue message 1305 when a program tries to load a sandboxed dll** controls `NotifyImageLoadDenied`.
- **Global Settings > Program Control > Program Alerts** provides **Issue message 1301 when forced processes has been disabled**, **Issue message 1321 when a process has been forced into a sandbox**, and the global **Issue message 1308 when a program fails to start** control.

Sandboxie Control Classic provides Internet Access and Start/Run Access notification controls. No equivalent dedicated current Classic controls were found for `NotifyDirectDiskAccess`, `NotifyProcessAccessDenied`, `NotifyBoxProtected`, or `NotifyImageLoadDenied`; compatible INI settings remain available through the shared runtime. No dedicated SandMan controls were found for `NotifyRootProtected` or `NotifyMsiInstaller`.

## Version history

- The setting metadata lists `AlwaysShowReminder` as added in version 1.3.0.
- `NotifyForceProcessDisabled` was added in Sandboxie Plus 1.3.2 / Classic 5.58.2.
- The setting metadata lists `AlertStartRunAccessDenied` as added in version 1.6.0.
- The setting metadata lists `NotifyNoCopy` as added in version 1.7.0.
- The setting metadata lists `NotifyImageLoadDenied` as added in version 1.9.0.
- The setting metadata lists `NotifyBoxProtected` as added in version 1.9.4.
- `NotifyProcessAccessDenied` was added in Sandboxie Plus 1.0.18 / Classic 5.55.18.
- `NotifyMsiInstaller` was added in Sandboxie Plus 1.15.2 / Classic 5.70.2.
- `NotifyForceProcessEnabled` was added in Sandboxie Plus 1.15.3 / Classic 5.70.3.
- The setting metadata lists `NotifyRootProtected` as added in version 1.15.5.
