# Template Architecture

A Sandboxie template is primarily a reusable collection of [Sandboxie configuration](SandboxieIni.md) entries. Selecting a template makes its ordinary settings part of the effective configuration; the selection does not permanently copy those entries into the sandbox's explicit configuration. Template presentation and discovery data are separate from the rules that Sandboxie applies at runtime.

For example:

```ini
[Template_Example]
Tmpl.Title=Example
Tmpl.Class=Misc
OpenFilePath=C:\Example\*
OpenIpcPath=\RPC Control\Example

[DefaultBox]
Template=Example
```

Here `OpenFilePath` and `OpenIpcPath` contribute configuration to `DefaultBox`. The `Tmpl.*` entries describe the template; they are not sandbox access rules.

## Official and local templates

Official templates ship in `Templates.ini` in the Sandboxie installation. Use that file as a reference for existing definitions, but put custom templates in [`Sandboxie.ini`](SandboxieIni.md) rather than editing the stock file.

Official template sections normally use `[Template_Name]`. User-created templates conventionally use `[Template_Local_Name]`, which distinguishes them in the UI and avoids collisions with future official names:

```ini
[Template_Local_ExampleSoft]
Tmpl.Title=ExampleSoft
Tmpl.Class=Local
OpenWinClass=ExampleSoft_WindowClass
OpenIpcPath=*\BaseNamedObjects*\ExampleSoft_*
```

Local templates can be enabled manually like official templates. `Template_Local_` is a naming and presentation convention, not a separate runtime inheritance mechanism. The [Applications Settings](ApplicationsSettings.md#local) page also describes the legacy local-template UI.

## Selecting templates

Enable a template for a sandbox with its name after `Template=`:

```ini
[DefaultBox]
Template=Example
```

A section can contain multiple `Template=` entries. Sandboxie processes each selected template and merges its settings into that section's effective configuration. A template can also be selected globally:

```ini
[GlobalSettings]
Template=Example
```

Global selection contributes settings to the global effective configuration. It does not make a separate permanent copy of the template definition in every sandbox section.

`TemplateReject=Name` belongs in `[GlobalSettings]`. It records compatibility-template selection state so a detected template is treated as rejected/configured instead of remaining a pending recommendation. A value in an individual sandbox section is not consulted for this purpose. It does not subtract settings from an explicitly selected `Template=Name`; normal template merging still applies to that selection.

## How templates are merged

At configuration load, Sandboxie first processes templates selected in `GlobalSettings`, then applies `[DefaultTemplates]` to the global effective configuration, and then processes templates selected by each sandbox. Ordinary settings in a selected template are merged into the destination's effective configuration. `Tmpl.*` metadata is skipped by this runtime merge.

Explicit entries and template-origin entries can coexist in the effective configuration. Sandboxie records which entries came from templates, and direct entries normally precede entries merged afterward. The effect of competing entries still depends on the subsystem that consumes them; configuration-source order is not a universal precedence rule. See [Rule Specificity](../PlusContent/RuleSpecificity.md) for resource-rule conflicts.

## Default templates

`[DefaultTemplates]` in the shipped `Templates.ini` lists built-in templates automatically merged into global effective configuration. These provide baseline settings without a user selecting them individually for a box. The current list includes `RpcPortBindings`, `SpecialImages`, `COM`, `WindowsExplorer`, `ThirdPartyIsolation`, `BlockSoftwareUpdaters`, `BlockWinRM`, `OpenWinInetCache`, `CredentialUIBroker`, and `MSI_Lite`. The shipped list can change between releases; default templates are not immutable policy.

This automatic merge differs from enabling an optional application compatibility template for a particular sandbox.

## Template variables and internal sections

`[TemplateSettings]` provides shared `%Tmpl.*%` variable definitions and related metadata infrastructure. A template can use these variables, as described in [Expandable Variables](ExpandableVariables.md#template-variables). `[TemplateSettings]` is not a compatibility template selected with `Template=TemplateSettings`; custom templates do not require copying or editing it.

Other sections with names beginning with `Template` are also not ordinary App Templates. `TemplateDefaultPaths`, `TemplateSModPaths`, `TemplatePModPaths`, and `TemplateAppCPaths` supply built-in path rules to runtime subsystems through separate loading paths. Do not enable them through the App Templates list or assume that `Template=Name` controls them.

## Template metadata

Entries beginning with `Tmpl.` describe a template or help discover when it may be useful. They are skipped when template rules are merged into runtime configuration.

| Entry | Purpose |
| --- | --- |
| `Tmpl.Title` | Display title |
| `Tmpl.Class` | UI category |
| `Tmpl.Url` | Related software or vendor URL |
| `Tmpl.Comment` | Description or comment |
| `Tmpl.Hide` | Hides a template from normal presentation |
| `Tmpl.Entry` | Specialized compatibility or known-conflict entry metadata |
| `Tmpl.Version` | Template/configuration metadata version |
| `Tmpl.Scan` | Compatibility discovery mode |
| `Tmpl.Scan*` | Evidence used to detect whether a template may apply |
| `Tmpl.ScanScript` | Scripted detection in SandMan's modern checker |

Most of these fields are used by template presentation or compatibility discovery code, not by the driver as access rules.

## Template discovery

Template discovery determines whether Sandboxie or SandMan should suggest a compatibility template. It does not itself enforce the template's sandbox rules. Those rules enter effective configuration only when the template is selected or applied through the default-template mechanism.

`Tmpl.Scan` selects one or more evidence modes:

- `i` checks for IPC objects using `OpenIpcPath` and `Tmpl.ScanIpc` evidence. An `OpenIpcPath` entry alone does not imply scanning unless `i` is selected.
- `w` checks known window classes using `OpenWinClass` and `Tmpl.ScanWinClass` evidence.
- `s` checks software-presence evidence such as `Tmpl.ScanService`, `Tmpl.ScanProduct`, `Tmpl.ScanKey`, and `Tmpl.ScanFile`. These can indicate services, installed products, registry keys, or files; `s` is not limited to services.

SandMan's modern compatibility checker evaluates `Tmpl.ScanScript` first when a scan script exists. The older C++ fallback scanner instead uses the `Tmpl.Scan` evidence fields and does not execute that script path. Automatic scanning by the modern checker skips `Local_` templates; local templates remain available for manual selection.

## Software updater blocking

The shipped `[DefaultTemplates]` list includes `Template=BlockSoftwareUpdaters`. Its `[Template_BlockSoftwareUpdaters]` section supplies maintained `SoftwareUpdater` patterns to effective configuration. This default template is already included; users do not need to select it as an optional App Template to obtain those definitions.

The maintained rules use an originating application image followed by an updater executable or path pattern:

```ini
SoftwareUpdater=starting_image.exe,updater_path\updater_image.exe

SoftwareUpdater=firefox.exe,*\mozilla firefox\updater.exe
SoftwareUpdater=msedge.exe,*\Microsoft\EdgeUpdate\MicrosoftEdgeUpdate.exe
```

`BlockSoftwareUpdaters` is a separate runtime gate, queried with a default of `y`. When the gate is enabled and a child process matches a `SoftwareUpdater` rule, Sandboxie blocks its creation with `ERROR_ACCESS_DENIED` and reports **Blocked start of an updater** to its monitor path. With `BlockSoftwareUpdaters=n`, the default template and its patterns may still be present in effective configuration, but this process-creation blocker does not enforce them.

`BlockSoftwareUpdaters` was introduced in 0.5.5, removed in 1.0.11, and reintroduced in 1.14.4. It is active in the current runtime. This mechanism covers matching updater process creations; it does not guarantee that every software update, installer, or network-based update path is blocked.

## SandMan and applying changes

In SandMan, templates are presented under **Sandbox Options > App Templates** by title and category. Enabling one for a sandbox corresponds to selecting its configuration without requiring manual `Template=` edits.

After enabling, disabling, or editing a template, restart affected sandboxed processes so settings cached during process initialization are rebuilt consistently. Different template-derived settings have different lifetimes; a template change should not be assumed to update every running process immediately. A Windows reboot, driver restart, or service restart is not normally required.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
- [Applications Settings](ApplicationsSettings.md)
- [Expandable Variables](ExpandableVariables.md)
- [Rule Specificity](../PlusContent/RuleSpecificity.md)
