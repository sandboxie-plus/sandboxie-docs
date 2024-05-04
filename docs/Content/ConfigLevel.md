# Config Level

**Note: In Sandboxie versions before 3.xx, ConfigLevel was a global setting in the [GlobalSettings] section. The global ConfigLevel setting is no longer used, and is ignored if it exists in the configuration file.**

_ConfigLevel_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It is used by [Sandboxie Control](SandboxieControl.md) to manage default configuration for a sandbox.

When ConfigLevel is missing, not a number, or a number below 9, Sandboxie Control will add the following configuration to the sandbox:

```
   .
   .
   .
   [DefaultBox]
   ConfigLevel=9
   Template=OpenSmartCard
   Template=OpenBluetooth
```
Note that ConfigLevel value was changed from 8 to 9 with the release of Sandboxie v0.7.5 / 5.49.8.

In the future, new configuration levels may be added in later versions of Sandboxie.
