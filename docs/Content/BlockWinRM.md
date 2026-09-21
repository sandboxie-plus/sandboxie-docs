# Block WinRM

*BlockWinRM* is a Sandboxie mitigation for Windows Remote Management (WinRM) and its remote-command component, WinRS. It does not disable the host WinRM service or block all networking. Current Sandboxie applies a file-component restriction and a separate policy value in the sandboxed registry view.

## Current enforcement layers

The mandatory `Template_BlockWinRM` in `[DefaultTemplates]` supplies `ClosedFilePath` rules for the WinRM/WinRS components `wsmsvc.dll`, `wsmauto.dll`, and `winrs.exe` under the relevant Windows system directories. These are file-access restrictions for sandboxed processes, not a guarantee that every possible remote-management route is blocked.

Separately, during initial sandbox customization, the enabled `BlockWinRM` option makes Sandboxie attempt to write the DWORD `AllowNegotiate=0` under:

```text
HKLM\Software\Policies\Microsoft\Windows\WinRM\Client
```

This value is placed in the sandboxed registry view; Sandboxie does not change the host's real WinRM policy through this operation.

## Configuration and the meaning of `n`

```ini
[DefaultBox]
BlockWinRM=y
```

The setting defaults to `y` when no effective value exists. A box-specific value takes precedence over `[GlobalSettings]`. There is no dedicated SandMan or Sandboxie Control Classic checkbox for this option. In SandMan, use **Sandbox Options > Edit ini Section > Edit ini** to configure the Boolean manually.

In the current implementation, `BlockWinRM=n` prevents the Boolean-controlled `AllowNegotiate=0` customization when that customization has not yet run. It does **not**, by itself, remove the file restrictions supplied by the mandatory `Template_BlockWinRM`. Other applicable file-access rules still determine effective access to those components. Thus, `n` is not a general switch that fully enables WinRM inside a sandbox.

The historical Sandboxie Plus 0.7.1 / Classic 5.48.5 changelog said that `BlockWinRM=n` disabled the WinRM file block. That described the earlier direct driver path; the current build uses the default template for those file rules instead.

## Applying changes

The file-component rules are loaded into a process's file policy when it starts. Restart affected sandboxed processes after changing relevant file rules.

The registry customization is different: it runs when a box is first customized and leaves state in the sandbox content. Changing `BlockWinRM` later does not automatically clear an existing `AllowNegotiate=0` value or necessarily rerun customization for an existing box. If a change must affect the initial sandboxed policy state, use an empty or newly created box and restart its processes. Emptying a box removes its existing sandbox content, so preserve anything needed first.

## Scope and related pages

This setting is distinct from [Block Network Files](BlockNetworkFiles.md), which controls access to network-share files and folders. Neither setting replaces Internet-access or firewall policy. See [Sandboxie Ini](SandboxieIni.md) for manual configuration.

## Version history

`BlockWinRM` is listed as added in Sandboxie Plus 0.7.1 / Classic 5.48.5. Mandatory `[DefaultTemplates]` appeared in 0.9.8 / 5.53.0. In 1.7.3 / 5.62.3, the WinRM file-component rules were moved to `Template_BlockWinRM` and included in `[DefaultTemplates]`; the earlier Boolean-controlled driver file list is no longer the active path.
