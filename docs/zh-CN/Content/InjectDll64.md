# 注入 Dll64

_InjectDll_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它告诉 Sandboxie 把某个 DLL“注入”到沙盒中的每个程序。“注入”意味着该 DLL 会被加载到进程中，例如：
```
   .
   .
   .
   [DefaultBox]
   InjectDll64=c:\Program Files\Sandboxie Utilities\Sample64.dll
```

你应该指定 DLL 的完整路径。如果 DLL 文件本身位于沙盒内，请指定沙盒内的完整路径。

**注意：** 注入 Dll64 设置指定 64 位 DLL，即使在 64 位 Windows 上，在 32 位进程中也会被忽略。使用 [注入 Dll](InjectDll.md) 设置指定 32 位 DLL。

全面讨论另请参阅：[注入 Dll](InjectDll.md)。
