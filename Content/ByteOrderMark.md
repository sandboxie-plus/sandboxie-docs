# Byte Order Mark

_ByteOrderMark_ is a global setting in [Sandboxie Ini](SandboxieIni). It is typically specified as ByteOrderMark=yes (see [Yes Or No Settings](YesOrNoSettings)), and indicates that [Sandboxie Control](SandboxieControl) should insert a UTF-16 UNICODE Byte Order Mark (BOM) character at the top of the configuration file.

Usage:

```
   .
   .
   .
   [GlobalSettings]
   ByteOrderMark=yes
```

This setting must be edited into [Sandboxie Ini](SandboxieIni), then Sandboxie configuration must be manually [reloaded](ConfigureMenu#reloadconf). Following this, the next time [Sandboxie Control](SandboxieControl) rewrites the configuration, it will insert the UNICODE BOM character into the very first two bytes in the [Sandboxie Ini](SandboxieIni) configuration file, thus: (hex.) FF FE.

You need only bother with this setting if both these statements are true:

*   You plan to edit the [Sandboxie Ini](SandboxieIni) file manually;
*   Your text editor cannot recognize that [Sandboxie Ini](SandboxieIni.) file is a UNICODE text file.
