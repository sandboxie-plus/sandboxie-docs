# Use Fake Shell Dispatch

_UseFakeShellDispatch_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.17.3. It provides a Shell automation compatibility fallback and is enabled by default.

```ini
[DefaultBox]
UseFakeShellDispatch=y
```

The setting does not replace all COM activation, does not emulate the complete Windows Shell, and is not limited to Electron or WebView2 applications.

## Shell-dispatch behavior

For eligible desktop-dispatch requests made through `IShellWindows::FindWindowSW`, Sandboxie can preserve a usable sandbox-local dispatch object or fall back to a partial synthetic Shell-dispatch chain.

In a normal security-isolation box, Sandboxie first tries to preserve a usable real Shell dispatch associated with the sandbox. If that cannot be used, it may try other usable real Shell-dispatch paths before falling back to the synthetic implementation.

In Compartment Mode, eligible desktop-dispatch requests use the synthetic Shell-dispatch chain instead of the original host desktop dispatch. This behavior applies to the eligible Shell-dispatch request; it is not a general replacement for all COM traffic.

The fallback supports the core `IShellDispatch` and `IShellDispatch2` interfaces needed for this compatibility path. It does not promise support for later `IShellDispatch3` through `IShellDispatch6` interfaces.

## Supported operations

The synthetic object provides a limited set of properties and actions, including:

- `Application`
- `Parent`
- `Windows`
- `Open`
- `Explore`
- `ControlPanelItem`
- `ShellExecute`

`Open`, `Explore`, `ControlPanelItem`, and `ShellExecute` can perform real Shell actions through Sandboxie's existing shell-execution path; they do not merely return a fabricated success result.

The fallback is intentionally partial and does not implement the full `IShellDispatch` or `IShellDispatch2` surface. Operations such as `BrowseForFolder`, `MinimizeAll`, `ShutdownWindows`, `FindFiles`, and `ServiceStart` are representative examples that are not implemented. Unsupported operations can return a not-implemented or member-not-found style COM failure rather than being silently treated as successful.

Possible outcomes for an eligible request therefore include use of a real usable dispatch, use of the synthetic dispatch, an error for an unsupported synthetic operation, or a COM failure when a required interface or object cannot be created.

## Per-process configuration

_UseFakeShellDispatch_ supports image-qualified values:

```ini
[DefaultBox]
UseFakeShellDispatch=y
UseFakeShellDispatch=problem.exe,n
UseFakeShellDispatch=another.exe,y
```

The unqualified value provides the normal box-level default. A process-qualified entry can disable or enable the behavior for a specific executable, and an exact image-specific setting takes precedence according to Sandboxie's normal image-aware configuration behavior.

## Electron and WebView2

The feature was introduced partly to address Shell-dispatch compatibility cases seen with WebView2-related software, but the implementation itself is general. It is a Shell automation compatibility fallback that may also help some WebView2-based applications.

_UseFakeShellDispatch_ and [UseElectronDetection](UseElectronDetection.md) are independent compatibility controls:

- _UseFakeShellDispatch_ does not depend on Chrome or Electron process classification.
- _UseElectronDetection_ does not enable or disable fake Shell dispatch.
- _UseFakeShellDispatch_ is evaluated for eligible Shell-dispatch calls, while _UseElectronDetection_ classifies processes during startup.

## COM and isolation considerations

Normal Sandboxie COM and CLSID restrictions still apply. The fallback does not itself grant `OpenClsid` access or bypass `ClosedClsid` handling; initial COM activation must succeed through Sandboxie's normal path before the `IShellWindows` compatibility hook can apply. `BoxedCOM` is a broader, related COM-isolation setting rather than a prerequisite for this fallback.

The setting reduces dependence on a host Explorer dispatch object while routing supported Shell actions through Sandboxie's existing shell-execution path. It is a compatibility mechanism, not a standalone security boundary. A resulting launch can still be affected by separately configured [Breakout Process](BreakoutProcess.md) or [Breakout Document](BreakoutDocument.md) rules; this setting does not itself create breakout behavior.

## Applying changes

The setting is evaluated for the current image when an eligible `FindWindowSW` request occurs. A configuration change can affect subsequent eligible calls in an already-running process, but it does not retroactively replace COM objects or results already returned. Restarting the application is usually not required solely for future eligible calls to use the new value.

## Sandboxie Plus interface

There is currently no dedicated SandMan checkbox for _UseFakeShellDispatch_. Configure it through Sandboxie's INI configuration. The absence of a checkbox does not mean that the feature is disabled; its runtime default is enabled.

## Version history

_UseFakeShellDispatch_ was introduced in Sandboxie Plus 1.17.3. It is enabled by default, supports per-process disabling, and currently has no dedicated SandMan checkbox.

## Related configuration

- [Sandboxie Ini](SandboxieIni.md)
- [Breakout Process](BreakoutProcess.md)
- [Breakout Document](BreakoutDocument.md)
- `OpenClsid`
- `ClosedClsid`
- `BoxedCOM`
