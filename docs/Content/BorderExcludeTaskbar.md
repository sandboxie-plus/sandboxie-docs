# BorderExcludeTaskbar

_BorderExcludeTaskbar_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.17.3. It is enabled by default.

```ini
[DefaultBox]
BorderExcludeTaskbar=y
```

This setting affects only the visual border overlay drawn by Sandboxie Plus (SandMan). It does not move, resize, or clip the sandboxed application's window.

## Border overlay behavior

Sandboxie Plus draws the colored frame and optional sandbox name or alias label in a separate overlay window. When _BorderExcludeTaskbar_ is enabled, SandMan clips that overlay around regions excluded from each monitor's reported work area. These regions normally include the Windows taskbar and may include other registered appbar or reserved desktop areas.

The clipping logic derives exclusions from the monitor and work-area rectangles reported for each display, so it is monitor-aware and can account for reserved work areas on multiple monitors. Exact results depend on the information Windows reports; auto-hide taskbars, unusual shell replacements, and unusual appbar layouts may behave differently.

Sandboxed target windows using topmost behavior are exempt from this border-overlay clipping. This is an overlay-rendering exception and does not give the underlying application permission to change taskbar behavior.

The colored frame and sandbox label are rendered in the same overlay, so exclusions affect both where they intersect a reserved work-area region. This includes label-oriented border modes.

_BorderExcludeTaskbar_ is meaningful only while Sandboxie Plus is displaying a visual sandbox border or label. If border display is disabled, there is no overlay for the setting to clip. See [Border Color](BorderColor.md).

## Configuration and runtime behavior

The setting can be configured per sandbox. A value in the global configuration acts as a fallback, and the default is enabled. There is no documented per-program syntax.

This is SandMan overlay behavior, so changing the setting does not require restarting the sandboxed application. The change is applied when the border region is rebuilt. In focused-window border modes, refocusing, moving, or resizing the target window may be necessary before the changed exclusion becomes visible.

There is currently no dedicated checkbox for _BorderExcludeTaskbar_ in the normal Sandbox Options interface. Configure it through the INI configuration.

## Version history

_BorderExcludeTaskbar_ was introduced in Sandboxie Plus 1.17.3. It was initially associated with all-window border behavior, while the current implementation also applies to focused-window border modes. Its default remains enabled.

## Related settings

* [Sandboxie Ini](SandboxieIni.md)
* [Border Color](BorderColor.md)
* [Allow Cover Taskbar](AllowCoverTaskbar.md) controls selected application-window restrictions and is independent of this border-overlay setting.
