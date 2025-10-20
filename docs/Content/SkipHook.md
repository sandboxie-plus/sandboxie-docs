# Skip Hook

`SkipHook` is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) used to prevent Sandboxie from installing specific hooks for particular modules or hook identifiers. It is consulted by callers that use the `Dll_SkipHook` helper.

Use this setting for module- or hook-name-level exclusions where a comma-separated list of identifiers is more convenient than a per-function list.

## Syntax

```ini
[DefaultBox]

; Skip hooks for specific module/hook identifiers (comma-separated list)
SkipHook=[<program>,]<entry1>,<entry2>,...
```

Notes:

- Entries are comma-separated tokens. Each token may optionally be prefixed with a program/image name followed by a comma (for example: `PotPlayer64.exe,cocreate`) to scope the token to a particular program. When a program prefix is present the remaining token(s) apply for that program only.
- Each token (the part after any optional program prefix) is compared to the requested hook name using a case-insensitive prefix comparison.[^1]
- Not every hook-install path necessarily consults `Dll_SkipHook`, so `SkipHook` may not prevent every single hook attempt.

## Usage

Typically used in templates to avoid hooking for particular applications or hook identifiers.

Examples:

```ini
[DefaultBox]

SkipHook=DragonSaga.exe,enumwin,findwin
SkipHook=PotPlayer64.exe,cocreate
```

## Behavior

- When called, `Dll_SkipHook` loads the configured `SkipHook` string for the current image/template and scans comma-separated tokens. If a token matches the start of the requested hook name (case-insensitive), the helper returns true and callers may skip installing that hook.
- Because this check is not universally used at every hook install point, some hooks may still be installed even if listed in `SkipHook`.

## GUI

`SkipHook` is an advanced setting and is typically edited by hand in the INI. Template files shipped with Sandboxie may include example `SkipHook` entries.

## Related Settings

- [FuncSkipHook](FuncSkipHook.md) — function-level setting to skip hooking specific API functions.

## Footnotes

[^1]: `Dll_SkipHook` initializes an internal buffer with `SbieDll_GetSettingsForName(..., L"SkipHook", ...)` and then scans comma-separated tokens. Matching is performed using a case-insensitive prefix comparison (`_wcsnicmp`).
