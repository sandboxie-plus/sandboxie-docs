# Msi Installer Exemptions

_MsiInstallerExemptions_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.7.2 / 5.49.0.

The runtime fallback is `n`. Without an effective value enabling this setting, the sandboxed MSIServer normally uses Sandboxie's systemless, user-token compatibility path rather than a LocalSystem token. Sandboxie provides other MSI compatibility handling in that path, so this setting is not required for every MSI installer.

```ini
[DefaultBox]
MsiInstallerExemptions=y
```

`MsiInstallerExemptions=y` selects Sandboxie's SYSTEM-token service path for the sandboxed MSIServer. This relaxes the default token model and may help with an MSI package that needs this compatibility path, but can weaken isolation and does not guarantee that every installer will work. It does not run the host MSIServer outside the sandbox or grant unrestricted host SYSTEM access. It is distinct from the broader [Run Services As System](RunServicesAsSystem.md) setting.

In [Application Compartment](NoSecurityIsolation.md) or with `OriginalToken=y`, the setting can also select a SYSTEM-token source for the sandboxed RpcSs process. This additional effect is conditional; other MSI-specific compatibility workarounds are not enabled by this setting. See [Sandboxed Services](SandboxedServices.md) for the related service-token paths.

The setting does not override the MSI startup check for open COM infrastructure. If Sandboxie detects that condition, it reports SBIE2196 and terminates the MSI process regardless of `MsiInstallerExemptions`. After that check, a process classified as MSI can instead produce the SBIE2194 warning when the exemption is not enabled and [NotifyMsiInstaller](NotifyMsiInstaller.md) is enabled (its runtime fallback is `y`). SBIE2194 does not itself block the installer; `NotifyMsiInstaller=n` suppresses the warning without enabling the exemption or bypassing SBIE2196.

The MSIServer token is selected when the sandboxed service starts, and the RpcSs token when sandboxed RpcSs starts. Changing the setting does not retroactively change either token; restart affected sandboxed installer and service processes to use a coherent new configuration.

SandMan exposes the setting under **Sandbox Options > Security Options > Security Hardening** as **Allow MSIServer to run with a sandboxed system token and apply other exceptions if required**. The checkbox reads the direct box value, which may differ from an effective value inherited through a template or `GlobalSettings`. SandMan disables it while **Drop Admin Rights** is enabled; a manually configured combination remains subject to service-start authorization. Sandboxie Control Classic has no equivalent dedicated control identified; the setting can be configured in Sandboxie Ini.
