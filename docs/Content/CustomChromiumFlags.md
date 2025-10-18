# Custom Chromium Flags

_CustomChromiumFlags_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.14.2 / 5.69.2. This setting allows you to pass additional command line flags to Chromium-based browsers when they are launched within the sandbox. Sandboxie automatically injects these flags into the browser's startup command line, enabling fine-tuned control over browser behavior for enhanced compatibility and functionality within the sandboxed environment.

## Usage

```ini
[DefaultBox]

CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
```

## Syntax

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC [<flag 1> <flag 2> ...]
```

## Technical Details

When `CustomChromiumFlags` is configured, Sandboxie modifies the command line of applications identified as Chromium-based browsers during process initialization:

1. **Browser Detection**: The setting applies only to applications classified as Chrome through the [`SpecialImage`](SpecialImage.md) configuration or automatic detection[^1].

2. **Command Line Injection**: During kernel initialization, Sandboxie intercepts the process parameters and reconstructs the command line by inserting the custom flags[^7] between the executable path and existing arguments[^2].

3. **Child Process Filtering**: The flags are only added to main browser processes, not to child processes that contain the `--type=` parameter, preventing duplication and potential conflicts[^3].

## Default Configuration

Sandboxie includes a default value to ensure browser compatibility:

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC
```

This default flag disables the Print Compositor LPAC (Low Privilege App Container) feature which can cause compatibility issues in sandboxed environments[^4].

## Usage Examples

- **Basic GPU Acceleration Disable**:
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
  ```

- **Multiple Performance Flags**:
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --no-sandbox --disable-web-security
  ```

- **Debugging Options**:
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --enable-logging --log-level=0
  ```

## Security Implications

- **Browser Compatibility**: The default `PrintCompositorLPAC` flag prevents printing-related crashes and ensures stable browser operation within sandboxes
- **Flag Validation**: Users should carefully validate custom flags as some may compromise sandbox security or browser stability
- **Automatic Application**: The setting automatically applies to all applications defined as Chrome browsers, whether configured manually or detected automatically

## Implementation Notes

The setting is processed during DLL initialization when Sandboxie detects a Chromium-based browser. The system:

- Queries the configuration using `SbieApi_QueryConfAsIs` with the key `CustomChromiumFlags`[^5]
- Allocates additional memory for the expanded command line to accommodate the custom flags
- Reconstructs the command line by copying the executable path, inserting the custom flags, and appending remaining arguments[^6]
- Hooks the `GetCommandLineW` and `GetCommandLineA` functions to return the modified command line to the application

## Browser Support

This setting works with all Chromium-based browsers, including:
- Google Chrome
- Microsoft Edge (Chromium)
- Brave Browser
- Opera
- Vivaldi
- Any other browser built on the Chromium engine

## Related Settings

- [SpecialImage](SpecialImage.md) - Used to classify applications as Chromium browsers

Related Sandboxie Plus setting: Not directly exposed in UI (uses default value automatically)

[^1]: Browser detection in `dllmain.c`: Applications are classified as `DLL_IMAGE_GOOGLE_CHROME` through the `SpecialImage` configuration system, which maps browser executables to the Chrome image type for specialized handling.

[^2]: Command line reconstruction in `kernel.c`: The system calls `SbieDll_FindArgumentEnd` to locate the boundary between the executable path and arguments, then allocates expanded memory and reconstructs the command line with injected flags.

[^3]: Child process filtering in `kernel.c`: The condition `!wcsstr(ProcessParms->CommandLine.Buffer, L" --type=")` ensures that only main browser processes receive the custom flags, excluding renderer and utility processes.

[^4]: Default configuration in `Templates.ini`: The default `--disable-features=PrintCompositorLPAC` flag prevents Low Privilege App Container printing issues that can cause browser instability in sandboxed environments.

[^5]: Configuration query in `kernel.c`: `SbieApi_QueryConfAsIs(NULL, L"CustomChromiumFlags", 0, CustomChromiumFlags, ARRAYSIZE(CustomChromiumFlags))` retrieves the setting value during kernel initialization.

[^6]: Command line modification in `kernel.c`: The system copies the original executable path, appends the custom flags with proper spacing, and concatenates the remaining arguments to create the modified command line.

[^7]: List of Chromium Command Line Switches - `https://peter.sh/experiments/chromium-command-line-switches/`