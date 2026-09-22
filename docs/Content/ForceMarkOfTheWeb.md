# Force Mark of The Web

_ForceMarkOfTheWeb_ is a global [Sandboxie Ini](SandboxieIni.md) setting that uses the presence of a Mark-of-the-Web stream when deciding whether to force a newly starting process into a sandbox. It is disabled by default. This is a process-start rule, not continuous isolation of every marked file that an application opens.

## Configuration

```ini
[GlobalSettings]
ForceMarkOfTheWeb=y
MarkOfTheWebBox=Web_Box
```

`ForceMarkOfTheWeb=y` enables the check. `MarkOfTheWebBox` names the destination sandbox; if it is absent or empty, the driver's runtime fallback is `DefaultBox`. Both settings are read from global configuration for this mechanism, not from an individual sandbox section.

## What Sandboxie checks

During an eligible process start, Sandboxie checks the executable's path. It can also check a document argument when it can identify one from the new process's command line. The document check is skipped when the process being evaluated is Sandboxie's `Start.exe` or SandMan. Sandboxie does not scan every command-line argument, and it does not check the working directory for a Mark of the Web.

For each candidate path, the driver appends `:Zone.Identifier` and tries to open that alternate data stream. A successful open counts as a match; the driver does not read the stream or check its `ZoneId`, origin, URL, referrer, contents, or reputation. If the stream cannot be opened, that candidate does not match.

## Process-start behavior and rule order

Sandboxie evaluates this rule only if earlier process-start checks have not selected a sandbox and an alert rule has not stopped the evaluation. Those earlier checks include existing sandbox paths, [Force Box Docs](ForceBoxDocs.md), [Force Folder](ForceFolder.md), and [Force Process](ForceProcess.md) or forced-child rules. Host injection is considered afterward. The Mark-of-the-Web rule does not override a sandbox already inherited from a sandboxed parent.

Opening a marked document through **File > Open** in an already-running host application does not, by itself, run this process-start check or move that application into a sandbox.

## Destination sandbox

The configured name is matched against eligible sandbox names without regard to letter case. Eligibility depends on the sandbox being enabled for the current user and session. A sandbox with [Disable Force Rules](DisableForceRules.md) enabled is excluded from the eligible list and cannot be selected as this rule's destination.

If a candidate matches but the destination cannot be selected from that list—for example, because the sandbox does not exist or is disabled—Sandboxie marks the new process for termination rather than allowing this path to continue unsandboxed. The particular application error or message is not fixed by this setting.

## SandMan interface

In Sandboxie Plus, open **Global Settings > Program Control > Force Process Options**. The controls are labeled **Force files with a Mark of The Web into a sandbox** and **Sandbox for MoTW marked files**.

When no `MarkOfTheWebBox` value is saved, SandMan initially looks for a sandbox named `Web_Box` in its selector. If it does not find one, the selector uses its first available sandbox. This UI initialization is distinct from the driver's `DefaultBox` runtime fallback when the setting is absent.

![Force Mark of The Web Settings](../Media/ForceMarkOfTheWeb.png)

## Limits

This rule does not monitor later file reads or opens, move an already-running host application into a sandbox, create or preserve a Mark of the Web, or inspect archive contents. It does not validate a file's reputation and does not replace SmartScreen or antivirus scanning. Its result depends on the relevant `Zone.Identifier` stream being openable at the time of the process-start check.

## Version history

`ForceMarkOfTheWeb` and `MarkOfTheWebBox` were introduced in Sandboxie Plus 1.16.0 / Classic 5.71.0. A later 1.16.1 / 5.71.1 update corrected an interaction with **Run Un-Sandboxed**.

## Related pages

- [Mark Of The Web Box](MarkOfTheWebBox.md)
- [Force Process](ForceProcess.md)
- [Force Folder](ForceFolder.md)
- [Force Box Docs](ForceBoxDocs.md)
- [Disable Force Rules](DisableForceRules.md)
