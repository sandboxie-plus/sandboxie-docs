# Msi Installer Exemptions

_MsiInstallerExemptions_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.7.2 / 5.49.0.

```
   .
   .
   .
   [DefaultBox]
   MsiInstallerExemptions=y
```

Use the 'MsiInstallerExemptions=y' option to allow MSIServer to run with a sandboxed system token and apply other exceptions. This option may help with installing an MSI package.

Related Sandboxie Plus setting: Sandbox Options > Security Options > Security Hardening > Allow MSIServer to run with a sandboxed system token and apply other exceptions if required
