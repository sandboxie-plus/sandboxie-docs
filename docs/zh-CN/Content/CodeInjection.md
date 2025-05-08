# 代码注入

Sandboxie 采用了一种特别低级的方法在进程创建期间将其代码注入到进程中。

##### 触发器
驱动程序注册一个 PsSetCreateProcessNotifyRoutine 回调函数，当此回调被触发时，它会检查进程是否应该被沙盒化。如果决定要沙盒化，它会阻塞并请求 SbieSvc 服务将加载器注入到进程映像中。另外，也可以创建一个挂起的进程，并通过使用 API_START_PROCESS 触发驱动程序将其放入沙盒中，然后在驱动程序完成后恢复进程。

注入机制本身可以被调整为无需驱动程序即可使用。从 5.44 版本开始，加载器代码已从 SbieSvc.exe 移至 SbieDll.dll。

##### 概述
代码注入机制由 3 个组件组成：注入器本身、低级 shell 代码（LowLevel.dll）和要注入的有效负载（SbieDll.dll）。请注意，LowLevel.dll 作为资源嵌入到加载器中。

## 远程注入
注入是通过调用 `_FX ULONG SbieDll_InjectLow(HANDLE hProcess, BOOLEAN is_wow64, BOOLEAN bHostInject, BOOLEAN dup_drv_handle)` 并提供所需参数来完成的，该函数然后：

* 首先准备一个类型为 `SBIELOW_DATA` 的数据块 `lowdata`，并填入各种值，如 is_wow64、bHostInject 等...
* 然后使用 `SbieDll_InjectLow_CopyCode` 在目标进程中分配 `sizeof(shell_code) + sizeof(SBIELOW_J_TABLE) + 0x400` 字节的内存并将 shell 代码写入其中。

这个函数还在一个不相关的最后步骤中，将 `ntdll!LdrInitializeThunk` 开头的 48 字节复制到 `lowdata.LdrInitializeThunk_tramp` 中。

* 然后如果设置了 `dup_drv_handle`，就使用 `SbieDll_InjectLow_SendHandle` 打开一个驱动程序句柄并将其复制到进程中，将其值保存到 `lowdata.api_device_handle`。
* 然后将一些必需的 NTDLL 函数的副本保存到 `lowdata` 数据块中，并将 `SBIELOW_J_TABLE` 段的地址存储到 `lowdata.Sbie64bitJumpTable`。
* 然后由 `SbieDll_InjectLow_BuildTramp` 在 `lowdata.LdrInitializeThunk_tramp` 中构建实际的跳板。
* 现在函数使用 `SbieDll_InjectLow_CopySyscalls` 分配并填充另一个内存段 `syscall_data`。

此块由 2 个部分组成，一个包含来自驱动程序的信息，用于钩住所有系统调用，
这在 `bHostInject == 0` 时由 shell 代码可选地完成，后面跟着指向内存块中存储的值的 `SBIELOW_EXTRA_DATA`。
存储在那里的数据包括几个偏移量，以及稍后要注入的 SbieDll.dll 的完整路径。

* 该辅助内存的地址被保存到 `lowdata.syscall_data`，并且 `lowdata` 块通过 `SbieDll_InjectLow_CopyData` 直接写入 shell 代码内存。
* 最后，目标进程中的 `ntdll!LdrInitializeThunk` 使用 `SbieDll_InjectLow_WriteJump` 被覆盖为跳转到 shell 代码入口点的指令。

现在可以恢复进程，注入的代码将执行其任务。

这里需要注意的一点是，此函数对原生 64 位和 wow64 模拟的 32 位进程执行相同的操作，实际上，在 64 位系统上注入的 shell 代码始终是 64 位的。只有在进程在 wow64 下运行的初始化后期才会切换到 32 位。

## Shell 代码（LowLevel.dll）操作

LowLevel.dll 部分用汇编语言编写，部分用 C 语言编写，其基地址设置为 0 以获得位置独立性。
初始入口点 `_Start` 检索当前地址并计算类型为 `SBIELOW_DATA` 的数据块 `data` 的地址以及用汇编语言编写的几个辅助函数的地址，将这些值作为参数调用 `EntrypointC` 函数，将操作移交给 C 部分。

`EntrypointC` 函数使用自旋锁确保它只执行一次，然后检查 `data->bHostInject` 字段是否设置为 `0`，如果是，它首先使用 `InitSyscalls` 钩住所有 ntdll 系统调用函数，然后使用 `InitInject` 准备稍后加载 SbieDll.dll，并且仅在 64 位系统上，它调用 `InitConsole` 来修改 ConsoleHandle。如果 `bHostInject != 0`，该函数只调用 `InitInject`。最后调用原始函数 `data->LdrInitializeThunk_tramp` 的跳板。

##### InitInject

`InitInject` 函数检查进程是否以原生方式运行（即在 x86 系统上运行 32 位或在 x64 系统上运行 64 位），或者是否在 wow64 下运行（即在 64 位系统上运行 32 位进程），并选择原生 ntdll 基地址或 wow64 ntdll 的基地址。在 Windows 8 之前的版本中，该地址位于 `KUSER_SHARED_DATA::Wow64SharedInformation` 结构中，但在后来的版本中不是。Sandboxie 使用驱动程序在映像加载期间记录 wow64 ntdll 的地址，`InitInject` 向驱动程序查询该地址。但从 5.44 版本开始，它已经独立于驱动程序，加载器代码使用 `NtQueryVirtualMemory` 查找映像基地址并将其保存到数据块的 `ntdll_wow64_base` 字段中。

此时，`data->syscall_data` 在 `SBIELOW_EXTRA_DATA` 区域之前的顶部部分不再需要，被重新用于存储类型为 `INJECT_DATA` 的临时数据。

然后该函数通过使用自定义的 `FindDllExport` 查找函数解析先前选择的 ntdll 映像，找到 `LdrLoadDll`、`LdrGetProcedureAddress`、`NtRaiseHardError` 和 `RtlFindActivationContextSectionString` 的地址，这些地址存储在 `INJECT_DATA` 区域中，然后还将 `SBIELOW_EXTRA_DATA` 中的一些值复制到该区域中，包含 SbieDll.dll 的路径（32 位和 64 位路径都有），以及 kernel32.dll 的名称。

在 64 位系统上，该函数区分原生和 wow64 执行，在后一种情况下分支到 `InitInjectWow64`。
在原生情况下，它继续钩住 ntdll.dll 中的 `RtlFindActivationContextSectionString` 函数。

* 首先将函数开头的原始副本保存到 `INJECT_DATA` 结构中。
* 将结构的地址写入用汇编实现的 detour 函数中。
* 然后用跳转到 detour 函数的指令覆盖 `RtlFindActivationContextSectionString` 的开头。
* 最后将指向 `SBIELOW_DATA` 区域的指针保存到 `INJECT_DATA` 区域的最顶部，然后函数退出。

在 wow64 情况下，`InitInjectWow64` 以类似的方式在 wow64 ntdll.dll 中的 32 位版本函数上设置 `RtlFindActivationContextSectionString` 钩子。

##### RtlFindActivationContextSectionString Detour

与上述始终以原生方式执行的操作相反，`RtlFindActivationContextSectionString` detour 函数以与启动进程位数匹配的模式执行。

* 该函数首先恢复原始 `RtlFindActivationContextSectionString` 的开头。
* 然后加载 kernel32.dll，接着加载 SbieDll.dll 并检索序号 1 的地址。
* 然后将第一个参数的值保存到 `INJECT_DATA` 结构中，并用指向该结构的指针替换它。
* 最后，它跳转到序号 1 的地址，它使用跳转而不是调用来调用它，这样当它返回时会直接返回到当前调用者。

## 有效负载（SbieDll.dll）操作

SbieDll.dll 钩子入口点 `Dll_Ordinal1` 函数首先从作为第一个参数传递的 `INJECT_DATA` 结构中获取一些必需的值，如 `SBIELOW_DATA` 数据块的地址和第一个参数的原始值。复制了所需的值后，它可以释放不再需要的 `INJECT_DATA`（原 `syscall_data` 区域）。
该函数现在检查 `bHostInject` 是否设置为 `0`，如果是，它调用 `SbieDll!Dll_InitInjected`，这个函数钩住几乎所有内容，最后但同样重要的是，它调用 `SbieDll!Ldr_Init`，该函数设置 dll 加载的回调并调用 `SbieDll!Ldr_Inject_Init`。但如果 `bHostInject != 0`，则 `SbieDll!Ldr_Inject_Init` 直接从 `Dll_Ordinal1` 调用。一旦初始化完成，`Dll_Ordinal1` 使用其原始参数运行真正的 `RtlFindActivationContextSectionString` 并返回。

好像所有这些钩子还不够，`SbieDll!Ldr_Inject_Init` 设置了另一个钩子，这次针对启动进程的实际入口点。该函数保存入口点的初始字节，并用跳转到 `SbieDll!Ldr_Inject_Entry64` 或 `SbieDll!Ldr_Inject_Entry32` 的指令覆盖它。
这些是用汇编实现的，它们将返回地址位置的指针作为参数传递给 `SbieDll!Ldr_Inject_Entry` 并清理栈，然后返回到入口点的开头。

##### Ldr_Inject_Entry

此函数首先从 `SbieDll!Ldr_Inject_SaveBytes` 恢复原始入口点函数，并将其调用者的返回地址更改为指向入口点的开头。这样一旦调用者返回，就会调用真正的入口点。然后该函数检查 `bHostInject` 是否设置为 `0`，如果是，它首先调用 `SbieDll!Ldr_LoadInjectDlls`，然后调用 `SbieDll!Dll_InitExeEntry`，后者执行最后的初始化步骤。如果 `bHostInject != 0`，它只调用 `SbieDll!Ldr_LoadInjectDlls`，这个函数检查 [Sandboxie.ini](SandboxieIni.md) 中的 [InjectDll](InjectDll.md) 或 [InjectDll64](InjectDll64.md)，并加载配置的额外 dll（如果有的话）。 