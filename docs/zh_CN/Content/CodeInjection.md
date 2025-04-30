# 代码注入

Sandboxie 采用了一种特别底层的方式，在进程创建期间将其代码注入目标进程。

##### 触发机制
驱动程序注册了一个 PsSetCreateProcessNotifyRoutine 回调，当该回调被触发时，会检查该进程是否应被放入沙箱。如果决定需要沙箱化，则会阻塞并请求 SbieSvc 服务向进程映像注入加载器。另一种方式是先创建一个挂起状态的进程，通过 API_START_PROCESS 通知驱动将其放入沙箱，待驱动完成后再恢复进程运行。

注入机制本身可以调整为无需驱动即可使用。自 5.44 版本起，加载器代码已从 SbieSvc.exe 移至 SbieDll.dll。

##### 概述
代码注入机制由三个组件组成：注入器本身、底层壳代码（LowLevel.dll）以及待注入的有效负载（SbieDll.dll）。需要注意的是，LowLevel.dll 作为资源嵌入在加载器中。

## 远程注入
注入过程通过调用 `_FX ULONG SbieDll_InjectLow(HANDLE hProcess, BOOLEAN is_wow64, BOOLEAN bHostInject, BOOLEAN dup_drv_handle)` 并传入所需参数实现，该函数主要执行以下步骤：

* 首先准备一个 `SBIELOW_DATA` 类型的数据块 `lowdata`，并填充值，如 is_wow64、bHostInject 等
* 然后利用 `SbieDll_InjectLow_CopyCode` 在目标进程中申请一块 `sizeof(shell_code) + sizeof(SBIELOW_J_TABLE) + 0x400` 字节的内存，并写入壳代码

此外，在相关的最后一步，会从 `ntdll!LdrInitializeThunk` 的起始位置复制 48 字节到 `lowdata.LdrInitializeThunk_tramp`。

* 如果设置了 `dup_drv_handle`，则通过 `SbieDll_InjectLow_SendHandle` 向驱动打开句柄，并将复制的句柄传入进程，保存到 `lowdata.api_device_handle`
* 需要用到的一些 NTDLL 函数的副本也会保存到 `lowdata` 数据块，并将 `SBIELOW_J_TABLE` 区段的地址写入 `lowdata.Sbie64bitJumpTable`
* 然后，实际的跳板由 `SbieDll_InjectLow_BuildTramp` 构建至 `lowdata.LdrInitializeThunk_tramp`
* 现在该函数使用 `SbieDll_InjectLow_CopySyscalls` 再分配一段内存 `syscall_data` 并填充相关内容

该数据块由两部分组成，一部分包含来自驱动的信息，用于 hook 所有系统调用（当 `bHostInject == 0` 时由壳代码完成），随后是 `SBIELOW_EXTRA_DATA`，其中包含指向该内存块后方存储值的指针。
这里保存的一些数据包括偏移量，以及后续要注入的 SbieDll.dll 的完整路径。

* 辅助内存地址被写入 `lowdata.syscall_data`，同时，通过 `SbieDll_InjectLow_CopyData` 将 `lowdata` 数据直接写入壳代码内存中
* 最后，目标进程中的 `ntdll!LdrInitializeThunk` 通过 `SbieDll_InjectLow_WriteJump` 被覆盖为跳转到壳代码入口

此时，进程可以恢复运行，注入的代码将开始执行。

值得一提的是，该函数对于原生 64 位进程和 wow64 模拟的 32 位进程均以相同方式处理，实际上，在 64 位系统中注入的壳代码始终为 64 位，仅在 wow64 下稍后才切换为 32 位。

## Shell 代码（LowLevel.dll）操作

LowLevel.dll 部分采用汇编，部分采用 C 语言实现，其基址被设置为 0 以便实现位置无关性。
初始入口点 `_Start` 获取当前地址，并计算出数据块 `data`（类型为 `SBIELOW_DATA`）及若干汇编实现的辅助函数的地址，并将这些值作为参数传递给 `EntrypointC`，从而将操作流程交由 C 部分处理。

`EntrypointC` 确保自身仅执行一次（使用自旋锁），随后检查 `data->bHostInject` 字段是否为 0。如果为 0，则会先通过 `InitSyscalls` hook 所有 ntdll 系统调用函数，然后使用 `InitInject` 为后续加载 SbieDll.dll 做准备，且仅在 64 位系统下调用 `InitConsole` 修改 ConsoleHandle。如果 `bHostInject != 0`，则仅调用 `InitInject`。最后，跳转回原始函数 `data->LdrInitializeThunk_tramp` 的跳板。

##### InitInject

`InitInject` 检查进程是原生运行（即 x86 系统下的 32 位进程或 x64 系统下的 64 位进程），还是处于 wow64（即 64 位系统下的 32 位进程），并选择使用本机的 ntdll 基址或 wow64 ntdll 的基址。在 Windows 8 之前，该地址位于 `KUSER_SHARED_DATA::Wow64SharedInformation` 结构中，但在更高版本中则不再如此。Sandboxie 曾利用驱动记录在映像加载期间 wow64 ntdll 的地址，由 `InitInject` 向驱动查询。自 5.44 版起，该过程不再依赖驱动，加载器代码直接通过 `NtQueryVirtualMemory` 查询映像基址，并将其写入数据块的 `ntdll_wow64_base` 字段。

此时，`data->syscall_data` 中 `SBIELOW_EXTRA_DATA` 区域之前的部分已无用，被重新用于存储 `INJECT_DATA` 类型的临时数据。

该函数接着通过自定义的 `FindDllExport` 查找与解析选定 ntdll 镜像，定位 `LdrLoadDll`、`LdrGetProcedureAddress`、`NtRaiseHardError` 和 `RtlFindActivationContextSectionString` 的地址并分别存入 `INJECT_DATA` 区域，然后将部分来自 `SBIELOW_EXTRA_DATA` 的值（包括 SbieDll.dll 的 32 位、64 位路径，以及 kernel32.dll 名称）也一并复制进去。

在 64 位系统下，该函数会根据进程的本机或 wow64 执行方式进行分支，若为 wow64 则会跳转到 `InitInjectWow64`。如为本机执行，则继续在 ntdll.dll 内 hook `RtlFindActivationContextSectionString` 函数。

* 首先，将该函数起始处的原始字节保存至 `INJECT_DATA` 结构体
* 结构体地址被写入 detour（分流）函数，该函数用汇编实现
* 然后覆盖 `RtlFindActivationContextSectionString` 的入口为跳转到 detour 的指令
* 最后，将指向 `SBIELOW_DATA` 区域的指针保存至 `INJECT_DATA` 区域顶部，函数退出

如果为 wow64，则由 `InitInjectWow64` 以类似方式为 wow64 ntdll.dll 中的 32 位版本设置 hook。

##### RtlFindActivationContextSectionString 绕过

与上述其他环节不同，`RtlFindActivationContextSectionString` 分流函数是在目标进程相应的位数模式下执行的。

* 首先恢复 `RtlFindActivationContextSectionString` 原始代码段
* 然后加载 kernel32.dll，随后加载 SbieDll.dll 并获取 Ordinal 1 的地址
* 保存第一个参数的值到 `INJECT_DATA` 结构，并将其替换为指向结构体的指针
* 最终跳转到 Ordinal 1 所指地址（用 jump 而非 call，以便返回时能直接回到当前调用者）

## 有效负载（SbieDll.dll）操作机制

SbieDll.dll hook 入口点 `Dll_Ordinal1` 首先从作为第一个参数传入的 `INJECT_DATA` 结构体中获取所需的几个值，如 `SBIELOW_DATA` 数据块地址和原始的第一个参数值。获取完所需值后，会释放已无用的 `INJECT_DATA`（原为 `syscall_data` 区域）。
此后，函数判断 `bHostInject` 是否为 0。如果为 0，则调用 `SbieDll!Dll_InitInjected`，该函数 hook 几乎所有内容，最后调用 `SbieDll!Ldr_Init`，该函数设置 dll 加载的回调并调用 `SbieDll!Ldr_Inject_Init`。如果 `bHostInject != 0`，则 `SbieDll!Ldr_Inject_Init` 由 `Dll_Ordinal1` 直接调用。初始化完成后，`Dll_Ordinal1` 使用原始参数调用并返回真实的 `RtlFindActivationContextSectionString`。

此外，为实现进一步的 hook，`SbieDll!Ldr_Inject_Init` 还会 hook 启动进程的实际入口点。此函数会保存入口点的初始字节，并覆盖为跳转至 `SbieDll!Ldr_Inject_Entry64` 或 `SbieDll!Ldr_Inject_Entry32`（分别用于 64 位和 32 位）。这两个函数由汇编实现，将返回地址指针传递给 `SbieDll!Ldr_Inject_Entry` 作为参数并清理堆栈，随后回到入口点起始处。

##### Ldr_Inject_Entry

该函数首先通过 `SbieDll!Ldr_Inject_SaveBytes` 恢复原入口点函数的初始内容，并将调用者返回地址改为指向入口点起始处，这样一旦返回即可正式执行真实入口点。然后函数判断 `bHostInject` 是否为 0，若为 0，则先调用 `SbieDll!Ldr_LoadInjectDlls`，然后调用 `SbieDll!Dll_InitExeEntry` 完成最后的初始化步骤。若 `bHostInject != 0`，则仅调用 `SbieDll!Ldr_LoadInjectDlls`，该函数会检查 [Sandboxie.ini](SandboxieIni.md) 的 [InjectDll](InjectDll.md) 或 [InjectDll64](InjectDll64.md) 配置项，如配置有其他需要加载的 dll，则一并加载。
