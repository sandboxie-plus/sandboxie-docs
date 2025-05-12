# Linger Exempt Wnds

_LingerExemptWnds_ 是自 v1.13.4 / 5.68.4 起在 [Sandboxie Ini](SandboxieIni.md) 中提供的一个沙箱设置。该设置用于让挂起进程监控机制，不再因为进程拥有窗口句柄而将其从终止列表豁免。例如：

```
   .
   .
   .
   [DefaultBox]
   LingerExemptWnds=n
```

相关的 [沙盘控制](SandboxieControl.md) 设置：[沙盘设置 -> 程序控制 -> 停止行为 -> 驻留进程](ProgramStopSettings.md#lingering-programs)

另请参阅：[程序设置](ProgramSettings.md#linger)。