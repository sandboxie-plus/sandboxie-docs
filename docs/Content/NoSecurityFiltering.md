# No Security Filtering

_NoSecurityFiltering_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.0 / 5.55.0. This setting disables all remaining security filtering mechanisms in [Application Compartment](../PlusContent/compartment-mode.md) mode, providing maximum compatibility at the cost of virtually all security protections.

## Prerequisites

> [!IMPORTANT]
> `NoSecurityFiltering` only functions when **[NoSecurityIsolation](NoSecurityIsolation.md)** is also enabled. This setting has no effect in standard sandbox mode.

## Usage

```ini
[DefaultBox]

NoSecurityFiltering=y
```

## Syntax

```ini
NoSecurityFiltering=<y/n>
```

Where:

- `y` disables all security filtering (only effective in Application Compartment mode).
- `n` (default) maintains standard filtering mechanisms.

## Interaction with Individual Filter Settings

`NoSecurityFiltering` serves as a master override that enables the individual filter disable settings:

- **[DisableFileFilter](DisableFileFilter.md)**: Disabled file filtering (same effect as `NoSecurityFiltering` for files).
- **[DisableKeyFilter](DisableKeyFilter.md)**: Disabled registry filtering (same effect as `NoSecurityFiltering` for registry).
- **[DisableObjectFilter](DisableObjectFilter.md)**: Disabled object filtering (same effect as `NoSecurityFiltering` for objects).

When `NoSecurityFiltering=y` is set, all three individual disable settings are automatically activated[^1][^2][^3].

## UI Integration

In Sandboxie Plus, this setting appears as:

- **Checkbox**: "Disable Security Filtering (not recommended)"[^1].
- **Location**: Sandbox Options > Security Options > Sandbox Isolation.
- **Availability**: Only enabled when "Disable Security Isolation" is checked[^2].

## Use Cases

This extreme configuration might be justified for:

- **Legacy Software**: Applications with severe compatibility issues.
- **Development Tools**: Build systems requiring unrestricted system access.
- **System Utilities**: Administrative tools that must access host resources.
- **Testing Scenarios**: When you need to verify application behavior without any restrictions.

## Debugging and Development

`NoSecurityFiltering` can be useful for:

- **Diagnosing Compatibility Issues**: Determining if filtering mechanisms cause application problems.
- **Development Testing**: Running development tools that require unrestricted access.
- **Legacy Application Support**: Supporting applications that cannot function with any filtering.

## Related Settings

### Alternative Granular Controls

Instead of disabling all filtering, consider these individual controls:

- **[DisableFileFilter](DisableFileFilter.md)**: Disables only file system filtering.
- **[DisableKeyFilter](DisableKeyFilter.md)**: Disables only registry filtering.
- **[DisableObjectFilter](DisableObjectFilter.md)**: Disables only object filtering.

[^1]: UI label in `OptionsWindow.ui`: The checkbox text "Disable Security Filtering (not recommended)" clearly indicates the security implications and discourages casual use of this setting.

[^2]: UI dependency in `OptionsAdvanced.cpp`: The code `ui.chkNoSecurityFiltering->setEnabled(ui.chkNoSecurityIsolation->isChecked());` ensures that NoSecurityFiltering can only be enabled when NoSecurityIsolation is also active, enforcing the Application Compartment mode prerequisite.
