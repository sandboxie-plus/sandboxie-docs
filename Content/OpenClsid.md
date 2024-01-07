# Open Clsid

_OpenClsid_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the COM class identifiers for unsandboxed COM objects that should be accessible by a sandboxed program. This allows unsandboxed COM ports to be accessed by sandboxed apps.

Examples:
```
   .
   .
   .
   [DefaultBox]
   OpenClsid={D713F357-7920-4B91-9EB6-49054709EC7A}
```

This example makes the HP Universal Printer Status Monitor pop-up component accessible to sandboxed programs.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > COM Access](ResourceAccessSettings.md#com-access)
