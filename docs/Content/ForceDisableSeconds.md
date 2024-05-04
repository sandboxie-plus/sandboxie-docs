# Force Disable Seconds

_ForceDisableSeconds_ is a global setting in [Sandboxie Ini](SandboxieIni.md). It specifies the time, in seconds, that the [Disable Forced Programs](FileMenu.md#disable-forced-programs) mode will stay in effect.

Usage:
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableSeconds=25
   ForceDisableSeconds=0
```

The default value for this setting is 10 seconds. Setting the value to zero effectively disables the _Disable Forced Programs_ feature itself. See also: [ForceDisableAdminOnly](ForceDisableAdminOnly.md).

The _Disable Forced Programs_ mode is engaged through [Sandboxie Control](SandboxieControl.md), which can also configure the number of seconds. Use the [FileMenu > Disable Forced Programs](FileMenu.md#disable-forced-programs) command, or the same command from the [Tray Icon Menu](TrayIconMenu.md).

When active, the _Disable Forced Programs_ mode causes Sandboxie to issue message [SBIE1301](SBIE1301.md) whenever a forced program is started.
