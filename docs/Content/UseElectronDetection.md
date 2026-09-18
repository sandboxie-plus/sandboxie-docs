# Use Electron Detection

_UseElectronDetection_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.17.4. It enables an early heuristic that can classify matching Chromium-style applications as Chrome for Sandboxie compatibility handling.

```ini
[DefaultBox]
UseElectronDetection=y
```

The setting is enabled by default. Set it to _n_ to disable the early file-layout heuristic:

```ini
[DefaultBox]
UseElectronDetection=n
```

## Detection behavior

The heuristic is evaluated during early process initialization. It does not parse Electron metadata and does not directly detect WebView2. Instead, it checks for a Chromium-style file layout near the application's executable.

The current implementation checks the executable directory and its `app` and `resources` subdirectories for characteristic packaging files, including:

- `chrome_100_percent.pak`
- `chrome_200_percent.pak`
- `resources.pak`
- `chrome_elf.dll`

A match to any one candidate is currently sufficient. These filenames explain the heuristic's behavior, but they should not be treated as a permanent application-detection specification.

Explicit [SpecialImage](SpecialImage.md) configuration and built-in image classifications are evaluated before this heuristic. Automatic detection is used only when the process has not already received another classification; it does not overwrite an explicit classification.

When a process matches, Sandboxie uses its existing Chrome-oriented process classification for that process. This classification can influence Chromium-related compatibility handling, such as hook selection, command-line handling, desktop or window-station compatibility, token handling, and the [Use Chrome Secure Preferences Hack](UseChromeSecurePreferencesHack.md). It does not disable sandbox isolation or grant broad host access.

## Detection limitations

This is a file-layout heuristic, not exact Electron identification. It can both miss Electron applications and match other Chromium-based packages.

False positives are possible because the characteristic files are not exclusive to Electron. Applications built with CEF, NW.js, WebView2, or other Chromium-based components may use similar layouts, but no particular product is guaranteed to match.

False negatives are possible when:

- The application uses different packaging.
- Expected files have been renamed.
- The files are stored outside the checked directories.
- Relevant Chromium components appear only later at runtime.

Disabling _UseElectronDetection_ disables only this early file-layout check. Sandboxie's independent `DynamicImageDetection` mechanism may still classify a process later if Chromium-related modules are loaded.

Classification is performed separately for each process. Child processes run their own classification logic rather than simply inheriting the parent process's in-memory classification.

## Applying changes

The setting is read during early process initialization. Changing it does not reclassify applications that are already running. Restart the affected application and its relevant child processes after changing the setting. SandMan itself does not need to be restarted.

## Sandboxie Plus interface

The setting is available at:

**Sandbox Options > Various Options > Compatibility**

The checkbox is labeled **Use heuristics to identify Electron/Chromium based processes**. It is checked by default and has no dedicated tooltip. Clearing it writes a disabled override; the normal checked state relies on the enabled default behavior.

## Diagnostics

Sandboxie also has a separate command-line-based diagnostic that may report `SBIE2189` when a process appears Chromium-based but does not have Chrome classification. This diagnostic is not the same algorithm as _UseElectronDetection_, and the setting does not directly emit the message.

After user confirmation, the troubleshooter may offer to add an image-qualified `SpecialImage=chrome,<program>` entry for the affected executable.

## Version history

_UseElectronDetection_ was introduced in Sandboxie Plus 1.17.4 and is enabled by default. In configuration metadata it replaced the older _UseElectronWorkaround_ setting, which was removed in the same release. The older setting used a different compatibility mechanism and is not an alias for _UseElectronDetection_.

## Related configuration

- [Sandboxie Ini](SandboxieIni.md)
- [Special Image Classification](SpecialImage.md)
- [Custom Chromium Flags](CustomChromiumFlags.md)
- `DynamicImageDetection`
