# Special Image Classification

_SpecialImage_ is a [Sandboxie Ini](SandboxieIni.md) setting that selects an initial compatibility classification for a sandboxed process. The resulting image type is consulted by selected process-creation, file-handling, and GUI compatibility paths. It is not a sandbox security level, token type, or isolation mode, and assigning a category does not guarantee one uniform set of behaviors for every application in it.

## Syntax

```ini
[DefaultBox]
SpecialImage=chrome,mybrowser.exe
SpecialImage=firefox,anotherbrowser.exe
SpecialImage=mail,myclient.exe
```

The format is `SpecialImage=category,program.exe`. Supported categories are `chrome`, `firefox`, `thunderbird`, `browser`, `mail`, `plugin`, and `none`.

Sandboxie compares `program.exe` with the executable's basename exactly and without regard to case. The first matching _SpecialImage_ entry in the effective configuration wins. This dedicated format does not use the generic program-name prefix rules: wildcard executable names, ProcessGroup selectors, and negated selectors are not supported here.

Entries can be configured directly for a box or supplied by applicable templates. Sandboxie's default `SpecialImages` template provides mappings for known browser and mail applications.

Manual classification can be useful when an application needs the compatibility handling associated with a category but is not recognized by the existing mappings or automatic detection. Check for an existing mapping first, since the first matching entry wins.

## Supported categories

- `chrome` selects the Chrome/Chromium compatibility image type, also used for some Electron-based applications.
- `firefox` selects the Firefox compatibility image type.
- `thunderbird` selects the Thunderbird mail image type.
- `browser` selects the other-web-browser image type.
- `mail` selects the other-mail-client image type.
- `plugin` selects the plugin-container image type.
- `none` suppresses initial fallback classification, subject to the later detection described [below](#the-none-category).

These names identify compatibility categories, not a promise that every application assigned to a category receives identical file, GUI, or token treatment.

## Classification order

During process initialization, Sandboxie determines the initial image classification in this order:

1. The first matching _SpecialImage_ entry, if any.
2. Built-in classification of known executable names, if no entry matched.
3. An early Electron/Chromium file-layout heuristic, if the image is still unclassified and [Use Electron Detection](UseElectronDetection.md) is enabled.

_UseElectronDetection_ is enabled by default. These are fallback stages, not checks that necessarily run for every process. Classification primarily selects compatibility-specific behavior for that sandboxed process.

## How the classification is used

The image type is checked by specific compatibility paths; their other conditions and settings still matter. For example:

- Chromium classification is checked before applying configured `CustomChromiumFlags` to an eligible command line. It is also checked by the conditional Chrome Secure Preferences file-handling path and selected window-station or desktop compatibility fallbacks.
- Firefox classification is checked by selected window-station and desktop fallbacks, a process-creation compatibility case, and a file-open workaround for executable files. These are specific cases, not general permission changes for all Firefox-classified processes.
- Mail classifications can cause selected mail-program checks to consult `OpenFilePath` configuration, while Chrome, Firefox, and other-browser classifications are explicitly excluded from that mail-program path. This does not establish category-wide filesystem permissions.
- Plugin classification can affect the token argument used when creating child processes. It does not remove the current plugin process's token or make that process tokenless.

## Default mappings

The default `Template_SpecialImages` configuration provides mappings for known Chromium-family and Firefox-family browsers, other browsers, mail clients, and some Electron/Chromium-based applications. The maintained list can change between releases; the example above is illustrative, not a complete list of template mappings. A program's category is determined by its actual matching entry, not merely by its product name.

## The `none` category

```ini
[DefaultBox]
SpecialImage=none,example.exe
```

`none` suppresses the initial built-in and early Electron/Chromium fallback classification for that executable. It does not establish a permanent "never classify" state: later dynamic detection may still classify the process.

## Dynamic detection

`DynamicImageDetection` is enabled by default and is separate from the early _UseElectronDetection_ heuristic. If a process remains unclassified, Sandboxie's loader can later assign a classification when characteristic modules are loaded. This can also happen after an initial _SpecialImage=none_ match.

## Applying changes

Initial classification and the dynamic-detection setting are initialized for each sandboxed process. After changing _SpecialImage_, _UseElectronDetection_, or `DynamicImageDetection`, start a new instance of the affected application and its relevant child processes to ensure they use the new configuration. A Windows reboot or Sandboxie service restart is not normally needed.

_SpecialImage_ entries are primarily managed through templates or manual INI configuration; SandMan does not provide a dedicated checkbox for them. SandMan does provide the _UseElectronDetection_ checkbox under **Sandbox Options > Various Options > Compatibility**.

_SpecialImage_ was introduced in Sandboxie Plus 0.5.3a / Classic 5.45.2.

## Related settings

- [Use Electron Detection](UseElectronDetection.md) controls the early Electron/Chromium heuristic used when the process is still unclassified.
- [Custom Chromium Flags](CustomChromiumFlags.md) is relevant to Chromium-classified processes.
- [Drop Child Process Token](DropChildProcessToken.md) is a separate child-process token control; `SpecialImage=plugin` does not drop the current process's token.
