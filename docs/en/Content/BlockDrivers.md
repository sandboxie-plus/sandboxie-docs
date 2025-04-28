# Block Drivers

**This feature was removed in SBIE version 4.+ and up. It is no longer available.**

_BlockDrivers_ was a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specified whether Sandboxie should allow sandboxed programs to load drivers into the operating system. However, this setting did _not_ govern the _installation_ of new drivers -- see more below.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockDrivers=n
```

Specifying _n_ indicates that a sandboxed program may load drivers into the operating system. If this is not done, Sandboxie will deny the driver load attempt, and instead issue message [SBIE2103](SBIE2103.md).

**Note:** Disabling the protection afforded by BlockDrivers is not recommended.

**Driver Installation**

Before a driver can be loaded, it must first be installed. Driver installation is not affected by the BlockDrivers setting. To allow driver installation, you should add the following OpenKeyPath setting:

```
OpenKeyPath=HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
```

And you should additionally _open_ the driver file, using OpenFilePath. This is needed because the driver path that will be set in the registry (in a key created below CurrentControlSet\Services) will typically not point inside the sandbox.

```
OpenFilePath=c:\program files\MyNewSoftware\SoftwareDriver.sys
```

**Note:** Allowing sandboxed programs to install drivers is not recommended.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access--removed)
