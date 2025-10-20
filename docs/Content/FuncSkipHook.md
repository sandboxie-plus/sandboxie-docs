# Function Skip Hook

`FuncSkipHook` is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) that tells Sandboxie not to attempt hooking particular exported API functions.

This setting is useful when a hook attempt for a particular function causes instability, incompatibility with other security products, or unwanted behavior.

## Syntax

```ini
[DefaultBox]

FuncSkipHook=FunctionNameA
FuncSkipHook=FunctionNameB
```

Notes:

- Each `FuncSkipHook` entry is compared to the start of the function name being considered for hooking; a match causes the hook to be skipped.

## Usage

Typically used in templates to avoid hooking for particular applications or hook identifiers.

Examples:

```ini
[DefaultBox]

FuncSkipHook=SomeVendor_BrokenCall
FuncSkipHook=PStoreCreateInstance
```

## Behavior

- The helper `SbieDll_FuncSkipHook` queries the configuration for `FuncSkipHook` entries. For each configured entry it performs a prefix comparison between the configured wide-character string and the ASCII function name being hooked. If the configured string is exhausted while matching the function name's initial characters, the function is considered matched and the hook is skipped.
- For efficiency, if no `FuncSkipHook` entries were found during the first query, subsequent calls skip this check altogether.

## Technical Notes

- The code reads entries using `SbieApi_QueryConfAsIs` in a loop over an index until the query fails (or returns a different error). Each returned `WCHAR` buffer is compared to the function name by advancing both pointers in parallel; the comparison stops and reports a match when the configured wide string ends while the ASCII function name still has characters.
- This comparison is effectively a case-sensitive prefix match (it compares raw characters in parallel). If you rely on case-insensitive matching, be aware that `FuncSkipHook` behaves differently than `SkipHook`.

## GUI

`FuncSkipHook` is an advanced setting and is typically edited by hand in the INI. Template files shipped with Sandboxie may include example `FuncSkipHook` entries.

## Related Settings

- [SkipHook](SkipHook.md) — module/hook-name level setting for skipping hooks by module or identifier.

## Footnotes

[^1]: Implementation is in `SbieDll_FuncSkipHook` (see `dllhook.c`). The function queries `FuncSkipHook` entries with `SbieApi_QueryConfAsIs` and compares the configured wide string with the function name character-by-character; an exhausted configured string indicates a match and triggers skipping the hook. If no entries are found, the function sets an internal flag to disable further checks for efficiency.
