# Force Process

_ForceProcess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) that automatically starts matching programs in a particular sandbox. For example:

```ini
[DefaultBox]
ForceProcess=iexplore.exe
ForceProcess=firefox.exe

[MailBox]
ForceProcess=outlook.exe
ForceProcess=cl?cke?.exe
```

The first two entries force Internet Explorer and Firefox into `DefaultBox`. The other entries force Outlook and executable names such as `clicker.exe` or `clicked.exe` into `MailBox`.

An entry without `*` is matched case-insensitively against the executable name and may use `?` to match one character. In the current runtime, an entry containing `*` is instead matched as a case-insensitive pattern against the full normalized executable path. A name-only pattern such as `App*.exe` therefore does not have the same semantics as the older name-only matching; exact executable names are preferable when they are sufficient.

_ForceProcess_ applies only when a program starts outside a sandbox. It is not reapplied when a program is explicitly started in a sandbox or is launched by an already sandboxed program.

## Immersive applications

By default, after a normal _ForceProcess_ or [ForceFolder](ForceFolder.md) rule selects a sandbox, Sandboxie discards that selection if it identifies the resulting process as an immersive/AppContainer application. The global setting below enables these force rules for such processes:

```ini
[GlobalSettings]
AllowForceImmersive=y
```

`AllowForceImmersive` defaults to `n`, is not a per-sandbox setting, and has no dedicated SandMan control. Enabling it does not guarantee compatibility with every AppContainer, UWP, or other immersive application. See [Force Folder](ForceFolder.md#immersive-applications) for the resulting launch behavior and limitations.

## Rule order

Sandboxie checks the executable's directory against _ForceFolder_ before checking _ForceProcess_. Working-directory and document-argument _ForceFolder_ checks occur later, after _ForceProcess_, so _ForceFolder_ does not have unconditional precedence in every case.

## User interfaces

In SandMan, open **Sandbox Options > Program Control > Force Programs** and use **Force Program** to maintain the list. The same page also provides **Force Children**, **Force Folder**, **Remove**, and **Show Templates** controls.

Sandboxie Control Classic provides the related [Sandbox Settings > Program Start > Forced Programs](ProgramStartSettings.md#forced-programs) page.

## Version history

`AllowForceImmersive` was added in Sandboxie Plus 1.16.0 / Classic 5.71.0. _ForceProcess_ predates the current version metadata and has no introduction version recorded there.

## Related pages

- [Force Folder](ForceFolder.md)
- [Program Settings](ProgramSettings.md#page-1)
- [Sandboxie Ini](SandboxieIni.md)
