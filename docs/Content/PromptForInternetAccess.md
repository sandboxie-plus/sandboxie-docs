# Prompt For Internet Access

*PromptForInternetAccess* lets SandMan offer an interactive exception when a process is blocked by Sandboxie's Internet-access restrictions. The prompt itself is not the network enforcement mechanism.

Enabling this setting does not create an Internet-access restriction and does not prompt for ordinary unrestricted network activity. A blockade must already apply to the process for there to be an exception to grant.

## Configuration

```ini
PromptForInternetAccess=y
PromptForInternetAccess=n
```

This is a box-wide boolean setting. It does not accept an executable-qualified value. The default is `n`, which disables the interactive exception prompt.

The setting was introduced in Sandboxie Plus 0.5.0.

## When the prompt appears

The prompt becomes relevant after another Sandboxie policy has denied Internet or network access for the process. Current enforcement paths include Windows Filtering Platform (WFP) blocking and blocking access to Internet-related network devices.

The dialog concerns the blocked process, not an individually classified remote destination. In the WFP path, a decision may be requested when a socket is created, before a remote destination is known. It should therefore not be interpreted as a separate approval for each server, LAN address, or connection.

SandMan identifies the executable and shows its full path when asking whether the process should be allowed Internet access.

## Prompt choices

| Choice | Effect on the current process | Persistent configuration |
| --- | --- | --- |
| **Yes** | Grants a runtime Internet exception to the current process instance/PID. | None. |
| **No** | Grants no exception; the existing blockade remains effective. | None. |
| **Yes and add to allowed programs** | Grants the runtime exception. | Adds the executable to the existing `<InternetAccess>` allowed-program group. |
| **Terminate** | Terminates the process. | None. |

**Remember for this process** is initially selected for an Internet-access prompt. It is not a separate allow or deny action: it causes SandMan to reuse the selected **Yes** or **No** decision for later requests from the same running process instance. The remembered decision ends with that process and does not create a `Sandboxie.ini` rule.

Selecting **Yes** alone is also temporary. Use **Yes and add to allowed programs** when the executable should be added to the persistent Internet-access allow configuration.

## Enforcement behavior

The underlying Internet-access restriction remains responsible for enforcement while SandMan handles the exemption decision:

- with WFP-backed blocking, the driver and network policy continue to block traffic unless a runtime exception is granted;
- with the network-device blockade, the protected device-open operation remains denied unless an exception is granted.

If SandMan cannot provide a decision, no exemption is granted and the existing block remains in effect. Merely waiting for the prompt does not give the process unrestricted network access.

The prompt is an exception workflow, not a firewall or a complete network policy. See [Restrictions Settings](RestrictionsSettings.md#internet-access) for the allowed-program model and [Windows Filtering Platform](../PlusContent/WFPSupport.md) for the separate network enforcement mechanism.

[*NotifyInternetAccessDenied*](NotifyInternetAccessDenied.md) is independent: it controls notification of denied access, while *PromptForInternetAccess* can offer an exception. Enabling either setting does not automatically enable the other.

## Sandboxie Plus interface

In SandMan, open:

**Sandbox Options** > **Network Options** > **Process Restrictions**

The checkbox is labeled **Prompt user whether to allow an exemption from the blockade.** It is disabled when Internet access is set to unrestricted **Allow access** mode because no configured blockade is available to exempt.

The New Box Wizard also offers the prompt option when an Internet-access blockade is being configured.

## Runtime changes

*PromptForInternetAccess* is consulted when a blocked access attempt needs a decision. Changing the setting can therefore affect later blocked-access events without recreating the sandbox or restarting SandMan or the Sandboxie service.

An existing runtime exception or a decision remembered for the current process instance may prevent another prompt for that process. Persistent approval through **Yes and add to allowed programs** follows the normal Internet-access allowed-program configuration.

## Sandboxie Plus and Classic

The underlying network and runtime mechanisms are shared, but the current interactive prompt is provided by SandMan. Source review did not identify an equivalent current Sandboxie Control Classic handler for this request. If no compatible management interface responds, no runtime exception is granted and the existing blockade remains in effect.

## Version history

- Sandboxie Plus 0.5.0 / Classic 5.45.0-era code introduced the interactive Internet-blockade exemption mechanism.
- Sandboxie Plus 0.5.5 / Classic 5.46.4 added the option to persistently allow the program.
- Sandboxie Plus 1.14.2 added the prompt option to the New Box Wizard.

These historical counterpart versions do not imply that the current Classic interface provides the same interactive prompt as SandMan.

## Related settings

- [Restrictions Settings](RestrictionsSettings.md#internet-access) — configures the Internet-access allow/block model
- [Notify Internet Access Denied](NotifyInternetAccessDenied.md) — controls denial notifications rather than granting exceptions
- [Windows Filtering Platform](../PlusContent/WFPSupport.md) — describes Sandboxie's separate WFP enforcement
- [Sandboxie Ini](SandboxieIni.md) — explains manual sandbox configuration
