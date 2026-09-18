# Use Chrome Secure Preferences Hack

_UseChromeSecurePreferencesHack_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It enables Sandboxie's compatibility workaround for the Secure Preferences file used by Chrome and some related applications.

```ini
[DefaultBox]
UseChromeSecurePreferencesHack=y
```

The setting may be disabled globally or for a particular executable:

```ini
UseChromeSecurePreferencesHack=n
UseChromeSecurePreferencesHack=browser.exe,n
```

## Scope and default

The workaround is enabled by default only for processes that Sandboxie internally classifies as Chrome or Chromium applications. That classification can come from [`SpecialImage=chrome`](SpecialImage.md), bundled application mappings, or compatible [Electron/Chromium detection](UseElectronDetection.md). It is not limited to an exact `chrome.exe` filename.

For a qualifying process:

- when the setting is absent, the workaround is enabled;
- `UseChromeSecurePreferencesHack=n` disables it;
- `UseChromeSecurePreferencesHack=y` enables it explicitly.

The setting is inactive for unrelated process classifications. Classification alone also does not guarantee that an application uses Chrome's Secure Preferences format or benefits from this workaround.

## Compatibility behavior

The current workaround combines three behaviors for qualifying processes.

### Secure Preferences migration

When the process accesses a host file named `Secure Preferences`, Sandboxie can direct the request into its copy-on-write [file migration](FileMigrationSettings.md) path. The compatibility changes are then applied to the sandbox copy rather than intentionally overwriting the host file.

Ordinary Sandboxie file and path rules still apply. A direct or normal path rule can change or bypass the migration path used by this workaround.

### Encrypted-hash entries

While creating the sandbox copy, Sandboxie can remove JSON members whose names end in `_encrypted_hash`. This is not decryption, and it does not recover the protected values.

In the current implementation, this transformed-copy path applies to non-empty matching files smaller than 16 MiB. Larger files, or files that cannot be transformed, may use normal migration behavior instead. The workaround should not be treated as a guarantee for every future Chromium preferences format.

### Domain-member compatibility query

For a qualifying process, the workaround also makes the relevant `IsOS(OS_DOMAINMEMBER)` compatibility query report true. This affects the application's view of that query; it does not change the computer's Windows domain membership.

Sandboxie's project rationale is to influence Chrome's Secure Preferences validation behavior in combination with the migrated and adjusted sandbox copy. It does not disable Sandboxie isolation.

## Limitations

The project's documented benefit is limited to compatibility for browser settings and extensions. This workaround does not provide access to protected host data such as:

- credentials;
- cookies;
- saved passwords;
- Application-Bound Encryption secrets or keys.

Applications classified as Chrome or Chromium can differ in file formats and security policies. Behavior confirmed for Chrome should not be assumed to apply identically to Edge, Brave, every Chromium derivative, or every Electron application.

## Template interactions

The bundled `Chromium_Elevation` template explicitly sets:

```ini
UseChromeSecurePreferencesHack=n
```

That template disables this workaround where the separate Chromium elevation compatibility mechanism is used. The elevation mechanism is independent and is not enabled by this setting.

The bundled `Edge_Fix` template contains a `NormalFilePath` rule for Edge's `Secure Preferences` file. Such a direct or normal path rule can alter whether the usual sandbox migration and transformation path is reached; it does not directly disable _UseChromeSecurePreferencesHack_.

## Applying changes

The setting and application classification are established during process initialization. Restart the affected browser or application and its relevant child processes after changing the configuration.

This setting has no dedicated control in SandMan or Sandboxie Control Classic. Configure it manually in `Sandboxie.ini`, through the INI editor, or through an applicable template.

## Version history

_UseChromeSecurePreferencesHack_ was introduced publicly in Sandboxie Plus 1.18.0 / Classic 5.73.0. The current implementation retains the same overall compatibility approach.

## Related configuration

- [Special Image Classification](SpecialImage.md)
- [Use Electron Detection](UseElectronDetection.md)
- [File Migration Settings](FileMigrationSettings.md)
- [Sandboxie Ini](SandboxieIni.md)
