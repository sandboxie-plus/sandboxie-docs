# Inject Dll


_InjectDll_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It tells Sandboxie to "inject" some DLL into every program in the sandbox. "Inject" means the DLL is
```
   .
   .
   .
   [DefaultBox]
   InjectDll=c:\Program Files\Sandboxie Utilities\Sample.dll
```

You should specify a full path to the DLL. If the DLL file itself resides within the sandbox, specify the full path inside the sandbox.

**Note:** The InjectDll setting specifies 32-bit DLLs, and will be ignored in a 64-bit process on 64-bit Windows. Use the [InjectDll64](InjectDll64.md) setting to specify 64-bit DLLs.

* * *

The order of DLLs loaded into the sandboxed program is thus:

*   Ntdll.dll
*   KernelBase.dll (on Windows 7 and later)
*   Kernel32.dll
*   SbieDll.dll (on 64-bit Windows, this can be either the 64-bit SbieDll or the 32-bit SbieDll)
*   _InjectDlls_ (loaded in the order specified in Sandboxie.ini)
*   Optionally, ShimEng (or AppHelp on Windows 7 and later) and related DLLs
*   All [statically-linked](https://msdn.microsoft.com/en-us/library/ms684184(VS.85).aspx) DLLs

The behavior described above applies to Sandboxie version 3.46 and later. Earlier versions of Sandboxie implemented a different behavior which is described below:

The injected DLL is loaded into the sandboxed process (or program) after all the statically-linked DLLs are loaded and initialized, but before the program itself begins to execute at its entry point.

* * *

If the DLL exports the symbol **InjectDllMain** or **InjectDllMain@8**, Sandboxie will call this procedure after the DLL is loaded, and pass the address of the SbieDll module. Declare InjectDllMain in your code:
```
   __declspec(dllexport) void __stdcall InjectDllMain(
      HINSTANCE hSbieDll, ULONG_PTR UnusedParameter);
```

It is recommended to use the **hSbieDll** parameter as the module instance handle for SbieDll.Dll, instead of relying on GetModuleHandle("SbieDll.dll"). This makes it possible for the injected DLL to interact with SbieDll.dll regardless of the actual name used for SbieDll.dll. However, using LoadLibrary or GetModuleHandle to look up SbieDll by name is also fine.

* * *

At this time, this setting cannot be manipulated from [Sandboxie Control](SandboxieControl.md). You have to manually edit it into [Sandboxie Ini](SandboxieIni.md).

See also: [InjectDll64](InjectDll64.md), [SBIE DLL API](SBIEDLLAPI.md), [Start Command Line](StartCommandLine.md).
