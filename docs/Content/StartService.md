# Start Service

_StartService_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It allows to run a service program in the sandbox. This setting expects a service name (identifier), which is defined outside the sandbox. For example:

```
   .
   .
   .
   [DefaultBox]
   StartService=Adguard Service
```

The example specifies that the service name _Adguard Service_ will be forced to run sandboxed in the sandbox _DefaultBox_.

**Technical Details**

_StartService_ is processed by [SandboxieRpcSs](ServicePrograms.md#remote-procedure-call-rpc), which runs just once in every sandbox. Like the [AutoExec](AutoExec.md) setting, it is processed when the first program begins to run in a sandbox.

For applications, see [StartProgram](StartProgram.md).
