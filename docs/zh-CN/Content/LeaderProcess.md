# 引导进程

_LeaderProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 配置文件中的一个沙盒设置。它用于指定在沙盒中被视为主要进程的程序名称。当这些程序退出时，沙盒中其他所有程序也会随之终止。例如：

```ini
   .
   .
   .
   [DefaultBox]
   LeaderProcess=iexplore.exe
```

_iexplore.exe_ 是 Internet Explorer。

相关的 [沙盒管理器](SandboxieControl.md) 设置项：[沙盒设置 -> 程序控制 -> 停止行为 -> 引导进程](ProgramStopSettings.md#主导程序)

另请参见：[程序设置](ProgramSettings.md#leader)。