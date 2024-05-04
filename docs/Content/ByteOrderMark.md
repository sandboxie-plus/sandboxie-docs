# Byte Order Mark

**This feature was removed since v0.6.5 / 5.47.0.**

_ByteOrderMark_ was a global setting in [Sandboxie Ini](SandboxieIni.md). It was typically specified as ByteOrderMark=y (see [Yes Or No Settings](YesOrNoSettings.md)), and indicated that [Sandboxie Control](SandboxieControl.md) should insert a UTF-16 UNICODE Byte Order Mark (BOM) character at the top of the configuration file.

Usage:

```
   .
   .
   .
   [GlobalSettings]
   ByteOrderMark=y
```

This setting must be edited into [Sandboxie Ini](SandboxieIni.md), then Sandboxie configuration must be manually [reloaded](ConfigureMenu.md#reload-configuration). Following this, the next time [Sandboxie Control](SandboxieControl.md) rewrites the configuration, it will insert the UNICODE BOM character into the very first two bytes in the [Sandboxie Ini](SandboxieIni.md) configuration file, thus: (hex.) FF FE.

You need only bother with this setting if both these statements are true:

*   You plan to edit the [Sandboxie Ini](SandboxieIni.md) file manually;
*   Your text editor cannot recognize that [Sandboxie Ini](SandboxieIni.md) file is a UNICODE text file.
