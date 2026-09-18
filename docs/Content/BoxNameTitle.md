# Box Name Title

_BoxNameTitle_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls whether Sandboxie displays the name of the sandbox in the title bar of a window that belongs to a sandboxed application.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BoxNameTitle=y
```

By default, Sandboxie only displays the sandboxed [#] indicator in the title bar of a window that belongs to a sandboxed application. For example:

[#] Sandboxie - Front Page - Windows Internet Explorer [#]


Specifying _BoxNameTitle=y_ places the sandbox name in the title bar:

[#] [DefaultBox] Sandboxie - Front Page - Windows Internet Explorer [#]

Sandboxie may skip title modification for windows detected as using custom or client-drawn title bars to avoid excessive DWM repaint activity and high CPU usage. See [Disable Custom Title Optimization](DisableCustomTitleOpt.md) for the per-program opt-out.


Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Appearance](AppearanceSettings.md)
