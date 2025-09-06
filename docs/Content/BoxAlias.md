# Box Alias

**BoxAlias** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since **v1.14.6**. It allows setting an alternate display name for a sandbox.

## Syntax

```ini
BoxAlias=DisplayName
```

## Usage

BoxAlias provides a way to set custom display names for sandboxes that contain special characters, which would otherwise be invalid for sandbox names. When BoxAlias is set, it overrides the default display behavior:

```ini
[MyTestBox]
BoxAlias=Development & Testing

[WebBox]  
BoxAlias=Secure Web Browser v2.0

[WorkSandbox]
BoxAlias=Email Client*
```

## Important Notes

- BoxAlias only affects the display name - the actual sandbox name in the INI file remains unchanged
- If BoxAlias is not set, sandbox names are displayed with underscores replaced by spaces

## User Interface

BoxAlias can be configured through the **Rename** function in **Sandboxie Plus**. When renaming a sandbox to a name containing special characters, Sandboxie Plus automatically prompts to set it as an alias instead of renaming the sandbox.