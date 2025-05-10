# 注入 Dll

_InjectDll_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它指示沙盒向沙箱内的每个程序“注入”一个或多个 DLL。所谓“注入”，即 DLL 被加载至进程，例如：

```
   .
   .
   .
   [DefaultBox]
   InjectDll=c:\Program Files\Sandboxie Utilities\Sample.dll
```

你应当指定 DLL 的完整路径。如果 DLL 文件本身位于沙箱内，应指定沙箱内部的完整路径。

**注意：** InjectDll 设置是用于指定 32 位 DLL，并且在 64 位 Windows 的 64 位进程中会被忽略。要指定 64 位 DLL，请使用 [InjectDll64](InjectDll64.md) 设置。

* * *

加载到沙箱内程序的 DLL 顺序如下：

*   Ntdll.dll
*   KernelBase.dll（适用于 Windows 7 及更高版本）
*   Kernel32.dll
*   SbieDll.dll（在 64 位 Windows 中，可能为 64 位或 32 位 SbieDll）
*   _InjectDlls_（按 Sandboxie.ini 中指定的顺序加载）
*   （可选）ShimEng（或 Windows 7 及更高版本下的 AppHelp）及相关 DLL
*   所有[静态链接](https://msdn.microsoft.com/en-us/library/ms684184(VS.85).aspx)的 DLL

上述行为适用于 Sandboxie 3.46 及更高版本。早期版本的 Sandboxie 实现方式与此不同，具体如下：

被注入的 DLL 会在所有静态链接的 DLL 被加载并初始化完成后，但在程序实际在入口点（entry point）开始执行之前，注入到沙箱进程（或程序）中。

* * *

如果该 DLL 导出符号 **InjectDllMain** 或 **InjectDllMain@8**，沙盒会在 DLL 加载完成后调用此过程，并传递 SbieDll 模块的地址。可以如下方式在你的代码中声明 InjectDllMain：

```
   __declspec(dllexport) void __stdcall InjectDllMain(
      HINSTANCE hSbieDll, ULONG_PTR UnusedParameter);
```

建议使用 **hSbieDll** 参数作为 SbieDll.Dll 的模块句柄，而不是依赖 GetModuleHandle("SbieDll.dll")。这样，无论 SbieDll.dll 实际的文件名为何，注入 DLL 都能与 SbieDll.dll 正确交互。当然，也可以通过 LoadLibrary 或 GetModuleHandle 使用名称查找 SbieDll。

* * *

目前，该设置无法通过 [沙盒控制](SandboxieControl.md) 进行操作。你需要手动在 [Sandboxie Ini](SandboxieIni.md) 中编辑此项。

参见：[注入 Dll64](InjectDll64.md)、[沙盒 DLL API](SBIEDLLAPI.md)、[启动命令行](StartCommandLine.md)。