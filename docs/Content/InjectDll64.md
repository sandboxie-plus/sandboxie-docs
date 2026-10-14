# Inject Dll 64

_InjectDll64_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) that loads an additional DLL during the startup of an eligible sandboxed process using the x64 SbieDll path. "Inject" means loading the DLL into that process, not guaranteed loading into every sandboxed program. For example:

```ini
   .
   .
   .
   [DefaultBox]
   InjectDll64=c:\Program Files\Sandboxie Utilities\Sample64.dll
```

You should specify a full path to the DLL. If the DLL file itself resides within the sandbox, specify the full path inside the sandbox. The DLL must be accessible and compatible with the target process; file permissions and image-mapping restrictions can still prevent loading.

**Note:** The applicable SbieDll build selects the setting, not Windows bitness alone. Native x64 uses `InjectDll64`; x86 processes use [InjectDll](InjectDll.md), even on 64-bit Windows. Native ARM64 uses `InjectDllARM64`, not `InjectDll64`. Sandboxie's ARM64EC-specific build for x64 on ARM64 uses `InjectDll64` in the current source/build model; this is not independently runtime-tested compatibility with arbitrary ARM64EC DLLs.

The same loading, optional-callback, failure, and restart limitations described on the main page apply. Configuration reload does not automatically load or unload these DLLs in already initialized processes.

See also: [InjectDll](InjectDll.md) for a comprehensive discussion.
