# Special Image Classification

_SpecialImage_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.5.3a / 5.45.2. This setting allows you to classify specific executable files as belonging to predefined application categories. Sandboxie uses this classification to apply specialized handling, optimizations, and security measures tailored to each application type. The setting maps application executables to internal image types that trigger category-specific behaviors throughout the sandboxing process.

## Usage

```ini
[DefaultBox]

SpecialImage=chrome,chrome.exe
SpecialImage=firefox,firefox.exe
SpecialImage=mail,outlook.exe
```

## Syntax

```ini
SpecialImage=<category>,<executable>
```

Where:
- `<category>` is one of the predefined application types
- `<executable>` is the name of the application executable file (case-insensitive)

## Technical Details

When `SpecialImage` is configured, Sandboxie performs application classification during DLL initialization:

1. **Image Type Detection**: During process startup, the system queries all `SpecialImage` configurations and matches the current executable against defined mappings[^1].

2. **Internal Classification**: Matched applications are assigned internal image types (such as `DLL_IMAGE_GOOGLE_CHROME` or `DLL_IMAGE_MOZILLA_FIREFOX`) that determine specialized behavior[^2].

3. **Behavior Customization**: The assigned image type influences various aspects including GUI handling, process restrictions, file access patterns, and security token management[^3].

## Supported Categories

- **chrome**: Chromium-based browsers and Electron applications
- **firefox**: Mozilla Firefox and related browsers  
- **thunderbird**: Mozilla Thunderbird email client
- **browser**: Other web browsers not based on Chrome or Firefox
- **mail**: Email clients other than Thunderbird
- **plugin**: Browser plugin containers and helper processes

## Default Configuration

Sandboxie includes extensive default mappings in the `Template_SpecialImages` template:

```ini
# Chromium-based browsers
SpecialImage=chrome,chrome.exe
SpecialImage=chrome,msedge.exe  
SpecialImage=chrome,brave.exe
SpecialImage=chrome,vivaldi.exe
SpecialImage=chrome,opera.exe

# Firefox family
SpecialImage=firefox,firefox.exe
SpecialImage=firefox,waterfox.exe
SpecialImage=firefox,librewolf.exe

# Email clients
SpecialImage=mail,winmail.exe
SpecialImage=mail,foxmail.exe
SpecialImage=mail,mailbird.exe

# Electron applications
SpecialImage=chrome,slack.exe
SpecialImage=chrome,spotify.exe
SpecialImage=chrome,steam.exe
```

## Category-Specific Behaviors

- **Chrome Applications**: Receive specialized sandbox handling, custom command line flags via [CustomChromiumFlags](CustomChromiumFlags.md), restricted token management for child processes, and optimized GUI window station handling[^4].

- **Firefox Applications**: Get tailored file access permissions, specialized D3D11 handling on specific Windows versions, sandbox process token modifications, and customized GUI enumeration behavior[^5].

- **Email Clients**: Receive appropriate file system access permissions and specialized handling for mail database operations.

- **Plugin Containers**: Have their process tokens dropped to prevent privilege escalation and receive specialized restricted token handling[^6].

**Security Implications**

- **Privilege Management**: Applications classified as plugin containers or certain browser types have their security tokens automatically restricted or dropped entirely
- **Child Process Handling**: Browser applications receive specialized handling for their sandbox child processes, preventing token inheritance issues
- **File System Access**: Each category receives tailored file system access permissions appropriate to their function
- **GUI Isolation**: Browser and mail applications get enhanced GUI isolation through specialized window station handling

## Implementation Notes

The image type classification system:

- Queries configuration during DLL initialization using `SbieApi_QueryConfAsIs` with indexed access to handle multiple mappings[^7]
- Performs case-insensitive string matching between the current executable name and configured mappings
- Falls back to automatic detection for well-known applications if no explicit mapping exists
- Stores the determined image type globally for use throughout the sandboxing process
- Influences numerous subsystems including process creation, GUI handling, file access, and security token management

## Usage Examples

- **Electron Application Support**:
  ```
  SpecialImage=chrome,discord.exe
  SpecialImage=chrome,vscode.exe
  ```

- **Alternative Browser Classification**:
  ```
  SpecialImage=chrome,thorium.exe
  SpecialImage=firefox,librewolf.exe
  ```

- **Custom Mail Client Support**:
  ```
  SpecialImage=mail,myclient.exe
  ```

## Related Settings

- [CustomChromiumFlags](CustomChromiumFlags.md) - Automatically applies to applications classified as `chrome`
- [DropChildProcessToken](DropChildProcessToken.md) - Affects behavior of plugin containers and certain browser types

Related Sandboxie Plus setting: Not directly exposed in UI (uses template-defined defaults automatically)

[^1]: Image type detection in `dllmain.c`: The function `Dll_GetImageType` iterates through all `SpecialImage` configurations using indexed queries, parsing the comma-separated category and executable pairs to find matches against the current process executable name.

[^2]: Internal classification mapping in `dllmain.c`: String comparisons map category names to internal constants: "chrome" maps to `DLL_IMAGE_GOOGLE_CHROME`, "firefox" to `DLL_IMAGE_MOZILLA_FIREFOX`, "thunderbird" to `DLL_IMAGE_MOZILLA_THUNDERBIRD`, "browser" to `DLL_IMAGE_OTHER_WEB_BROWSER`, "mail" to `DLL_IMAGE_OTHER_MAIL_CLIENT`, and "plugin" to `DLL_IMAGE_PLUGIN_CONTAINER`.

[^3]: Behavior customization throughout codebase: The assigned image type influences multiple subsystems including GUI window enumeration in `guienum.c`, process creation and token handling in `proc.c`, file access permissions in `file.c`, and specialized browser handling in `kernel.c`.

[^4]: Chrome-specific handling in `kernel.c`: Applications classified as `DLL_IMAGE_GOOGLE_CHROME` receive automatic injection of custom command line flags through the `CustomChromiumFlags` mechanism, with special handling to avoid flag duplication in child processes containing the "--type=" parameter.

[^5]: Firefox-specific optimizations in `guienum.c` and `proc.c`: Firefox applications receive specialized D3D11 graphics handling on Windows 10+, custom sandbox process token management for contentproc children, and tailored GUI window station behavior for better compatibility.

[^6]: Plugin container restrictions in `proc.c`: Applications classified as `DLL_IMAGE_PLUGIN_CONTAINER` automatically have their security tokens dropped entirely during process creation to prevent privilege escalation, along with Adobe Reader and other sandboxed plugin systems.

[^7]: Configuration query mechanism in `dllmain.c`: The system uses `SbieApi_QueryConfAsIs(NULL, L"SpecialImage", index, buf, 90 * sizeof(WCHAR))` with incrementing index values to retrieve all SpecialImage entries, parsing each comma-separated value pair until no more entries exist.