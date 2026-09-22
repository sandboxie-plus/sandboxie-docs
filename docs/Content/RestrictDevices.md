# Restrict Devices

*RestrictDevices* reduces access from sandboxed processes to arbitrary driver and device endpoints under the NT `\Device` namespace. It uses Sandboxie's file/path filtering rules: a broad device-path restriction is combined with more-specific built-in compatibility exceptions. It is not a universal hardware blocker or a network firewall.

## Configuration

The setting is disabled by default. To enable it for a sandbox, add:

```ini
[DefaultBox]
RestrictDevices=y
```

The setting is evaluated for the sandbox as a whole, including applicable configuration inheritance. It does not have an executable-qualified form. Restart affected sandboxed processes after changing it.

[Security Hardened Mode](../PlusContent/security-mode.md) (`UseSecurityMode=y`) enables the same device-restriction behavior even if `RestrictDevices` is absent or explicitly set to `n`. It also enables other security features; selecting that mode does not require a separate `RestrictDevices=y` entry.

## Device-path policy

The current built-in policy, held in the internal `[TemplateSModPaths]` section of `Templates.ini`, broadly closes `\Device\*` with `ClosedFilePath` and includes more-specific `NormalFilePath` exceptions. These include Windows compatibility endpoints such as `\Device\CNG` and `\Device\NamedPipe\*`. The NT `\Device` namespace also contains objects such as named pipes that are not physical hardware. The shipped exception list may change between releases.

The restriction is a Sandboxie path policy. It does not change Windows device ACLs, uninstall devices, disable host drivers, or guarantee that every operation under `\Device` is blocked. It reduces the attack surface exposed to sandboxed applications where host drivers provide powerful device-control interfaces; it does not prevent every vulnerable-driver exploit.

Device restriction also enables [Rule Specificity](../PlusContent/RuleSpecificity.md), even if `UseRuleSpecificity=n` is configured. This lets a sufficiently specific exception take precedence over the broad device-path closure.

Ordinary drive and volume paths receive separate treatment so that enabling the restriction does not simply make normal filesystem access unusable. Outside Privacy Mode, the built-in drive patterns receive normal-path treatment. With [Privacy Mode](../PlusContent/privacy-mode.md), device restriction remains active, but those drive patterns receive Privacy Mode's `WriteFilePath` treatment instead. This is not permission for unrestricted raw-disk access.

## Allowing a specific endpoint

If an application needs a device endpoint that the broad rule closes, use the narrowest suitable [Normal File Path](NormalFilePath.md) exception after identifying its actual NT path. For example, `VendorDevice` below is only a placeholder:

```ini
[DefaultBox]
RestrictDevices=y
NormalFilePath=\Device\VendorDevice*
```

For a matching endpoint, `NormalFilePath` restores Sandboxie's normal path handling: reads can use the real path while writes remain subject to normal sandbox copy/virtualization behavior where that applies. A non-filesystem driver endpoint may not behave like an ordinary file. By contrast, [Open File Path](OpenFilePath.md) requests direct access to the real host path; it is not the standard compatibility exception for this setting. Windows permissions and other Sandboxie controls still apply.

> [!WARNING]
> Add only the exception needed for compatibility. Broad `NormalFilePath` rules covering large portions of the `\Device` namespace can substantially weaken the protection when they are more specific than the built-in device closure. Prefer the narrowest endpoint-specific rule that resolves the compatibility issue.

When troubleshooting, keep `RestrictDevices=y`, use Sandboxie's Trace Log or Resource Access Monitor where available to identify a denied `\Device\...` path, add a narrow `NormalFilePath` rule, and test again. Not every denial has a dedicated SBIE message. The outcome for a particular peripheral also depends on its NT endpoint, Windows permissions, device-control operations, and other Sandboxie rules.

## Interaction with other settings

- [Block Network Files](BlockNetworkFiles.md): when it is disabled, Sandboxie adds normal-path exceptions for its network redirector and MUP paths. When it is enabled, those particular exceptions are not added. `RestrictDevices` does not replace network access rules or Windows Filtering Platform enforcement.
- [Disable File Filter](DisableFileFilter.md): device restriction depends on Sandboxie's file/path filtering layer. Disabling that layer for a process undermines enforcement of this device-path policy.
- [Application Compartment](NoSecurityIsolation.md): `NoSecurityIsolation=y` alone does not turn off device restriction. In an Application Compartment, however, [No Security Filtering](NoSecurityFiltering.md) disables the file-filter layer used to enforce it.
- [Open Dev CM API](OpenDevCMApi.md): the built-in device policy has a normal-path exception for the `\Device\DeviceApi*` family. `OpenDevCMApi` separately controls selected Configuration Manager operations through its CMApi endpoint; it is not the same restriction.
- [Block Register Device Notification](BlockRegisterDeviceNotification.md) and [USB Sandboxing](../PlusContent/USBSandboxing.md) address separate notification and USB forced-execution behaviors. `RestrictDevices` does not enable either one.

Existing device handles are not retroactively stripped of rights by this path policy. The setting affects relevant later path/open evaluations. Path-rule lists can be refreshed for a running process, but a refresh does not recalculate that process's stored `RestrictDevices` state. Restart the affected process tree for a consistent test after changing the setting itself; a Windows reboot or normal driver/service restart is not required for newly started processes.

## SandMan interface and certificate

In SandMan, open **Sandbox Options > Security Options > Security Hardening** and select **Restrict driver/device access to only approved ones**. It is unchecked by default in a normal sandbox. The **Enable all security enhancements (make security hardened box)** control shows it as checked and disables the individual checkbox because `UseSecurityMode=y` already enables the behavior. The Rule Specificity checkbox is likewise shown checked and disabled while device restriction is selected; that display does not imply a separate `UseRuleSpecificity=y` entry is saved.

*RestrictDevices* requires an eligible supporter certificate with Sandboxie's security-enhancement capability. Without it, the current runtime logs a feature-availability message and schedules an ordinary affected process for termination after an approximately five-minute evaluation period; it does not universally refuse startup immediately.

## Version history

- Sandboxie Plus 1.0.7 / Classic 5.55.7 introduced the older `DeviceSecurity` template.
- Sandboxie Plus 1.3.0 / Classic 5.58.0 replaced it with the `RestrictDevices=y` setting and introduced the current Security Hardened mode relationship.
- Sandboxie Plus 1.7.1 / Classic 5.62.1 fixed an interaction with `BlockNetworkFiles=y`.
- Sandboxie Plus 1.8.0 / Classic 5.63.0 moved built-in access rules into template sections. The current device rules are in the internal `[TemplateSModPaths]` section, not the deprecated `Template_DeviceSecurity` template.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
- [Security Hardened Mode](../PlusContent/security-mode.md)
- [Rule Specificity](../PlusContent/RuleSpecificity.md)
- [Normal File Path](NormalFilePath.md)
- [Block Network Files](BlockNetworkFiles.md)
