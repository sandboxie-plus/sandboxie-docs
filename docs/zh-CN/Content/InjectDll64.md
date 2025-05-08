# 注入64位DLL

_InjectDll_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它告诉 Sandboxie 将某些 DLL "注入"到沙盒中的每个程序中。"注入"意味着 DLL 是
```
   .
   .
   .
   [DefaultBox]
   InjectDll64=c:\Program Files\Sandboxie Utilities\Sample64.dll
```

您应该指定 DLL 的完整路径。如果 DLL 文件本身位于沙盒内，请指定沙盒内的完整路径。

**注意：** InjectDll64 设置指定 64 位 DLL，在 32 位进程中将忽略，即使在 64 位 Windows 上也是如此。使用 [InjectDll](InjectDll.md) 设置来指定 32 位 DLL。

另请参见：[InjectDll](InjectDll.md) 以获取全面的讨论。 