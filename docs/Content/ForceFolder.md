# Force Folder

_ForceFolder_ is a sandbox setting in [Sandboxie.ini](SandboxieIni.md) that automatically starts matching programs in a particular sandbox. A normal folder entry applies to programs in that folder and its subfolders. For example:

```ini
[DefaultBox]
ForceFolder=C:\Download
ForceFolder=E:\
```

The first entry forces programs started from `C:\Download` or one of its subfolders into `DefaultBox`. The second applies to programs started from drive `E:`. Folder matching is case-insensitive.

## What is matched

During normal force-rule evaluation, Sandboxie first checks the executable's directory against _ForceFolder_. If that does not select a sandbox, it checks [ForceProcess](ForceProcess.md). If neither check selects a sandbox, the effective working directory and a document argument can also be checked against _ForceFolder_. The latter checks are skipped when the process being evaluated is Sandboxie's `Start.exe` itself.

An ordinary folder entry is matched as a recursive path prefix. An entry containing `*` is instead handled as a wildcard pattern against the normalized directory path. A `?` character does not by itself switch a _ForceFolder_ entry to wildcard matching; it participates as a wildcard only when the same entry also contains `*`. Use [ForceProcess](ForceProcess.md) when selection by executable name is required.

## Shortcuts

Merely storing a shortcut in a forced folder does not force a target program located outside that folder. The target can still be forced if its executable directory, effective working directory, or document argument matches a _ForceFolder_ rule.

## Immersive applications

By default, after a normal _ForceFolder_ or _ForceProcess_ rule selects a sandbox, Sandboxie discards that selection if it identifies the resulting process as an immersive/AppContainer application. In the ordinary unsandboxed-parent case, this check does not terminate the process; the process continues without being forced into the selected sandbox by this path. Other independent launch policies can still affect the result.

The advanced global setting `AllowForceImmersive` enables these force rules for such processes:

```ini
[GlobalSettings]
AllowForceImmersive=y
```

The default is `n`. This setting is global rather than per sandbox, and SandMan does not currently provide a dedicated control for it. Enabling the setting does not guarantee compatibility with every AppContainer, UWP, or other immersive application.

## Rule order

For the executable path, a matching _ForceFolder_ rule is checked before _ForceProcess_. Working-directory and document-argument _ForceFolder_ checks occur later, after _ForceProcess_, so _ForceFolder_ does not have unconditional precedence in every case.

## User interfaces

In SandMan, open **Sandbox Options > Program Control > Force Programs** and use **Force Folder** to maintain the list. The same page also provides **Force Program**, **Force Children**, **Remove**, and **Show Templates** controls.

Sandboxie Control Classic provides the related [Sandbox Settings > Program Start > Forced Folders](ProgramStartSettings.md#forced-folders) page.

## Version history

`AllowForceImmersive` was added in Sandboxie Plus 1.16.0 / Classic 5.71.0. _ForceFolder_ predates the current version metadata and has no introduction version recorded there.

## Related pages

- [Force Process](ForceProcess.md)
- [Sandboxie Ini](SandboxieIni.md)
