# Start Program

_StartProgram_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). This feature provides an automatic start for the specified process. Any specified application will automatically run inside sandboxie. For example:

```
   .
   .
   .
   [DefaultBox]
   StartProgram=chrome.exe
   StartProgram=Ccleaner.exe
   [MailBox]
   StartProgram=FireZilla.exe
   
```

The example specifies that Chrome (chrome.exe) and Ccleaner (Ccleaner.exe) will be forced to run sandboxed in the sandbox _DefaultBox_. Fire (FireZilla.exe) will be forced to run sandboxed in the sandbox _MailBox_.

Note that the _StartProgram_ launches the specified application in hidden mode, for services see [StartService](StartService.md).
