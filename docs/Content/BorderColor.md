# Border Color

_BorderColor_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It controls whether Sandboxie displays a colored border around the active foreground window, if that windows belongs to a sandboxed application.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BorderColor=#00FFFF,ttl,6
   BorderColor=#00FFFF,off,6
   BorderColor=#00FFFF,on,6
```
Its default value is  _"#00FFFF,ttl,6"_. The number represents the default pixel width of the drawn border and can be omitted.

Sandboxie doesn't draw the border if _BorderColor_ ends with _",off,6"_, while in previous versions it was  _",n"_.

The color is specified in HTML-like RGB color notation:

*   The hash mark prefixes a hexadecimal (base-16) number that is exactly 6-digits long.
*   The first two hex digits denote the red component of the color.
*   The next two hex digits denote the green component of the color.
*   The last two hex digits denote the blue component of the color.

The border will not be drawn when [Sandboxie Control](SandboxieControl.md) is not running.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Appearance](AppearanceSettings.md)
