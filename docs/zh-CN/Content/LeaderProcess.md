# 领导进程

_LeaderProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定在沙盒中被视为主要程序的名称，当这些程序停止运行时，沙盒中的所有其他程序也会停止。例如：
```
   .
   .
   .
   [DefaultBox]
   LeaderProcess=iexplore.exe
```

_iexplore.exe_ 是 Internet Explorer。

相关的 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒设置 -> 程序停止 -> 领导程序](ProgramStopSettings.md#leader-programs)

另见：[程序设置](ProgramSettings.md#leader)。 