# 窗口驻留豁免

_LingerExemptWnds_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.13.4 / 5.68.4 起可用。用于让残留进程监视机制不再豁免带窗口的残留进程被终止。例如：

```
   .
   .
   .
   [DefaultBox]
   LingerExemptWnds=n
```

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 程序停止 > 残留程序](ProgramStopSettings.md#残留程序)

另请参阅：[程序设置](ProgramSettings.md#linger)。
