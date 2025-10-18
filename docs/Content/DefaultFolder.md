# Default Folder

_DefaultFolder_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.12 / 5.70.12 that specifies folders to be pre-created in the sandbox during initialization when [Privacy Mode](../PlusContent/privacy-mode.md) is enabled. This setting ensures that essential system and user directories exist within the sandbox environment before programs attempt to access them, preventing potential failures.

## Usage

```ini
[DefaultBox]

DefaultFolder=%SystemRoot%
DefaultFolder=%USERPROFILE%
DefaultFolder=%Desktop%
DefaultFolder=C:\SomeSpecificPath
```

## Overview

When a sandbox operates in privacy mode (`UsePrivacyMode=y`), most locations on the system are isolated and programs may expect certain standard directories to exist. The `DefaultFolder` setting ensures these directories are pre-created within the sandbox, maintaining compatibility with applications that rely on their presence.

## How It Works

During sandbox initialization[^1], Sandboxie processes each `DefaultFolder` entry in the following manner:

1. **Environment Variable Expansion**: If the path contains environment variables (like `%SystemRoot%` or `%USERPROFILE%`), they are expanded to their actual values.
2. **Path Translation**: The DOS path is converted to its NT equivalent for internal processing.
3. **Sandbox Creation**: The corresponding directory structure is created within the sandbox hierarchy.

## Template Integration

Sandboxie includes a built-in template called `TemplateDefaultFolders`[^2] that provides a comprehensive set of standard directories commonly needed by applications. This template includes:

### System Directories

- `%SystemRoot%` (Windows directory)
- `%TEMP%` (Temporary files)
- `%ProgramFiles%` and `%ProgramFiles(x86)%`
- `%CommonProgramFiles%` and `%CommonProgramFiles(x86)%`

### User Profile Directories

- `%USERPROFILE%` (User profile root)
- `%Desktop%` (User desktop)
- `%Personal%` (Documents folder)
- `%{374DE290-123F-4565-9164-39C4925E467B}%` (Downloads folder)
- `%Favorites%` (Internet favorites)
- `%{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}%` (Links folder)
- `%My Music%`, `%My Pictures%`, `%My Video%` (Media folders)
- `%{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}%` (Saved Games)

### Public Directories

- `%PUBLIC%` and its subdirectories
- `%LOCALAPPDATA%` (Local application data)

## Use Cases

- **Privacy Mode**: Essential for proper operation when `UsePrivacyMode=y` is enabled
- **Application Compatibility**: Ensures programs that check for standard directory existence don't fail
- **Initialization Optimization**: Pre-creates directories that would otherwise be created on first access

## Limitations

- Only activated when privacy mode is enabled.
- Directory creation follows standard sandbox path rules and restrictions.
- Environment variables must be valid and expandable at initialization time.

## Examples

### Custom Application Directory

```ini
[ApplicationBox]

UsePrivacyMode=y
DefaultFolder=C:\MyApp\Data
DefaultFolder=%APPDATA%\MyApplication
```

## Related Settings

- [UsePrivacyMode](UsePrivacyMode.md) - Enables privacy mode (required for `DefaultFolder` to function)
- [NormalFilePath](NormalFilePath.md) - Controls read/write access to specific paths
- [FileRootPath](FileRootPath.md) - Specifies sandbox container location

[^1]: The folder pre-creation occurs in the `File_CreateBaseFolders()` function during process initialization when privacy mode flags are detected. This function iterates through both the template defaults and user-specified `DefaultFolder` entries. (Source: `/Sandboxie/core/dll/file_dir.c:3550`)

[^2]: The `TemplateDefaultFolders` template is defined in the `Templates.ini` file and provides a comprehensive list of standard Windows directories that applications commonly expect to exist. (Source: `/Sandboxie/install/Templates.ini`)