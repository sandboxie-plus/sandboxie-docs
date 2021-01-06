# Border Color

_BorderColor_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls whether Sandboxie displays a colored border around the active foreground window, if that windows belongs to a sandboxed application.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BorderColor=#00FFFF
   BorderColor=#00FFFF,n
```

By default, Sandboxie does not draw the border. This is also true if the _BorderColor_ setting ends with _,n_ as shown in the second example above.

The color is specified in HTML-like RGB color notation:

*   The hash mark prefixes a hexadecimal (base-16) number that is exactly 6-digits long.
*   The first two hex digits denote the red component of the color.
*   The next two hex digits denote the green component of the color.
*   The last two hex digits denote the blue component of the color.

The border will not be drawn when [Sandboxie Control](SandboxieControl.md) is not running.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Appearance](AppearanceSettings.md)
