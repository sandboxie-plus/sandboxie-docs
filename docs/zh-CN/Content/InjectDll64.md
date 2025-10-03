# 注入 Dll64

_InjectDll_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于让沙盘向沙箱内的每个程序“注入”指定的 DLL。“注入”表示 DLL 会被加载到相应进程中。
```ini
   .
   .
   .
   [DefaultBox]
   InjectDll64=c:\Program Files\Sandboxie Utilities\Sample64.dll
```

您应当指定 DLL 的完整路径。如果 DLL 文件本身位于沙箱内，请指定沙箱内部的完整路径。

**注意：** 注入 Dll64 设置用于指定 64 位 DLL，并且即使在 64 位 Windows 上，该设置在 32 位进程中也会被忽略。要指定 32 位 DLL，请使用 [注入 32 位 Dll](InjectDll.md) 设置。

另请参阅：[注入 Dll](InjectDll.md) 获取详细讨论。