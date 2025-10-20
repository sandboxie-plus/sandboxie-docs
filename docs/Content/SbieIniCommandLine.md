# SbieIni Command Line

SbieIni.exe is a small command-line utility for querying and updating the Sandboxie configuration file [Sandboxie.ini](SandboxieIni.md). This page documents common invocation forms, examples for automation, and implementation references for maintainers.

## Quick start

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
SbieIni.exe set DefaultBox RecoverFolder %Desktop%
```

## Overview

SbieIni.exe supports two primary workflows:

- Querying configuration values (read-only)
- Updating the configuration (`set`, `append`, `insert`, `delete`)

## Invocation summary

Basic forms:

```batch
SbieIni.exe query    <section> [setting]
SbieIni.exe queryex  [/expand] [/boxes] <section> [setting]

SbieIni.exe set|append|insert|delete [/passwd:********] [/drv] <section> <setting> <value>
```

Notes:

- `queryex` is shorthand for `query /expand`.
- `/boxes` lists only enabled sandboxes.
- `/passwd:` supplies a config password; if empty the utility will prompt interactively.
- `/drv` routes updates through the driver/service API; without `/drv` the DLL helper path is used.

## Querying configuration (read-only)

Purpose: inspect sections and settings.

How to list sections:

```batch
SbieIni.exe query *
```

How to list settings in a section:

```batch
SbieIni.exe query DefaultBox *
```

How to get the value(s) for a setting:

```batch
SbieIni.exe query DefaultBox RecoverFolder
```

How to expand variables (NT→DOS path translation):

```batch
SbieIni.exe queryex DefaultBox RecoverFolder
```

## Update operations (set / append / insert / delete)

Purpose: modify configuration contents.

### Set — replace existing lines of a setting (or remove them if no value supplied)

```batch
SbieIni.exe set <section> <setting> <value>
```

### Append — add a new value line after existing entries

```batch
SbieIni.exe append <section> <setting> <value>
```

### Insert — add a new value line before existing entries

Note: in some builds `insert` may behave like `append`; test if order matters.

```batch
SbieIni.exe insert <section> <setting> <value>
```

### Delete — remove a value line that exactly matches the supplied value

```batch
SbieIni.exe delete <section> <setting> <value>
```

## Advanced and automation notes

- To delete an entire box: `SbieIni.exe set BoxName * ""` (removes all lines for that section). Use with extreme caution.
- Batch files: escape percent variables as `%%VAR%%`.
- If values include spaces, wrap them in double-quotes.
- Avoid running updates while `Sandboxie.ini` is open/locked by another process.
- For driver-level updates or automation where immediate driver state is required, use `/drv` (service/driver must be available and caller needs necessary privileges).

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

The authoritative behavior lives in the `apps/ini` sources. Key implementation points:

- `apps/ini/cmd.c` — argument parsing helpers.
- `apps/ini/query.c` — query implementation and SBIEDLL query helpers.
- `apps/ini/update.c` — update verbs, `/passwd` prompt, `/drv` vs DLL path.
- `apps/ini/main.c` — program entry and usage handling.

## Forum/source note

Some usage examples and operational notes were informed by community forum discussion [archived](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947).
