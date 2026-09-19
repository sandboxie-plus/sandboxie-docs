# Box Alias

_BoxAlias_ is a per-sandbox setting in [Sandboxie Ini](SandboxieIni.md) that assigns an alternate display name to a sandbox. It is available since version 1.14.6.

## Syntax

```ini
[MyTestBox]
BoxAlias=Development & Testing
```

Aliases can contain display text and special characters that are not valid in a real sandbox name.

## Display name and sandbox identity

An alias is presentation-only. The real sandbox name remains the INI section name and the sandbox's operational identity. Setting an alias does not rename or change:

* the `Sandboxie.ini` section;
* the sandbox file or registry root identity;
* IPC or other internal sandbox identity;
* the name used by APIs or command-line tools;
* the sandbox name referenced by forcing rules.

Different display surfaces may format names differently. SandMan commonly replaces underscores with spaces when presenting a real sandbox name, while Start.exe and lower-level consumers may show the raw name.

## BoxAliasDisplayMode

_BoxAliasDisplayMode_ is a global display setting available since version 1.18.2:

```ini
[GlobalSettings]
BoxAliasDisplayMode=0
```

| Value | Display behavior |
| --- | --- |
| `0` | Shows the alias when one is active; otherwise shows the sandbox name. |
| `1` | Shows the real sandbox name. |
| `2` | In normal, non-compact displays, shows `Alias (RealBoxName)` when a non-empty alias differs from the real name. Compact displays may show only the alias. |

The setting is consumed by several current display paths, including SandMan, Start.exe, sandboxed window titles, borders, tooltips, recovery logs, and messages. It does not guarantee identical formatting in every interface and does not change operational sandbox identifiers.

!!! note

    Current components do not all use the same fallback when _BoxAliasDisplayMode_ is absent. SandMan's main display and border paths use mode `2`, while Start.exe and sandboxed window-title handling use mode `0`. For an explicitly consistent mode across consumers, configure _BoxAliasDisplayMode_ directly.

    SandMan's Settings interface currently saves **Sandbox alias and name** by removing the explicit key instead of writing `2`. This is the current UI behavior and leaves the component-specific absent-key fallbacks in effect.

## Global interface setting

The global control is available under:

**Global Settings > Interface Config > User Interface > Interface Options**

The **Sandbox name display:** selector provides:

| Choice | Stored value |
| --- | --- |
| **Sandbox name** | `1` |
| **Sandbox alias** | `0` |
| **Sandbox alias and name** | `2`, represented by an absent key when saved through the current SandMan interface |

This selector controls global display behavior. The alias text itself remains a per-sandbox setting.

## Hiding and restoring an alias

The current SandMan **Rename Sandbox** dialog has separate controls for the real sandbox name and its alias. It can hide an alias without discarding its text by moving the value between _BoxAlias_ and _BoxAliasDisabled_:

* With an active alias, _BoxAlias_ stores the text and _BoxAliasDisabled_ is absent.
* With **Hide alias** selected, _BoxAlias_ is removed and _BoxAliasDisabled_ stores the text.
* Clearing the alias removes both settings.
* Re-enabling the saved alias restores it to the active _BoxAlias_ setting.

For example, a hidden alias may be stored as:

```ini
[MyTestBox]
BoxAliasDisabled=Development & Testing
```

_BoxAliasDisabled_ is UI persistence for a hidden alias, not another active alias. Normal display paths read _BoxAlias_; hiding an alias does not change _BoxAliasDisplayMode_.

## Version history

* _BoxAlias_ metadata lists version 1.14.6.
* _BoxAliasDisabled_ metadata lists version 1.17.2. The Sandboxie Plus 1.17.2 / Classic 5.72.2 release notes describe the reworked SandMan rename dialog and its **Hide alias** persistence.
* _BoxAliasDisplayMode_ metadata lists version 1.18.2. The Sandboxie Plus 1.18.2 / Classic 5.73.2 release notes describe its use across current display-only name surfaces.
