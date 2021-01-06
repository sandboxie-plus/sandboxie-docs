# Block Sys Param

**BlockSysParam feature is deprecated.**


_BlockSysParam_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies whether Sandboxie will allow sandboxed programs to change various system parameters.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockSysParam=n
```

Specifying _n_ indicates that a sandboxed program should be permitted to issue requests to change various system parameters, such as the desktop wallpaper.

For an extensive discussion about the system parameters that can be changed, please consult the discussion on the [SystemParametersInfo API](https://msdn.microsoft.com/en-us/library/ms724947%28VS.85%29.aspx) on the Microsoft MSDN web site.

**Technical Note:** When Sandboxie blocks a request to change a system parameter, this is logged in the [Resource Access Monitor](ResourceAccessMonitor) as operation _(SystemParametersInfo:nnnnnnnn)_ where _nnnnnnnn_ is a hexadecimal value corresponding to the _uiAction_ parameter passed to the SystemParametersInfo API.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings#lowlevel)
