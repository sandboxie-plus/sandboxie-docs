# Use Non-Rude HWND Hack

_UseNonRudeHwndHack_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.16.0 / 5.71.0 This setting enables compatibility hack for the NonRudeHWND property to improve fullscreen support in sandboxed applications.

Usage:

```ini
[DefaultBox]

UseNonRudeHwndHack=y
```

## Purpose

The NonRudeHWND property is a Windows window property that can be set by applications to inform the system about their fullscreen behavior and interaction with the taskbar. Some applications, particularly games and media players, set this property to ensure proper fullscreen display without unwanted taskbar interference.

When sandboxed applications attempt to set the NonRudeHWND property via `SetProp()`, Sandboxie's security model normally blocks or filters these property modifications to maintain isolation. However, this can break fullscreen functionality for applications that rely on this property.

## Technical Details

This setting controls the `Gui_NonRudeHWND_Hack` variable in Sandboxie's GUI property handling code[^1]. When enabled, Sandboxie intercepts calls to `SetPropW()` and `SetPropA()` functions and specifically allows the NonRudeHWND property to be set successfully, returning `TRUE` without actually performing the operation[^2].

The hack works by:

1. Intercepting `SetProp` calls with the property name "NonRudeHWND"[^3]
2. When this specific property is detected, returning success immediately[^4]
3. Allowing the application to believe the property was set correctly
4. This enables proper fullscreen behavior without compromising sandbox security

## Default Behavior

By default, this setting is:
- **Enabled** (`y`) when **not** running in app compartment mode
- **Disabled** (`n`) when running in app compartment mode

The logic is: `!Dll_CompartmentMode`[^5] - meaning it's enabled unless compartment mode is active.

## Important Notes

- This setting only affects how Sandboxie handles the NonRudeHWND property - it doesn't modify Windows' actual taskbar behavior
- The hack maintains sandbox security while allowing applications to function correctly in fullscreen mode

## Related Issues

This setting was introduced to address fullscreen compatibility issues, particularly referenced as GitHub issue [#4761](https://github.com/sandboxie-plus/Sandboxie/issues/4761)[^6].

[^1]: **Source**: guiprop.c: `static BOOLEAN Gui_NonRudeHWND_Hack = FALSE;`

[^2]: **Source**: guiprop.c: The `Gui_SetPropW()` and `Gui_SetPropA()` functions check for NonRudeHWND property and return `TRUE` immediately when the hack is enabled.

[^3]: **Source**: guiprop.c: `if (_wcsicmp(lpString, L"NonRudeHWND") == 0)` and line 537: `if (strcmp(lpString, "NonRudeHWND") == 0)`

[^4]: **Source**: guiprop.c: `return TRUE;` - The function returns success without actually setting the property.

[^5]: **Source**: guiprop.c: `Gui_NonRudeHWND_Hack = SbieApi_QueryConfBool(NULL, L"UseNonRudeHwndHack", !Dll_CompartmentMode);`
