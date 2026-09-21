# Use Drag Drop Hack

*UseDragDropHack* controls a Sandboxie compatibility workaround for file drops onto sandboxed application windows that register an OLE drop target. It bridges a window-message file drop to that target; it is not a general permission to access host files or a switch for all drag-and-drop operations.

## Configuration and default

```ini
[DefaultBox]
UseDragDropHack=y
```

The current runtime treats an absent effective value as `y`: it requests the workaround by default. This differs from the setting metadata, which lists `[bN]`. An explicit `n` disables this compatibility path for matching processes; it does not disable drag and drop generally.

The setting also supports an executable-qualified value:

```ini
[DefaultBox]
UseDragDropHack=example.exe,n
```

The image-name lookup supports case-insensitive program-name patterns and configured process groups. A positive match for a particular program, pattern, or group outranks a negated match, and both outrank a general value. A `*,` selector has the same priority as an unqualified value. Among matches at the same priority level, the later enumerated entry replaces the earlier one. Box configuration can also inherit entries from templates or `[GlobalSettings]`, so inspect the effective configuration when troubleshooting an override.

For example, the optional `OfficeLicensing` compatibility template contains `UseDragDropHack=excel.exe,n`. When that template applies to a box, it can disable the workaround for Excel. The template calls this an Excel compatibility fix but does not explain the precise failure it addresses.

## How the workaround operates

When the hooks are installed, Sandboxie first calls the real OLE `RegisterDragDrop`. After a successful registration, if the window is not already accepting `WM_DROPFILES`, the workaround adds `WS_EX_ACCEPTFILES`, associates the application's `IDropTarget` with the window, and installs Sandboxie's window-procedure handling. On a compatible file-drop message, Sandboxie constructs an OLE data object and calls the target's `DragEnter`, `DragOver`, and `Drop` methods. A successful `RevokeDragDrop` removes the added association and window style.

This is a compatibility bridge for the covered file-drop path, not a promise that every application or data format will work. Ordinary sandbox file-access and recovery rules remain separate.

## Conditions and limitations

The `RegisterDragDrop` and `RevokeDragDrop` hooks are installed only when Sandboxie's OLE initialization runs and its COM-proxy path is active. `DisableComProxy=y` or open-COM mode bypasses that hook-installation branch, even if `UseDragDropHack=y` is configured.

With `OpenWinClass=*`, Sandboxie also does not install this workaround: the property and window-procedure hooks it needs are not available in that mode. A rule opening only particular window classes is not the same all-classes condition. This does not mean that `OpenWinClass=*` disables every form of drag and drop. See [Open Win Class](OpenWinClass.md) for the broader window-access setting.

Some application types have additional handling after a file-drop message reaches this path. That handling does not make the setting browser-specific or guarantee identical behavior across applications.

## User interface and applying changes

SandMan and Sandboxie Control Classic do not currently provide a dedicated checkbox for `UseDragDropHack`. In SandMan, edit it through **Sandbox Options > Edit ini Section > Edit ini**.

The option is read when SbieDll initializes its `ole32.dll` hooks in a sandboxed process, rather than on each drop. Restart affected sandboxed applications after changing it to ensure their OLE hooks use the new value. A SandMan, service, or driver restart is not normally required.

## Version history

The setting metadata lists Sandboxie Plus 1.9.6 as its introduction version. The 1.9.6 source change added the configuration check and the Excel template exception. The underlying drag-and-drop bridge predates that setting.

## Related pages

- [Open Win Class](OpenWinClass.md)
- [Sandboxie Ini](SandboxieIni.md)
