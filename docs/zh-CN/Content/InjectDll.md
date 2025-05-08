# 注入 DLL

_InjectDll_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它告诉 Sandboxie 将某个 DLL "注入"到沙盒中的每个程序中。"注入"意味着该 DLL 将被加载到程序中。
```
   .
   .
   .
   [DefaultBox]
   InjectDll=c:\Program Files\Sandboxie Utilities\Sample.dll
```

您应该指定 DLL 的完整路径。如果 DLL 文件本身位于沙盒内，请指定沙盒内的完整路径。

**注意：** InjectDll 设置指定 32 位 DLL，在 64 位 Windows 的 64 位进程中将被忽略。使用 [InjectDll64](InjectDll64.md) 设置来指定 64 位 DLL。

* * *

DLL 加载到沙盒化程序的顺序如下：

* Ntdll.dll
* KernelBase.dll（在 Windows 7 及更高版本上）
* Kernel32.dll
* SbieDll.dll（在 64 位 Windows 上，这可以是 64 位 SbieDll 或 32 位 SbieDll）
* _InjectDlls_（按照 Sandboxie.ini 中指定的顺序加载）
* 可选的 ShimEng（或在 Windows 7 及更高版本上的 AppHelp）和相关 DLL
* 所有[静态链接](https://msdn.microsoft.com/en-us/library/ms684184(VS.85).aspx)的 DLL

上述行为适用于 Sandboxie 3.46 及更高版本。早期版本的 Sandboxie 实现了不同的行为，如下所述：

注入的 DLL 在所有静态链接的 DLL 加载和初始化之后，但在程序本身开始在其入口点执行之前，被加载到沙盒化进程（或程序）中。

* * *

如果 DLL 导出符号 **InjectDllMain** 或 **InjectDllMain@8**，Sandboxie 将在 DLL 加载后调用此过程，并传递 SbieDll 模块的地址。在您的代码中声明 InjectDllMain：
```
   __declspec(dllexport) void __stdcall InjectDllMain(
      HINSTANCE hSbieDll, ULONG_PTR UnusedParameter);
```

建议使用 **hSbieDll** 参数作为 SbieDll.Dll 的模块实例句柄，而不是依赖于 GetModuleHandle("SbieDll.dll")。这使得注入的 DLL 可以与 SbieDll.dll 交互，而不管 SbieDll.dll 实际使用的名称是什么。但是，使用 LoadLibrary 或 GetModuleHandle 通过名称查找 SbieDll 也是可以的。

* * *

目前，此设置无法从 [Sandboxie 控制](SandboxieControl.md) 进行操作。您必须手动将其编辑到 [Sandboxie Ini](SandboxieIni.md) 中。

另见：[InjectDll64](InjectDll64.md)、[SBIE DLL API](SBIEDLLAPI.md)、[启动命令行](StartCommandLine.md)。 