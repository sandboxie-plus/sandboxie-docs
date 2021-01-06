# Open Protected Storage

_OpenProtectedStorage_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It is typically specified as _OpenProtectedStorage=y_ (see [Yes Or No Settings](YesOrNoSettings)), and indicates that Sandboxie should not isolate [Protected Storage](ProtectedStorage) in the sandbox. For example:
```
   .
   .
   .
   [DefaultBox]
   OpenProtectedStorage=y
```

Indicates that programs running in the DefaultBox sandbox will update the global system [Protected Storage](ProtectedStorage), rather than a sandboxed instance of it.

Related [Sandboxie Control](SandboxieControl) setting: _Save outside sandbox: History of search strings and invoked commands_  
in [Sandbox Settings > Applications > Web Browsers](ApplicationsSettings#web)
