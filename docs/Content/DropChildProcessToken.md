# Drop Child Process Token

_DropChildProcessToken_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.6 / 5.70.6. This setting forces child processes of specified applications to run without modified security tokens, bypassing Sandboxie's normal restricted token mechanism. It's primarily designed as a debugging tool for troubleshooting "green box" (Application Compartment) compatibility issues where applications fail to start or function properly due to token restrictions.

## Usage

```ini
[DefaultBox]

DropChildProcessToken=chrome.exe,y
DropChildProcessToken=firefox.exe,y
DropChildProcessToken=acroread.exe,y
```

## Syntax

```ini
DropChildProcessToken=<executable>,y
```

Where:

- `<executable>` is the name of the application executable file (case-insensitive).
- The value must be `y` to enable the setting.

## Technical Details

When `DropChildProcessToken` is enabled, Sandboxie modifies its process creation behavior during child process initialization:

1. **Token Nullification**: During `CreateProcessInternalW`, the system checks if the target application matches any configured `DropChildProcessToken` entries and sets the process token to `NULL`[^1].

2. **Automatic Application**: The setting automatically applies to specific application types - Adobe Acrobat Reader and plugin containers receive this treatment by default through hardcoded image type detection[^2].

3. **Green Box Compatibility**: This mechanism helps applications that struggle with Sandboxie's restricted security tokens to function in compartment mode, where compatibility is prioritized over strict isolation[^3].

## Default Behavior

Sandboxie automatically applies token dropping to certain application categories without explicit configuration:

- **Adobe Acrobat Reader**: All versions automatically have child process tokens dropped to prevent privilege escalation.
- **Plugin Containers**: Applications classified as `DLL_IMAGE_PLUGIN_CONTAINER` through [SpecialImage](SpecialImage.md) automatically receive this treatment.
- **Flash Player Sandbox**: Historical support for Adobe Flash Player sandbox architecture (commented out in current versions).

**Usage Scenarios**

- **Green Box Debugging**: Troubleshooting Application Compartment boxes where applications fail to start due to token restrictions.
- **Legacy Application Support**: Enabling older applications that don't work well with modern security token restrictions.
- **Plugin Compatibility**: Ensuring browser plugins and helper processes can function without token-related conflicts.
- **Development Testing**: Testing application behavior without Sandboxie's token-based security isolation.

**Security Implications**

- **Reduced Security**: Child processes run with the same token as their parent, potentially reducing isolation effectiveness.
- **Privilege Management**: Removes Sandboxie's normal privilege restrictions, allowing processes to inherit full parent privileges.
- **Compatibility Trade-off**: Improves application compatibility at the cost of some security isolation.
- **Debugging Context**: Primarily intended for troubleshooting rather than production use.

**Green Box Integration**

This setting is particularly relevant for Green Box (Application Compartment) configurations:

- **Compartment Mode**: Green boxes use `NoSecurityIsolation=y` to disable token-based security while maintaining file/registry virtualization.
- **Token Conflicts**: Some applications still experience issues even in compartment mode, requiring complete token dropping.
- **Compatibility Priority**: Green boxes prioritize compatibility over security, making this setting a natural fit for problematic applications.

## Implementation Notes

The token dropping mechanism:

- Operates during the `Proc_CreateProcessInternalW` function in the DLL injection layer.
- Uses `Config_GetSettingsForImageName_bool` to query per-application settings with a default value of `FALSE`[^4].
- Integrates with the image type classification system to automatically handle known problematic application types.
- Sets `hToken = NULL` to bypass normal token creation and restriction processes[^5].
- Affects the `CreateProcessInternalW` call chain where restricted tokens would normally be applied.

## Related Compatibility Settings

- **OriginalToken**: When enabled, bypasses most token-related modifications including `DropChildProcessToken`.
- **DeprecatedTokenHacks**: Re-enables older token-based workarounds that were disabled in compartment mode.
- **NoSecurityIsolation**: The core Green Box setting that disables token-based security isolation.
- **FakeAppContainerToken**: Controls AppContainer token simulation for specific applications.

## Usage Examples

- **Browser Child Process Issues**:
  ```ini
  DropChildProcessToken=chrome.exe,y
  DropChildProcessToken=msedge.exe,y
  ```

- **Plugin Container Problems**:
  ```ini
  DropChildProcessToken=plugin-container.exe,y
  DropChildProcessToken=flashplayer.exe,y
  ```

- **Custom Application Debugging**:
  ```ini
  DropChildProcessToken=myapp.exe,y
  ```

## Troubleshooting Green Boxes

When applications fail in Green Box mode:

1. Enable `DropChildProcessToken` for the problematic executable.
2. Test if the application starts and functions correctly.
3. If successful, the issue was token-related and the setting can remain enabled.
4. If unsuccessful, investigate other compatibility settings or file/registry access issues.

## Related Settings

- [SpecialImage](SpecialImage.md) - Automatically applies token dropping to plugin containers and Adobe Reader.
- [NoSecurityIsolation](NoSecurityIsolation.md) - Core Green Box setting for Application Compartment mode.

Related Sandboxie Plus setting: Available in advanced debugging options (not exposed in standard UI).

[^1]: Token nullification in `proc.c`: The function `Proc_CreateProcessInternalW` checks `Config_GetSettingsForImageName_bool(L"DropChildProcessToken", FALSE)` and sets `hToken = NULL` when the condition is met, bypassing the normal restricted token creation process.

[^2]: Automatic application in `proc.c`: The condition `Dll_ImageType == DLL_IMAGE_ACROBAT_READER || Dll_ImageType == DLL_IMAGE_PLUGIN_CONTAINER` automatically applies token dropping to Adobe Reader and plugin containers regardless of explicit configuration.

[^3]: Green box compatibility mechanism: This setting addresses the fundamental tension between Sandboxie's security model and application compatibility by allowing selective bypassing of token restrictions while maintaining file system and registry virtualization.

[^4]: Configuration query in `proc.c`: The system uses `Config_GetSettingsForImageName_bool(L"DropChildProcessToken", FALSE)` to retrieve per-application settings, with the `FALSE` default ensuring the feature is only active when explicitly enabled.

[^5]: Token bypass implementation in `proc.c`: Setting `hToken = NULL` in the `CreateProcessInternalW` function effectively disables the entire restricted token creation pipeline, allowing child processes to inherit their parent's full security context.