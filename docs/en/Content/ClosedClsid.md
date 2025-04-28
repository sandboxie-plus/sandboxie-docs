# Closed Clsid

_ClosedClsid_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.5.3a / 5.45.2. It specifies the COM class identifiers for unsandboxed COM objects that should not be accessible by a sandboxed program.

Usage:
```
   .
   .
   .
   [DefaultBox]
   ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

This example makes the _Windows Management and Instrumentation_ not accessible to sandboxed programs.

Related Sandboxie Plus setting: Sandbox Options > Resource Access > COM > Add COM Object > Access column > Closed
