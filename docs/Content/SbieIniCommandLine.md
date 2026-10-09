# SbieIni Command Line

SbieIni.exe is a small command-line utility for inspecting and changing Sandboxie configuration. Queries read the configuration currently held by the driver. Ordinary updates edit [Sandboxie.ini](SandboxieIni.md) through the service and attempt to reload it; `/drv` is a separate advanced direct-driver update route.

## Quick start

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
SbieIni.exe set DefaultBox RecoverFolder "C:\Recovery"
```

To store the literal Sandboxie variable `%Desktop%` from a **batch file**, double the percent signs:

```batch
SbieIni.exe set DefaultBox RecoverFolder "%%Desktop%%"
```

CMD expands its own `%VAR%` expressions before SbieIni.exe receives them; the doubled-percent example above is specifically batch-file syntax.

## Overview

SbieIni.exe supports three distinct workflows:

- Querying driver-resident configuration (read-only).
- Updating persistent configuration through the service (`set`, `append`, `insert`, `delete`), followed by save and driver-reload attempts.
- Updating driver-resident configuration directly with `/drv`, without the ordinary INI save or reload.

## Invocation summary

Basic forms:

```batch
SbieIni.exe query    [/expand] [/boxes] <section> [setting]
SbieIni.exe queryex  [/expand] [/boxes] <section> [setting]

SbieIni.exe set [/passwd:********] <section> <setting> [value]
SbieIni.exe append|insert|delete [/passwd:********] <section> <setting> <value>
```

Notes:

- `queryex` is shorthand for `query /expand`.
- `/boxes` filters section listing to enabled sandboxes available to the current user, not boxes with running processes.
- `/passwd:` supplies a configuration password for ordinary updates; an empty option value opens an interactive prompt.
- Use omitted-value `set` only for ordinary persistent deletion. `append`, `insert`, and `delete` require a non-empty value.
- `/drv` is an advanced update option with different authorization, persistence, and deletion limitations; see below.

## Querying configuration (read-only)

Queries inspect the driver's resident configuration, not the physical INI file. Output can therefore differ from the file, including after driver-only changes.

Value queries exclude template-derived values, but retain fallback to matching direct values from `GlobalSettings`. For repeated settings, direct values in the requested section can be followed by direct global values. The output is neither a complete effective configuration nor necessarily limited to direct values in the named section.

How to list sections:

```batch
SbieIni.exe query *
```

This prints `GlobalSettings` explicitly and then enumerates eligible non-template-origin sections in resident configuration; it is not a sandbox-only list. To list only enabled sandboxes available to the current user:

```batch
SbieIni.exe query /boxes *
```

No running sandboxed process is required for a box to appear.

How to list settings in a section:

```batch
SbieIni.exe query DefaultBox *
```

This lists distinct setting names directly represented in that section under the template-excluding lookup. It does not enumerate global fallback names: a globally configured value may be queryable even when its setting name is absent from this list. Omitting the setting also lists setting names.

How to get the value(s) for a setting:

```batch
SbieIni.exe query DefaultBox RecoverFolder
```

How to expand variables to paths:

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
```

`queryex` and `query /expand` use Sandboxie's configuration expansion context, not merely the CLI process's environment. Expanded output then undergoes an NT-to-DOS path translation attempt; not every string becomes a DOS filesystem path. Expansion does not change template exclusion or global fallback.

For syntactically accepted queries, exit code `0` does not prove that a value was found. Empty output can mean absence, the end of enumeration, or a lower-level query, expansion, or buffer-processing failure.

## Update operations (set / append / insert / delete)

Without `/drv`, these commands edit the service's writable INI model, attempt to save Sandboxie.ini, and attempt to reload the driver's configuration. This is the normal persistent workflow, not an atomic transaction. Save or reload can fail, and the CLI does not reliably report every failure through its exit status.

These operations edit the named section, not the source definitions of inherited templates. Whether running processes observe changes depends on each setting's consumer and lifecycle.

### Set — replace existing lines of a setting (or remove them if no value supplied)

```batch
SbieIni.exe set <section> <setting> [value]
```

`set` removes the setting's existing entries and writes the replacement. Omitting the value removes the setting instead. An empty quoted token (`""`) is also treated as an omitted value by the CLI parser.

To remove an entire configuration section through the ordinary persistent route:

```batch
SbieIni.exe set BoxName * ""
```

Use this with extreme caution: it removes the section's configuration, not the sandbox's stored contents. Do not use this deletion form with `/drv`.

### Append — add a new value line after existing entries

```batch
SbieIni.exe append <section> <setting> <value>
```

The new value is added after the existing entries for that same setting. If the setting does not exist, it is added to the section. Duplicate values are permitted; this does not necessarily append to the end of the section or file.

### Insert — add a new value line before existing entries

```batch
SbieIni.exe insert <section> <setting> <value>
```

Ordinary `insert` adds the value before the existing entries for that setting. With `/drv`, `insert` currently has append semantics instead.

### Delete — remove matching value lines

```batch
SbieIni.exe delete <section> <setting> <value>
```

This removes all entries for the setting whose complete value matches the supplied value case-insensitively. It does not use wildcards. If the setting does not exist or no value matches, deletion is a no-op in the writable model.

### Password handling

For ordinary updates, `/passwd:secret` or `/passwd=secret` supplies a configuration password. `/passwd`, `/passwd:`, or `/passwd=` opens an interactive prompt. Pressing Escape cancels before issuing an update, but still returns exit code `0`; do not use interactive prompting for unattended automation.

## Advanced and automation notes

### Direct-driver updates (`/drv`)

`/drv` is not the normal persistent update route. It mutates driver-resident configuration directly, without the ordinary service-side INI edit, file save, or configuration reload.

The driver rejects sandboxed callers and accepts the registered service process or a recognized session-leader context. `/passwd` does not authorize `/drv`: the direct-driver API receives no configuration password, and generic administrator elevation alone should not be assumed sufficient.

Driver-only changes are not written to Sandboxie.ini and must not be relied on as durable configuration across reloads or driver lifecycle changes. Do not assume either that every change survives or that every change disappears on every reload.

Current limitations:

- `/drv insert` has append semantics, unlike ordinary `insert`.
- Do not use `/drv` with no-value `set` deletion forms, including `""`; use the ordinary persistent route for setting or section deletion.
- Changing resident configuration is not a universal live reload. Whether an already-running sandboxed process observes a changed setting depends on that setting's consumer and lifecycle.

### Exit codes and verification

The CLI's own handling uses these exit codes:

| Code | Meaning and limitation |
| --- | --- |
| `1` | Syntax or usage error. |
| `2` | An update reported a wrong configuration password. |
| `0` | Not proof of success: accepted queries, password-prompt cancellation, and many other update failures can return this code. |

Process-start or loading failures can occur outside this handling. Do not rely solely on `ERRORLEVEL 0` to verify an update. A normal `query` can check the driver's lookup afterward, but that readback does not independently prove disk persistence. Conversely, inspecting the physical INI does not establish the complete effective runtime configuration.

### CMD parsing and concurrent edits

- Wrap values containing spaces in double-quotes.
- In batch files, double percent signs to pass a literal Sandboxie variable, as shown in Quick start.
- `""` becomes an omitted positional value, not a distinct empty-string argument.
- After quote removal, a token beginning with `/` is treated as an option, not a positional value. Quoting alone does not make such a token usable as a setting value.
- Conflicting file locks or concurrent writers can interfere with persistence; avoid editing the INI concurrently with scripted updates.

## Examples

```batch
SbieIni.exe query * | sort > Sections.txt
SbieIni.exe query DefaultBox RecoverFolder
SbieIni.exe queryex DefaultBox RecoverFolder
SbieIni.exe append DefaultBox Template RoboForm
SbieIni.exe set DefaultBox AutoRecover n
SbieIni.exe delete DefaultBox RecoverFolder "C:\Old\Path"
```

## Implementation and references

The authoritative behavior is defined by the CLI and its active consumers. Key implementation points in the Sandboxie source repository:

- `apps/ini/cmd.c` — argument parsing helpers.
- `apps/ini/query.c` — query implementation and SBIEDLL query helpers.
- `apps/ini/update.c` — update verbs, `/passwd` prompt, `/drv` vs DLL path.
- `apps/ini/main.c` — program entry and usage handling.
- `core/dll/callsvc.c` / `core/dll/sbieapi.c` — service-update helper and driver API wrappers.
- `core/svc/sbieiniserver.cpp` — ordinary configuration edits, save, and reload handling.
- `core/drv/conf.c` — resident configuration queries and direct-driver updates.

## Forum/source note

Some usage examples and operational notes were informed by community forum discussion [archived](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947). This is historical context, not authority for current behavior.
