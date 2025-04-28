# Block Sys Param

**BlockSysParam feature was removed in SBIE version 4.+ and up. It is no longer available.**


_BlockSysParam_ was a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specified whether Sandboxie should allow sandboxed programs to change various system parameters.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockSysParam=n
```

Specifying _n_ indicates that a sandboxed program should be permitted to issue requests to change various system parameters, such as the desktop wallpaper.

For an extensive discussion about the system parameters that can be changed, please consult the discussion on the [SystemParametersInfo API](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa) on the Microsoft MSDN web site.

**Technical Note:** When Sandboxie blocks a request to change a system parameter, this is logged in the [Resource Access Monitor](ResourceAccessMonitor.md) as operation _(SystemParametersInfo:nnnnnnnn)_ where _nnnnnnnn_ is a hexadecimal value corresponding to the _uiAction_ parameter passed to the SystemParametersInfo API.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access--removed)
