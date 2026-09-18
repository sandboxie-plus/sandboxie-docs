# 注入 Dll

_InjectDll_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它告诉 Sandboxie 把某个 DLL“注入”到沙盒中的每个程序。“注入”意味着该 DLL 会被加载到进程中，例如：
```
   .
   .
   .
   [DefaultBox]
   InjectDll=c:\Program Files\Sandboxie Utilities\Sample.dll
```

你应该指定 DLL 的完整路径。如果 DLL 文件本身位于沙盒内，请指定沙盒内的完整路径。

**注意：** 注入 Dll 设置指定 32 位 DLL，在 64 位 Windows 上的 64 位进程中将忽略它。使用 [注入 Dll64](InjectDll64.md) 设置指定 64 位 DLL。

* * *

加载到沙盒化程序中的 DLL 顺序如下：

*   Ntdll.dll
*   KernelBase.dll（Windows 7 及更高版本）
*   Kernel32.dll
*   SbieDll.dll（在 64 位 Windows 上，可以是 64 位或 32 位 SbieDll）
*   _InjectDlls_（按 Sandboxie.ini 中指定的顺序加载）
*   可选地，ShimEng（或 Windows 7 及更高版本上的 AppHelp）及相关 DLL
*   所有 [静态链接](https://msdn.microsoft.com/en-us/library/ms684184(VS.85).aspx)的 DLL

上述行为适用于 Sandboxie 3.46 及更高版本。早期版本实现了下面描述的不同行为：

注入的 DLL 会在所有静态链接的 DLL 加载并初始化之后、程序本身开始在其入口点执行之前，被加载到沙盒化进程（或程序）中。

* * *

如果 DLL 导出符号 **InjectDllMain** 或 **InjectDllMain@8**，Sandboxie 将在 DLL 加载后调用此过程，并传入 SbieDll 模块的地址。在你的代码中声明 InjectDllMain：
```
   __declspec(dllexport) void __stdcall InjectDllMain(
      HINSTANCE hSbieDll, ULONG_PTR UnusedParameter);
```

建议使用 **hSbieDll** 参数作为 SbieDll.Dll 的模块实例句柄，而不是依赖 GetModuleHandle("SbieDll.dll")。这使得注入的 DLL 无论 SbieDll.dll 实际使用什么名称，都能与之交互。不过，使用 LoadLibrary 或 GetModuleHandle 按名称查找 SbieDll 也是可以的。

* * *

目前，此设置无法从 [沙盒管理器](SandboxieControl.md) 操作。你必须手动把它编辑进 [Sandboxie Ini](SandboxieIni.md)。

另请参阅：[注入 Dll64](InjectDll64.md)、[SBIE DLL API](SBIEDLLAPI.md)、[启动命令行](StartCommandLine.md)。
