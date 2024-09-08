# Code Injection

Sandboxie employs a particularly low level approach of injecting its code into processes during creation.

##### Trigger
The driver registers a PsSetCreateProcessNotifyRoutine callback and when this is triggered inspects if the process should be sandboxed, when it decides so it blocks and requests the SbieSvc service to inject a loader into the process image. Alternatively a suspended process can be created and the driver triggered to put it into a sandbox by using API_START_PROCESS and resuming the process once the driver has finished.

The injection mechanism itself can be adapted to be utilized without the driver. As of version 5.44 the loader code has been moved from the SbieSvc.exe to SbieDll.dll.

##### Overview
The Code Injection mechanism is made up of 3 components, the injector itself, a low-level shell code (LowLevel.dll), and the to be injected payload (SbieDll.dll). Note that the LowLevel.dll is embedded into the loader as a resource.

## Remote Injection
The injection is done calling `_FX ULONG SbieDll_InjectLow(HANDLE hProcess, BOOLEAN is_wow64, BOOLEAN bHostInject, BOOLEAN dup_drv_handle)` and providing the required arguments, the function then:

* Starts with preparing a data block `lowdata` of type `SBIELOW_DATA`, and filling in various values like is_wow64, bHostInject and others...
* Then it uses `SbieDll_InjectLow_CopyCode` to allocate `sizeof(shell_code) + sizeof(SBIELOW_J_TABLE) + 0x400` bytes of Memory in the target process and write the shell code to it.

This function also, in an unrelated last step, copies 48 bytes from the begin of `ntdll!LdrInitializeThunk` into `lowdata.LdrInitializeThunk_tramp`.

* Then if `dup_drv_handle` was set `SbieDll_InjectLow_SendHandle` is used to open a handle to the driver and duplicate it into the process, saving its value to `lowdata.api_device_handle`.
* Then duplicates of a couple of required NTDLL functions are saved to the `lowdata` data block, and the address of the `SBIELOW_J_TABLE` section is stored to `lowdata.Sbie64bitJumpTable`.
* Then the actual trampoline is build by `SbieDll_InjectLow_BuildTramp` in `lowdata.LdrInitializeThunk_tramp`.
* Now the function uses `SbieDll_InjectLow_CopySyscalls` to allocate and fill in another memory segment `syscall_data`.

This block is made up of 2 sections one containing information from the driver that are used to hook all system calls,
this is optionally done by the shell code when `bHostInject == 0`, that is followed by the `SBIELOW_EXTRA_DATA` that points to values stored behind it in the memory block.
The data stored there a couple of offsets, as well as the full paths to the SbieDll.dll that is to be injected later on.

* The address of that auxiliary memory is saved to `lowdata.syscall_data` and the `lowdata` block is written with `SbieDll_InjectLow_CopyData` directly into the shell code memory.
* Finally the `ntdll!LdrInitializeThunk` in the target process gets overwritten using `SbieDll_InjectLow_WriteJump` with a jump instruction into the shell code's entry point.

Now the process can be resumed and the injected code will do its thing.

An important note to make here is that this function does the same for native 64 bit and wow64 emulated 32 bit processes, in fact, on a 64-bit system the injected shell code is always 64 bit. Only much later in the initialization of the process running under wow64 it switches to 32-bit.

## Shell Code (LowLevel.dll) operation

The LowLevel.dll is written partially in assembler and partially in C, its base address is set to 0 to gain position independence.
The initial entry point `_Start` retrieves the current address and calculates the addresses of the data block `data` of type `SBIELOW_DATA` and those of a couple of helper functions written in assembler, with those values as parameter it calls the `EntrypointC` function handing off the operation to the C portion.

The `EntrypointC` function ensures that it will be executed only once, using a spinlock, and then checks if the `data->bHostInject` field is set to `0` it first hooks all the ntdll sys call functions using `InitSyscalls` then it prepares the later loading of the SbieDll.dll using `InitInject` and, on 64 bit systems only, it calls `InitConsole` to modify the ConsoleHandle. If ` bHostInject != 0` the function only calls `InitInject`. Last the trampoline to the original function` data->LdrInitializeThunk_tramp` is called.

##### InitInject

The `InitInject` function checks if the process is running natively (i.e. 32-bit on a x86 system or 64-bit in a x64 system), or if it's running under wow64 (that is a 32-bit process on a 64-bit system) and selects either the native ntdll base address or the one of the wow64 ntdll. On Windows versions prior to 8, that address was located in `KUSER_SHARED_DATA::Wow64SharedInformation` structure, but not on later versions. Sandboxie used the driver to record the address of the wow64 ntdll during image loading and `InitInject` queried the driver for it. Since version 5.44, however, it's driver independent, the loader code uses `NtQueryVirtualMemory` to find the image base address and saves it into the `ntdll_wow64_base` field of the data block.

At this point the top portion of the `data->syscall_data` before the `SBIELOW_EXTRA_DATA` region is no longer required and is repurposed to store temporary data of the type `INJECT_DATA`.

The function then finds the addresses of `LdrLoadDll`, `LdrGetProcedureAddress`, `NtRaiseHardError` and `RtlFindActivationContextSectionString` using a custom `FindDllExport` lookup function by parsing through the previously selected ntdll image, these addresses are stored into the `INJECT_DATA` region, then a couple values from the `SBIELOW_EXTRA_DATA` are also copied into that region, containing paths to the SbieDll.dll (both 32 and 64 bit paths), as well as the name of kernel32.dll.

On 64-bit systems the function distinguishes between the native and the wow64 execution, in the latter case branching off to `InitInjectWow64`.
In the native case it continues with hooking the `RtlFindActivationContextSectionString` function in the ntdll.dll.

* An original copy of the functions begin is first saved to the `INJECT_DATA` structure.
* The address of the structure is written into the detour function which is implemented in assembler.
* Then the `RtlFindActivationContextSectionString` begin is overwritten with a jump instruction to the detour function.
* Last a pointer to the `SBIELOW_DATA` region is saved into the very top of the `INJECT_DATA` region, and the function exits.

In the wow64 case `InitInjectWow64` sets up the `RtlFindActivationContextSectionString` hook on the 32-bit version of the function in the wow64 ntdll.dll in a similar way.

##### RtlFindActivationContextSectionString Detour

In contrary to the above operations which are always executed natively, the `RtlFindActivationContextSectionString` detour function is executed in the mode matching the bit-ness of the started process.

* The function first restores the original `RtlFindActivationContextSectionString` begin.
* Then it loads the kernel32.dll followed by loading the SbieDll.dll and retrieving the address of Ordinal 1.
* Then it saves value of the first argument to the `INJECT_DATA` structure and replaces it with a pointer to said structure.
* Finally, it jumps to address of Ordinal 1, it uses a jump rather than call to invoke it so that when it returns it will return directly to the current caller.

## Payload (SbieDll.dll) operation

The SbieDll.dll hook entry point `Dll_Ordinal1` function starts of by obtaining a few required values from the `INJECT_DATA` structure that was passed as first argument, like the address of `SBIELOW_DATA` data block, and the original value of the first argument. Having copied the required values, it can free the no longer needed `INJECT_DATA`, formally `syscall_data` region.
The function now checks if `bHostInject` is set to `0` in which case it Calls `SbieDll!Dll_InitInjected` this function hooks pretty much everything, ?, last but not least it calls `SbieDll!Ldr_Init` which sets up callbacks for dll loading and calls `SbieDll!Ldr_Inject_Init`. If `bHostInject != 0` however `SbieDll!Ldr_Inject_Init` is called directly from `Dll_Ordinal1`. Once the initialization is completed `Dll_Ordinal1` runs the real `RtlFindActivationContextSectionString` with its original arguments and returns.

As if all this hooking wouldn?t be enough `SbieDll!Ldr_Inject_Init` sets up yet an other hook, this time targeting the actual entry point of the starting process. The function saves the initial bytes of the entry point, and overwrites it with a jump to `SbieDll!Ldr_Inject_Entry64` or to `SbieDll!Ldr_Inject_Entry32` respectively.
Those are implemented in assembler, they pass a pointer to the return address location as argument to `SbieDll!Ldr_Inject_Entry` and clean up the stack, then they return to the begin of the entry point.

##### Ldr_Inject_Entry

This function first restores the original entry point function from `SbieDll!Ldr_Inject_SaveBytes`  and changes its caller?s return address to point to the begin of the entry point. This way once the caller returns the real entry point will be invoked. Then the function checks if `bHostInject` is set to `0` in which case it first calls `SbieDll!Ldr_LoadInjectDlls` and then `SbieDll!Dll_InitExeEntry` which performs the last initialization steps. If `bHostInject != 0` it calls only `SbieDll!Ldr_LoadInjectDlls` this function checks the [Sandboxie.ini](SandboxieIni.md) for the [InjectDll](InjectDll.md) or the [InjectDll64](InjectDll64.md) respectively, and loads the additional dll?s if any are configured.
