# Win32k Hooks

## Overview

Sandboxie can hook selected Win32k system calls for compatibility with applications that need particular GUI or graphics-driver calls to pass through Sandboxie's mediation. The mechanism has two configuration levels: global support must be available before a box or process can use the hooks.

This is not a general GPU-acceleration switch, does not hook every Win32k system call, and does not toggle a Windows security mitigation. Experimental Win32k filter-table support is a separate internal mechanism.

## Global hook support

The global availability setting is:

```ini
[GlobalSettings]
EnableWin32kHooks=y
```

The current runtime default is enabled. The driver initializes Win32k system-call support only on Windows build 14393 or later and when `EnableWin32kHooks` is enabled. This makes the mechanism available; it does not force hooks into every sandboxed process.

Disabling the setting prevents the later per-process Win32k hook path from being installed. Current setting metadata classifies this global control as advanced and experimental.

SandMan exposes it under **Global Settings > Advanced Config > Sandboxie Config** with the label:

> Hook selected Win32k system calls to enable GPU acceleration (required for chrome, firefox and more)

The control is unavailable on Windows builds older than 14393. The UI label describes the compatibility motivation, but global enablement alone does not select every application or guarantee GPU acceleration.

## Per-process hook selection

`UseWin32kHooks` selects which sandboxed processes use the available hook path. It supports executable-qualified configuration such as:

```ini
UseWin32kHooks=program.exe,y
```

The process setting requires global `EnableWin32kHooks=y`. A value without an executable qualifier can set the behavior for the box, while a qualified entry can target a particular executable.

When no applicable `UseWin32kHooks` value is present, the current default is enabled only for processes Sandboxie classifies with its Google Chrome/Chromium image type. Current templates and application-detection logic can classify other browser or Electron processes into that type. This classification is maintained by the project and should not be treated as a fixed list of applications.

In SandMan, `UseWin32kHooks` is available through the per-process advanced option editor under **Sandbox Options > Advanced Options > Miscellaneous**. Its description notes that global Win32k hook support must be enabled first. It is not a dedicated normal checkbox.

## GPU acceleration compatibility

The primary compatibility motivation is graphics-driver interaction used by Chrome/Chromium GPU processing. Sandboxie's default Win32k hook map includes selected calls whose names match `GdiDdDDI*`.

These hooks allow the selected calls to use Sandboxie's Win32k mediation and token-handling path. This does not mean every GPU call is hooked, that every Chromium-derived application needs manual configuration, or that enabling the hooks guarantees hardware acceleration.

## Platform and process gates

Win32k hooks are installed for a process only when all relevant conditions are satisfied. Installation is skipped when, among other conditions:

- the Windows build or driver support is unavailable;
- the process does not have Sandboxie's Win32k-hookable capability;
- global `EnableWin32kHooks` is disabled;
- the process is operating in Application Compartment mode;
- the low-level system-call hook facility is disabled internally;
- `UseWin32kHooks` is disabled or does not default to enabled for that process.

These checks occur while the sandboxed process initializes its hook path. Restart affected sandboxed processes after changing the settings to ensure the new selection is used.

## Advanced and experimental controls

> [!WARNING]
> Sandboxie contains low-level Win32k hook-map controls intended for expert diagnostics and development. They can disable required mediation or force hooks that Sandboxie deliberately excludes for stability reasons. Project metadata and source comments warn that forcing additional hooks can cause system instability or BSoDs. These controls are not recommended as general compatibility settings.

Internally, `EnableWin32Hook` can add specifically named calls to the hook set, `DisableWin32Hook` can remove calls, and `IgnoreWin32HookBlacklist` bypasses the built-in stability blacklist. This page intentionally does not provide configuration recipes for them.

Experimental `UseWin32kFilterTable` support also exists internally. It is not a general-purpose Win32k hook setting: current code consults it both while loading the Windows filter service table and for processes that Windows already reports as Win32k-filtered. It does not itself enable Windows Win32k filtering on arbitrary processes and is not documented here as a supported compatibility control.

`AlwaysUseWin32kHooks` is obsolete. It was removed in version 1.0.11 and superseded by `UseWin32kHooks`; it has no current runtime consumer.

## Troubleshooting guidance

- Verify that `EnableWin32kHooks` has not been disabled globally.
- For a confirmed Win32k or GPU compatibility problem, check the effective `UseWin32kHooks` value for the affected executable.
- Prefer current templates and Sandboxie's image classification over forcing individual Win32k hook names.
- Remove custom hook-map experiments when investigating system crashes or regressions.
- Do not bypass the Win32k hook blacklist or use experimental filter-table support as routine troubleshooting steps.

Disabling Win32k hooks does not disable Sandboxie security globally, and enabling them should not be presented as an automatic security improvement. This mechanism primarily addresses compatibility for selected intercepted calls.

## Version history

| Setting or change | Version |
| --- | --- |
| `EnableWin32kHooks` metadata | AddedVersion 1.0.0 |
| Win32k hook feature described in the changelog | Sandboxie Plus 1.0.3 / Classic 5.55.3 |
| `AlwaysUseWin32kHooks` | Added in 1.0.3; removed in 1.0.11 and superseded by `UseWin32kHooks` |
| `UseWin32kHooks` metadata | AddedVersion 1.0.11 |
| Win32k hook use temporarily defaulted to all processes | Sandboxie Plus 1.16.6 / Classic 5.71.6 |
| Broad default reverted because of compatibility problems | Sandboxie Plus 1.16.7 / Classic 5.71.7 |

The metadata lists `EnableWin32kHooks` as added in 1.0.0, while the Win32k hook feature is described in the 1.0.3 / 5.55.3 release notes. The reason for this version discrepancy is not established. Current executable behavior, rather than historical default descriptions, determines the present selection rules.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
- [Special Image](SpecialImage.md)
- [Token and Syscall Internals](TokenMagic.md)
