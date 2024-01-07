# Inject Dll

The _InjectDll_ setting in [Sandboxie Ini](SandboxieIni.md) allows Sandboxie to inject a specified DLL into every program within the sandbox. This can be useful for extending functionality or implementing custom behavior.

To implement this setting, you should include it in the [DefaultBox] section, providing the full path to the DLL, as demonstrated below:

```ini
[DefaultBox]
InjectDll=c:\Program Files\Sandboxie Utilities\Sample.dll
```

Ensure that the full path is specified, and if the DLL resides within the sandbox, use the full path inside the sandbox.

**Note:** The InjectDll setting is for 32-bit DLLs and won't affect 64-bit processes on 64-bit Windows. For 64-bit DLLs, use the [InjectDll64](InjectDll64.md) setting.

### DLL Loading Order:

1. Ntdll.dll
2. KernelBase.dll (only on Windows 7)
3. Kernel32.dll
4. SbieDll.dll (64-bit SbieDll or 32-bit SbieDll on 64-bit Windows)
5. _InjectDlls_ (loaded in order specified in Sandboxie.ini)
6. Optionally, ShimEng (or AppHelp on Windows 7) and related DLLs
7. All [statically-linked](https://msdn.microsoft.com/en-us/library/ms684184(VS.85).aspx) DLLs

This behavior is applicable from Sandboxie version 3.46 onwards. Earlier versions had a different loading behavior, explained below:

The injected DLL loads into the sandboxed process after the initialization of statically-linked DLLs but before the program execution starts at its entry point.

### DLL Interaction:

If the DLL exports **InjectDllMain** or **InjectDllMain@8**, Sandboxie will call this procedure after loading. Declare InjectDllMain in your code as follows:

```c
__declspec(dllexport) void __stdcall InjectDllMain(HINSTANCE hSbieDll, ULONG_PTR UnusedParameter);
```

It's recommended to use the **hSbieDll** parameter as the module instance handle for SbieDll.Dll for interaction. However, using LoadLibrary or GetModuleHandle to look up SbieDll by name is also acceptable.

**Note:** This setting is not adjustable from [Sandboxie Control](SandboxieControl.md) at this time; manual editing of [Sandboxie Ini](SandboxieIni.md) is required.

See also: [InjectDll64](InjectDll64.md), [SBIE DLL API](SBIEDLLAPI.md), [Start Command Line](StartCommandLine.md).
