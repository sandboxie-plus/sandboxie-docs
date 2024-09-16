# Hide Firmware Info

HideFirmwareInfo is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```
   .
   .
   .
   [DefaultBox]
   HideFirmwareInfo=y
```

Use the 'HideFirmwareInfo=y' option to return the SMBiosTable value in HKCU\System\SbieCustom as firmware information. When enabled, the sandbox entry (if exist) will be prioritized, then the one in the host system.

Related Sandboxie Plus setting: Sandbox Options > Advanced Options > Privacy > Hide Firmware Info
