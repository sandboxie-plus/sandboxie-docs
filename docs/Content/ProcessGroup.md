# Process Group

`ProcessGroup` defines a reusable, named set of executable-image selectors. Settings that accept a process-qualified selector can refer to the group instead of repeating each executable name, where the corresponding runtime parser supports process groups.

For example:

```ini
[DefaultBox]
ProcessGroup=<Browsers>,firefox.exe,chrome.exe
```

This definition alone does not grant or deny access, force programs into a sandbox, start or stop processes, create a Windows process group or Job Object, or otherwise apply a policy. A second setting must use `<Browsers>` as its process selector before the group affects runtime behavior.

Both Sandboxie's driver-side and SbieDll user-mode configuration matchers resolve process groups for settings that use those matchers. This does not mean that every Sandboxie setting accepts a process group; check the syntax of the setting that will reference it.

## Syntax

The general form is:

```ini
ProcessGroup=<GroupName>,program1.exe,program2.exe
```

The angle brackets are part of the group selector. Current runtime matching recognizes a group reference when the selector begins with `<`; a bare name such as `Browsers` is treated as an ordinary image selector rather than as the `ProcessGroup` named `<Browsers>`.

Group names and ordinary executable-image membership matches are case-insensitive. Use executable image names such as `firefox.exe`, rather than process IDs or full executable paths.

Some generic configuration matchers can interpret wildcard image patterns, but not every active process-group matching path does so. For configuration that must work consistently across consumers, use literal executable image names and nested group references rather than wildcard members.

Negation belongs to the process selector in the rule that uses a group, not to the `ProcessGroup` definition. Where a setting supports a negated process selector:

- `<Browsers>` matches members of the group;
- `!<Browsers>` matches processes that are not members of the group.

Do not define the group as `ProcessGroup=!<Browsers>,...`.

## Using a group in rules

This resource-access example applies the file rule to the members of `<Browsers>`:

```ini
[DefaultBox]
ProcessGroup=<Browsers>,firefox.exe,chrome.exe
OpenFilePath=<Browsers>,C:\Shared\*
```

`OpenFilePath` is one proven consumer, but it is not the only one. Built-in templates also use process groups with file, registry, IPC, and window-class rules.

In consumers that use Sandboxie's generic process-match levels, a direct executable or group match has stronger process-match priority than a negated selector, which in turn is stronger than a global or `*` selector. This is precedence between qualified rules. The order of members inside a `ProcessGroup` does not make one member take precedence over another.

## Nested groups

A process group can contain another process group:

```ini
[DefaultBox]
ProcessGroup=<Browsers>,firefox.exe,chrome.exe
ProcessGroup=<WebApps>,<Browsers>,electron-app.exe
```

`<WebApps>` can therefore match `firefox.exe`, `chrome.exe`, and `electron-app.exe`.

Nested expansion is deliberately depth-limited in the current runtime. Expansion through cyclic or excessively deep definitions is bounded rather than recursing indefinitely, but such definitions are not useful configurations and should not be relied upon. SandMan allows an existing group to be selected as a member and does not currently prevent direct or indirect cycles.

## Repeated and inherited definitions

Repeated definitions with the same group name contribute additional members:

```ini
ProcessGroup=<Browsers>,firefox.exe
ProcessGroup=<Browsers>,chrome.exe
```

The effective group matches either executable. The same runtime behavior applies when same-named definitions come from the box, `[GlobalSettings]`, or enabled templates: applicable definitions contribute members rather than one definition being selected solely by its source. Consequently:

- `[GlobalSettings]` can provide groups to sandboxes through normal global configuration lookup;
- enabled templates can contribute groups;
- a box-local definition with the same name does not remove the inherited members at runtime;
- same-named definitions from multiple enabled templates also contribute members.

The current SandMan description says that groups defined for the box overwrite groups defined in templates. That wording does not reflect the current runtime matchers, which inspect all applicable same-named definitions. Avoid reusing a group name across configuration sources when an accidental combined membership would be unclear.

## Managing groups in SandMan

Open **Sandbox Options > Program Groups**. The page provides:

- **Add Group**;
- **Add Program**;
- **Remove**;
- **Show Templates**.

**Add Group** stores the entered name in angle brackets. **Add Program** can select an existing group, displayed as **Group: GroupName**, which creates a nested group reference.

**Show Templates** displays groups from `[GlobalSettings]` and the box's enabled templates alongside local groups. Template-derived entries are read-only in this view; the page writes only the box's local `ProcessGroup` entries.

Renaming a local group in this page changes its definition name, but it is not a global refactoring operation. References to the old name in other process groups or configuration rules are not automatically rewritten. Removing a group likewise removes the selected definition without necessarily removing settings that refer to it. A dangling group selector cannot match through the removed definition, although another applicable definition with the same name may still supply members.

## UI-managed groups

Some higher-level SandMan features maintain `ProcessGroup` entries internally. Current examples include the program lists used by Internet Access and Start/Run restrictions, with groups such as `<InternetAccess>`, `<StartRunAccess>`, and `<StartRunAccessDisabled>`.

Editing or removing these entries manually can therefore change what those controls represent. These names are ordinary runtime process groups; their significance comes from the rules and SandMan features that reference them.

## ProcessGroup vs BoxGrouping

`ProcessGroup` and [`BoxGrouping`](BoxGrouping.md) serve unrelated purposes.

| Setting | Contains | Scope and effect |
| ------- | -------- | ---------------- |
| `ProcessGroup` | Executable-image selectors and nested process groups | Sandbox, global, or template configuration used by runtime rule matching; referenced as `<GroupName>` |
| `BoxGrouping` | Sandboxes and visual subgroups | Per-user SandMan hierarchy and ordering metadata; no runtime policy effect |

Putting two sandboxes in the same `BoxGrouping` branch does not share their `ProcessGroup` definitions or make processes in those sandboxes members of a common process group.

## Applying changes

Saving a `ProcessGroup` change updates the configuration, but when new membership becomes observable depends on the setting that references the group. Dynamically evaluated checks can use the updated definition on subsequent operations, while consumers that build or cache effective rules during process initialization may require the affected sandboxed processes to be restarted. A SandMan, service, or driver restart is not normally required solely to change a process group.

## Sandboxie Plus and Classic

`ProcessGroup` is a shared runtime configuration mechanism, not a Sandboxie Plus-only feature. SandMan provides the current **Program Groups** page, and Sandboxie Control Classic also contains program-group configuration and selection support. Their interfaces are not identical, but compatible INI definitions are consumed by the shared runtime.

## Version history

The current settings metadata does not record an `AddedVersion` for `ProcessGroup`, so no exact introduction version is established here. Program-group handling predates Sandboxie Plus 0.4.3 / Classic 5.43.7; that release fixed parsing in the SandMan UI rather than introducing the runtime setting. Later SandMan releases also fixed additional program-group UI issues.

## Related pages

- [Box Grouping](BoxGrouping.md) — organizes sandboxes in the SandMan interface
- [Sandboxie Ini](SandboxieIni.md) — explains Sandboxie configuration sections and editing
