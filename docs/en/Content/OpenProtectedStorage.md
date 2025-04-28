# Open Protected Storage

_OpenProtectedStorage_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It is typically specified as _OpenProtectedStorage=y_ (see [Yes Or No Settings](YesOrNoSettings.md)), and indicates that Sandboxie should not isolate [Protected Storage](ProtectedStorage.md) in the sandbox. For example:
```
   .
   .
   .
   [DefaultBox]
   OpenProtectedStorage=y
```

Indicates that programs running in the DefaultBox sandbox will update the global system [Protected Storage](ProtectedStorage.md), rather than a sandboxed instance of it.

Related Sandboxie Plus setting: Sandbox Options > App Templates > Templates > Open Protected Storage

Related [Sandboxie Control](SandboxieControl.md) setting: _Save outside sandbox: History of search strings and invoked commands_ in [Sandbox Settings > Applications > Web Browser](ApplicationsSettings.md#web-browser)
