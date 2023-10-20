# Start Program

_StartProgram_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It provides an automatic start for the specified program. For example:

```
   .
   .
   .
   [DefaultBox]
   StartProgram=%ProgramFiles%\Google\Chrome\Application\chrome.exe
```

The example specifies that Google Chrome (chrome.exe) will be forced to run sandboxed in the sandbox _DefaultBox_.

**Technical Details**

_StartProgram_ is processed by [SandboxieRpcSs](ServicePrograms.md#remote-procedure-call-rpc), which runs just once in every sandbox. Like the [AutoExec](AutoExec.md) setting, it is processed when the first program begins to run in a sandbox. Note that _StartProgram_ launches the specified application in hidden mode, if supported.

For services, see [StartService](StartService.md).
