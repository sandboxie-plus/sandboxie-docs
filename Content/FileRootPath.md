# File Root Path

The _FileRootPath_ setting in [Sandboxie Ini](SandboxieIni.md) is crucial for defining the root folder in your system for a specific sandbox. This setting can be specified globally or within a sandbox section, providing flexibility.

To configure this setting, you can use the following example:

```ini
[DefaultBox]
FileRootPath=C:\Sandbox\MySandbox
```

Additionally, you can employ substitution variables in the path for dynamic configurations:

- `%Personal%`: User's Documents folder
- `%SBIEHOME%`: Root of the Sandboxie installation
- `%SANDBOX%`: Name of the sandbox
- `%USER%`: User name
- `%SID%`: User security ID (SID)
- `%SESSION%`: Terminal Services session number

If _FileRootPath_ is not specified, the default value is generated using the _deprecated_ [BoxRootFolder](BoxRootFolder.md) setting:

- `BoxRootFolder\Sandbox\%SANDBOX%`

If _BoxRootFolder_ is also absent, the fallback is:

- `C:\Sandbox\%USER%\%SANDBOX%`
