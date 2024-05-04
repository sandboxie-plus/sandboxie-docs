# Inject Dll 64

_InjectDll_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It tells Sandboxie to "inject" some DLL into every program in the sandbox. "Inject" means the DLL is
```
   .
   .
   .
   [DefaultBox]
   InjectDll64=c:\Program Files\Sandboxie Utilities\Sample64.dll
```

You should specify a full path to the DLL. If the DLL file itself resides within the sandbox, specify the full path inside the sandbox.

**Note:** The InjectDll64 setting specifies 64-bit DLLs, and will be ignored in a 32-bit process, even on 64-bit Windows. Use the [InjectDll](InjectDll.md) setting to specify 32-bit DLLs.

See also: [InjectDll](InjectDll.md) for a comprehensive discussion.
