# Hide Firmware Info

HideFirmwareInfo is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```ini
[DefaultBox]
HideFirmwareInfo=y
```

When enabled and `SMBiosTable` data is available, Sandboxie substitutes the bytes returned for the intercepted `RSMB` SMBIOS firmware-table `Get` query with that data. Other firmware-table providers and actions continue through the original query path. This setting does not establish coverage for every firmware API or WMI query.

## SMBIOS table data

The hook reads `SMBiosTable` from `HKCU\System\SbieCustom` through the sandboxed process's normal Registry view. `SMBiosTable` is a Registry value, not an INI setting. The hook does not explicitly search the sandbox and then the host; any visibility of host or sandboxed values follows normal Registry virtualization. The setting expects this data to be available through the effective Registry view. Missing or invalid custom data should not be treated as a documented fallback to the host SMBIOS table.

In **Sandbox Options > Advanced Options > Privacy**, the **Hide Firmware Information** checkbox controls the direct box setting. **Dump FW Tables** reads the host's `RSMB` table and saves it as a binary `SMBiosTable` value under the host user's `HKCU\System\SbieCustom`. That value can be copied into the sandboxed Registry if a box-specific table is wanted. Dumping the table does not enable `HideFirmwareInfo`.

The runtime fallback is disabled when no effective value is configured. The Boolean lookup can be qualified by the sandboxed process image and can include applicable template or global configuration; the checkbox's direct box value may therefore differ from the effective value. The Boolean is checked on intercepted queries, so an updated effective value can affect later calls if the `NtQuerySystemInformation` hook is already installed in that process. A configuration change cannot retroactively install a hook that was skipped at process initialization.
