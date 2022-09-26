# Start Service

_StartService_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). This feature provides an automatic start for the specified service. Any specified service will be started automatically. For example:

```
   .
   .
   .
   [DefaultBox]
   StartService=Google Update.exe
   StartService=Adaware.exe
   
```

The example specifies that Google Update (Google Update.exe) and Adaware (Adaware.exe) will be forced to run sandboxed in the sandbox _DefaultBox_.

Note that the _StartService_ works right after launching any application the specified sandbox, for general applications see [StartProgram](StartProgram.md).
