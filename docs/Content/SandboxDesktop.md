# Sandbox Desktop and Window Station

## Overview

Sandboxie does not normally give every sandbox its own persistent Windows Window Station and Desktop. Instead, it uses temporary dummy GUI objects and controlled handle substitution during GUI initialization and compatibility handling. A normal sandboxed GUI process ultimately connects to the interactive Window Station and Desktop rather than remaining on a dedicated per-sandbox Win32 desktop.

This page describes that architecture and three settings that affect it:

| Setting | Default | Scope | Current role |
| --- | --- | --- | --- |
| `OpenWndStation` | `n` | Box-wide | Broad compatibility relaxation of the Desktop/Window Station isolation path |
| `UseSbieWndStation` | `y` | Box-wide or image-aware | Dummy Window Station fallback after `CreateWindowStation` fails |
| `UseSbieDeskHack` | `y` | Box-wide or image-aware | Window-object security and `CreateDesktop` compatibility workarounds |

`OpenWndStation` changes token construction, GUI initialization, hook installation, and Job Object UI limits. The two `UseSbie*` settings instead provide narrower compatibility fallbacks within the normal model.

## Windows object model

The Windows GUI object hierarchy relevant to these settings is:

```text
Session
  |
  +-- Window Station
        |
        +-- Desktop
              |
              +-- windows / GUI objects
```

A process is associated with a Window Station, and each GUI thread is associated with a Desktop. The interactive Window Station is normally named `WinSta0`; desktops belonging to that station can display interactive user-interface elements and receive user input.

## Normal Sandboxie GUI initialization

With the default setting:

```ini
OpenWndStation=n
```

Sandboxie initializes a GUI process through this high-level flow:

```text
restricted sandboxed process
        |
        v
Sandboxie obtains GUI objects and handles through SbieSvc
        |
        v
temporary dummy Window Station and Desktop bootstrap
        |
        v
first GUI conversion
        |
        v
Sandboxie applies handles for the real interactive
Window Station and Desktop
        |
        v
normal sandboxed GUI execution
```

The main components have distinct responsibilities:

- SbieDll installs GUI and API hooks, coordinates the bootstrap, substitutes selected handles, and implements compatibility fallbacks.
- SbieSvc and its GuiServer create or obtain the dummy GUI objects, duplicate appropriate handles for the process, and apply relevant Job Object UI restrictions.
- The driver participates in token construction and the token behavior required by this model.
- Separate Win32k hook and filter mechanisms exist, but they are not the main implementation of the three settings on this page.

## Dummy Window Station

Sandboxie's dummy Window Station is a real, non-interactive Win32 Window Station object, not an invented pseudo-handle. It contains a real Desktop and is accessible to the restricted process during GUI bootstrap and compatibility fallbacks.

The dummy station is not a permanent, unique Window Station assigned to each sandbox, and its Desktop is not the application's final interactive desktop. Sandboxie can reuse the dummy object when an application cannot create or query a GUI object normally under its restricted token.

## `OpenWndStation`

```ini
OpenWndStation=y
```

`OpenWndStation` is a box-wide Boolean setting. Its default is `n`.

Enabling it changes the normal GUI-isolation and bootstrap path so Windows can connect the process more directly to the interactive Window Station and Desktop. Current effects include:

- skipping the normal temporary `DesktopName` and dummy-object bootstrap behavior;
- bypassing a subset of Sandboxie's Desktop and Window Station emulation hooks;
- using Low integrity instead of the normal Untrusted integrity level for the relevant token path;
- preserving the token group marked with `SE_GROUP_LOGON_ID` rather than applying the normal group restriction to it;
- omitting a set of Job Object UI restrictions normally applied through this path.

This is the broad compatibility relaxation among the three settings. It does not give the process an unchanged host token or unrestricted access to every GUI object.

### Token and integrity behavior

The normal token path for this GUI model uses Untrusted integrity. With `OpenWndStation=y`, it uses Low integrity and preserves the logon-SID group.

Two related token settings affect this distinction:

- `NoUntrustedToken=y` independently selects Low rather than Untrusted integrity.
- `KeepTokenIntegrity=y` preserves the source integrity level, superseding the Low-versus-Untrusted choice for that aspect.

These effects do not automatically preserve administrator groups, privileges, or every other property of the source token. Token filtering outside these specific changes remains independent.

### Job Object UI restrictions

With `OpenWndStation=y`, Sandboxie does not apply its normal basic Job Object UI-limit set through this path. The omitted limits currently cover:

- `JOB_OBJECT_UILIMIT_EXITWINDOWS`;
- `JOB_OBJECT_UILIMIT_HANDLES`;
- `JOB_OBJECT_UILIMIT_SYSTEMPARAMETERS`;
- `JOB_OBJECT_UILIMIT_READCLIPBOARD`.

The process may still be placed in a Sandboxie Job Object; this setting changes the GUI-related limits applied through that path.

### GUI-hook boundary

Under normal isolation, Sandboxie installs compatibility hooks for selected Desktop and Window Station APIs. With `OpenWndStation=y`, the `Gui_InitEnum` group of Desktop and Window Station hooks is not installed. Other GUI hooks and window-policy mechanisms remain independent.

In particular, `OpenWndStation` does not directly disable:

- filesystem or registry isolation;
- IPC isolation;
- network restrictions;
- all Sandboxie GUI hooks;
- window-class policy;
- all clipboard handling;
- all token restrictions.

It is a targeted compatibility relaxation, not a general sandbox bypass.

## `UseSbieWndStation`

```ini
UseSbieWndStation=y
```

The setting is enabled by default. It supports both box-wide configuration and image-aware overrides, for example:

```ini
UseSbieWndStation=program.exe,n
```

The current runtime uses `UseSbieWndStation` in Sandboxie's wrappers for `CreateWindowStationA` and `CreateWindowStationW`:

```text
application calls CreateWindowStation
        |
        v
Sandboxie calls the real API
        |
        +-- succeeds -> return the newly created Window Station
        |
        v
creation failed
        |
        v
if UseSbieWndStation is effective and the dummy station is available
        |
        v
return the dummy Window Station handle
```

`UseSbieWndStation` therefore allows Sandboxie to use its dummy Window Station as a compatibility fallback when an application's attempt to create a Window Station fails. It does not force every process onto the dummy station, create a station unique to each sandbox, control the main `CreateDesktop` retry path, alter the process token, or change Job Object UI limits.

The SandMan label and some historical descriptions are broader than this current behavior. The setting originated in older Desktop and Window Station compatibility work, but the current executable path uses it primarily after `CreateWindowStation` failure.

Even with `UseSbieWndStation=n`, current built-in compatibility handling can retain the dummy-station fallback for processes classified internally as Chrome or Firefox image types. Disabling the setting therefore does not remove every special-image fallback.

## `UseSbieDeskHack`

```ini
UseSbieDeskHack=y
```

The setting is enabled by default and supports image-aware overrides:

```ini
UseSbieDeskHack=program.exe,n
```

`UseSbieDeskHack` provides compatibility retries for Window-object security queries and Desktop creation when restricted-token behavior prevents an application from completing those operations normally.

### Security-information queries

Sandboxie can retry selected failed Window-object DACL security queries against the dummy Window Station. This applies to specific `GetSecurityInfo` and related NTMARTA compatibility paths; it does not redirect every security-descriptor request.

There is also narrow `SetSecurityInfo` compatibility handling for some internally classified browser images. This is not a universal fake-success behavior.

### `CreateDesktop` compatibility

The high-level `CreateDesktopA/W` flow is:

```text
try the normal Windows CreateDesktop operation
        |
        v
if needed, retry using Sandboxie's dummy Window Station
        |
        v
if UseSbieDeskHack applies, retry with simplified
device and security parameters
        |
        v
return the result or apply Sandboxie's compatibility fallback
```

Sandboxie does not currently install an equivalent hook for `CreateDesktopEx`.

For `OpenDesktop`, the normal `Default` desktop path can return a duplicated handle to the real interactive Desktop. Other failures use Sandboxie's compatibility path.

With `OpenWndStation=y`, the normal `Gui_InitEnum` `CreateDesktop` and `OpenDesktop` hooks are not installed. The application observes native Windows API behavior for that part of the path, subject to its token and available Window Station rights. Other desktop-related GUI hooks can still remain active.

Even with `UseSbieDeskHack=n`, current source retains built-in compatibility behavior for processes classified internally as Chrome, Firefox, or Acrobat Reader image types. A per-box or per-image `n` value does not disable every related fallback for those image types.

## Interactions and boundaries

### `NoSecurityIsolation`

With `NoSecurityIsolation=y`, important normal paths are already bypassed, including primary-token replacement, the normal Sandboxie GUI bootstrap, the relevant Desktop and Window Station hook set, and the same Job UI-restriction path. `OpenWndStation` is therefore largely redundant for those particular mechanisms.

Application Compartment mode can still retain independent GUI, window-message, and window-class policies. It should not be described as having no GUI isolation.

### Window-class policy

`OpenWinClass`, `ClosedWinClass`, and `NoRenameWinClass` control related but independent window-policy mechanisms. `OpenWndStation` does not make those settings generally redundant. See [Open Win Class](OpenWinClass.md) and [No Rename Win Class](NoRenameWinClass.md).

### Clipboard

The clipboard is associated with a Window Station, but Sandboxie also implements separate clipboard hooks and proxy behavior. `OpenWndStation` omits `JOB_OBJECT_UILIMIT_READCLIPBOARD`; it does not replace or disable all Sandboxie clipboard handling.

### Win32k and other desktop options

The settings on this page are implemented primarily through SbieDll USER32, ADVAPI, and NTMARTA hooks, SbieSvc/GuiServer behavior, and driver token adjustments. Separate Win32k hook and filter mechanisms are outside this page.

`NoSandboxieDesktop` is a separate, broader debugging and compatibility option that can bypass Sandboxie's normal desktop proxy and bootstrap.

Secure-desktop and UAC behavior use a separate flow. See [Prompt On Secure Desktop](PromptOnSecureDesktop.md) and [Use Sandboxie UAC](UseSandboxieUAC.md).

## SandMan configuration

### `OpenWndStation`

Path: **Sandbox Options > Security Options > Security Isolation > Desktop Isolation**

Label: **Open Window Station (improves compatibility by reducing desktop isolation)**

The checkbox is unchecked by default. Checking it writes `OpenWndStation=y`; clearing it removes the explicit value and uses the disabled default. The reduction in desktop isolation is the combined change to bootstrap behavior, selected hooks, token integrity and logon-SID handling, and Job Object UI limits described above.

### `UseSbieWndStation`

Path: **Sandbox Options > Various Options > Compatibility**

Label: **Emulate sandboxed window station for all processes**

The checkbox is checked by default. The default state normally requires no explicit key; clearing it writes `UseSbieWndStation=n`. The label is broader than the current executable behavior, which primarily uses the setting as a fallback after `CreateWindowStation` failure.

### `UseSbieDeskHack`

Path: **Sandbox Options > Various Options > Compatibility**

Label: **Use desktop object workaround for all processes**

The checkbox is checked by default. The default state normally requires no explicit key; clearing it writes `UseSbieDeskHack=n`.

No dedicated New Box Wizard controls or certificate restrictions were identified for these three settings. SandMan also supports image-aware editing for the two `UseSbie*` options even though their current setting metadata describes them more simply.

## Applying configuration changes

`OpenWndStation` affects token construction, GUI initialization, hook installation, and Job Object setup. Recreate or restart the affected sandboxed process tree after changing it; an existing process will not have its token, Job Object, or Desktop bootstrap rebuilt.

`UseSbieWndStation` is consulted during `CreateWindowStation` compatibility handling, but restarting affected applications is recommended so the dummy objects and hooks have a predictable initialization state. `UseSbieDeskHack` affects both hook installation and runtime compatibility retries, so affected applications or process trees should also be restarted after it changes.

A SandMan, SbieSvc, or driver restart is not normally required.

## Failure behavior

Failures can occur while creating dummy GUI objects, obtaining or duplicating real Window Station and Desktop handles, completing GUI bootstrap, or processing native and compatibility calls to `CreateWindowStation`, `CreateDesktop`, and `OpenDesktop`.

Sandboxie retries or applies compatibility fallbacks for some failures, while other failures can cause the individual API call or GUI initialization to fail. Applications should not rely on one universal error code or on the internal form of a compatibility handle.

## Sandboxie Plus and Classic

Runtime support for these settings is implemented in shared Sandboxie components. SandMan provides the current controls, and compatible INI settings can be consumed by the shared runtime. No equivalent current controls were confirmed in the Sandboxie Control Classic interface, so UI parity should not be assumed.

## Version history

- Before Sandboxie Plus 0.7.3 / Classic 5.49.5, Chrome and Firefox image types already received specific compatibility behavior.
- Sandboxie Plus 0.7.3 / Classic 5.49.5 introduced `UseSbieWndStation`.
- Sandboxie Plus 1.0.6 / Classic 5.55.6 made `UseSbieWndStation=y` the default.
- Sandboxie Plus 1.1.2 / Classic 5.56.2 added `UseSbieDeskHack` for broader process use.
- Sandboxie Plus 1.8.2 / Classic 5.63.2 made `UseSbieDeskHack` enabled by default.
- `OpenWndStation` metadata was introduced in Sandboxie Plus 1.14.9 / Classic 5.69.9, while the principal current GUI bootstrap behavior appeared in the 1.15.0 / 5.70.0 development.
- Sandboxie Plus 1.15.6 / Classic 5.70.6 fixed a Windows 10 BSoD scenario involving `OpenWndStation=y` and applications calling `CreateDesktopA/W`. The current implementation avoids the relevant condition by omitting the normal Job Object UI limits in this mode; this is historical, not a current reproducible limitation.
- Sandboxie Plus 1.16.7 / Classic 5.71.7 fixed the interaction between `OpenWndStation=y` and `SandboxieAllGroup=y`. Current token handling preserves the logon SID before adding the Sandboxie group.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
- [Use SbieDesk Hack](UseSbieDeskHack.md)
- [Open Win Class](OpenWinClass.md)
- [No Rename Win Class](NoRenameWinClass.md)
- [Prompt On Secure Desktop](PromptOnSecureDesktop.md)
- [Use Sandboxie UAC](UseSandboxieUAC.md)
- [Special Image](SpecialImage.md)
