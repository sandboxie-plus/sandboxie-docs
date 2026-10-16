# Inject Dll

_InjectDll_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) that loads an additional DLL during the startup of an eligible sandboxed x86 process. "Inject" means loading the DLL into that process; it does not guarantee that every sandboxed program reaches the required loading stage. For example:

```ini
   .
   .
   .
   [DefaultBox]
   InjectDll=c:\Program Files\Sandboxie Utilities\Sample.dll
```

## Architecture selection

The applicable SbieDll build selects one setting list, not the Windows architecture alone. There is no fallback to another architecture's list. Use a DLL compatible with the target process:

| Execution context | Setting |
| --- | --- |
| x86 | `InjectDll` |
| x86 on x64 Windows | `InjectDll` |
| Native x64 | `InjectDll64` |
| Native ARM64 | `InjectDllARM64` |
| x86 emulation on ARM64 | `InjectDll` |
| x64 on ARM64 using Sandboxie's ARM64EC-specific build | `InjectDll64` |

Use [InjectDll64](InjectDll64.md) for the x64 path; native ARM64 uses `InjectDllARM64`. The x64-on-ARM64 mapping describes the inspected source/build model, not independently runtime-tested compatibility with arbitrary ARM64EC DLLs. See the [setting selection](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr_init.c#L34-L60) and [ARM64EC build definitions](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/Sandbox64ec.props#L14-L18).

## Configuration and DLL paths

Entries come from the effective configuration associated with the sandboxed process. Direct sandbox values, applicable enabled templates, and `GlobalSettings` values can participate. Repeat the setting for multiple DLLs. The [configuration query](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbieapi.h#L371-L372) disables variable expansion, not templates or global fallback; the [driver lookup](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/conf.c#L1505-L1567) supplies the effective values.

Each value is a DLL path. This consumer does not interpret executable-name prefixes, ProcessGroup, or wildcard or negated process selectors.

You should specify a full path to the DLL. If the DLL file itself resides within the sandbox, specify the full path inside the sandbox. The file must be accessible in the target process context, have a compatible architecture, and satisfy applicable image-mapping restrictions. Configuring its path does not guarantee successful loading.

An installation-relative form begins with a backslash:

```ini
[DefaultBox]
InjectDll=\Extensions\Example.dll
```

The loader prefixes this form with the Sandboxie installation directory when the combined path fits its length check. It is not a generic filesystem-root path. UNC-style or native paths beginning with backslashes should not be assumed to retain their original meaning.

The [extra-DLL loader](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr_init.c#L178-L274) requires a `.dll` suffix, case-insensitively, and skips strings containing literal `..` anywhere. It does not expand configuration variables or perform general path canonicalization. Some other relative strings reach the native loader, but this is not a verified arbitrary relative-path search contract; do not rely on bare or relative DLL names.

## Startup and multiple DLLs

The current startup path loads configured DLLs after normal initialization of [statically imported DLLs](https://learn.microsoft.com/en-us/windows/win32/dlls/load-time-dynamic-linking) and before the original executable entrypoint. Remaining Sandboxie entrypoint initialization follows the configured loads and callbacks. This replaces the old fixed system-DLL ordering; it is not a guarantee of the order of every Windows DLL. See the [entrypoint path](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr_init.c#L736-L910).

SbieDll must reach this startup path, install the executable-entrypoint interception, and the process must reach that entrypoint. A zero executable entrypoint prevents this interception path; early exits or initialization failures can also prevent configured loading.

Entries are processed sequentially in their effective enumeration order: query the value, validate its string, attempt native loading, and invoke an optional callback after a successful load before proceeding to the next entry. Dependencies, callbacks, and other loader activity can cause additional DLL loads, so the explicit list does not establish a total module-loading order.

The consumer does not sort or deduplicate entries. Duplicate entries can cause repeated load attempts and callback lookup; they do not guarantee repeated Windows `DLL_PROCESS_ATTACH` notifications. Loading is not transactional and provides no automatic rollback.

## Optional InjectDllMain callback

After a successful load, Sandboxie first looks for `InjectDllMain`, then `_InjectDllMain@8` if the first lookup supplies no address. A callback is optional: a DLL without a matching export can remain loaded. Declare the callback in your code:

```c
__declspec(dllexport) void __stdcall InjectDllMain(
    HINSTANCE hSbieDll,
    ULONG_PTR UnusedParameter);
```

The callback is synchronous. Its first argument is the loaded SbieDll module handle, not the injected DLL's handle; its second argument is zero. The loader does not consume a return value. A successful DLL load alone does not prove that a callback was found or executed successfully.

Use appropriate C linkage (`extern "C"`) for a C++ implementation and verify the actual exported names and ABI. x86 `__stdcall` decoration matters; other architectures and toolchains can use different conventions. Use the intended export names rather than relying on permissive matching details in the [current lookup](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L1288-L1341).

It is recommended to use `hSbieDll` when resolving SbieDll entrypoints: the supplied handle identifies the instance without assuming its filename. `LoadLibrary` or `GetModuleHandle` can also locate SbieDll by name when appropriate, but should not be assumed universally equivalent to the supplied handle. This callback is distinct from the separate `SbieDll_RegisterDllCallback` API.

## SandMan and Classic configuration

In **Sandbox Options > Various Options > Dlls & Extensions**, SandMan manages DLL mappings supplied by installed add-ons, not arbitrary custom DLL paths. Add-ons can supply x86, x64, and, in a native ARM64 SandMan build, ARM64 mappings.

Checked, partially checked, and unchecked states reflect matches in the direct box lists for recognized add-on architecture mappings. Partial state is not an inheritance indicator. The panel does not display the full effective template/global configuration, so an unchecked add-on does not prove that no inherited DLL entry applies.

Changing an add-on's state can remove or replace direct entries with a matching DLL suffix, including manually configured paths to another copy with that suffix. Entries without that suffix match are preserved. See the [panel loading](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/SandboxiePlus/SandMan/Windows/OptionsAdvanced.cpp#L237-L286) and [saving](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/SandboxiePlus/SandMan/Windows/OptionsAdvanced.cpp#L509-L546) code.

For arbitrary custom paths, edit [Sandboxie Ini](SandboxieIni.md) manually; SandMan also provides **Edit ini Section > Edit ini**. [Sandboxie Control](SandboxieControl.md) Classic does not provide the equivalent add-on panel. Its **Configure > Edit Configuration** workflow opens the INI editor and can reload configuration after the editor exits.

## Applying changes

Save/reload configuration as required by the editing workflow, then restart affected sandboxed applications to apply a changed DLL list reliably. Newly started eligible processes can use the updated effective entries. No service, driver, or Windows restart is inherently required solely for an ordinary list change.

Already initialized processes do not automatically reenumerate the list, and removing an entry does not automatically unload a DLL already loaded into them. A process created before reload but not yet at its startup query may still see the updated values.

## Failures and trust

- Missing effective entries mean no extra DLLs from these settings. Oversized values can be skipped, while other configuration-query failures can stop enumeration.
- A wrong extension or literal `..` causes that entry to be skipped; later entries can still be processed.
- Ordinary native load failure, such as a missing, inaccessible, or incompatible DLL, does not invoke its callback and normally allows the next entry to be attempted. Applicable image-mapping policy can also deny loading.
- A missing callback is not a load failure. Callback faults have no demonstrated local exception-isolation barrier and can interrupt subsequent loading or startup. Early initialization or entrypoint-interception failures can prevent this path entirely.

Ordinary load-failure continuation is not a guarantee for allocation failures, callback faults, or startup failures. These settings provide no universal recovery or retry mechanism, and failures can be diagnosed by other Windows or Sandboxie components.

Load only trusted, architecture-compatible DLLs and protect their storage from unintended modification. A DLL in a writable sandbox location can be changed before a later process loads it. Ordinary injected code runs inside the target sandboxed process under its existing identity and restrictions; loading it does not independently grant unrestricted host privileges or bypass applicable file and image-mapping policy.

[Host Injection](HostInjection.md) is a separate path with different target identity, path restrictions, and initialization behavior. Do not use its `HostInjectDll*` examples as ordinary `InjectDll*` guidance.

See also: [InjectDll64](InjectDll64.md), [SBIE DLL API](SBIEDLLAPI.md), [Start Command Line](StartCommandLine.md).
