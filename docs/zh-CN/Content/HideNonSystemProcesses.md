# 隐藏非系统进程

HideNonSystemProcesses 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。

```
   .
   .
   .
   [DefaultBox]
   HideNonSystemProcesses=y
```

使用 'HideNonSystemProcesses=y' 选项可以防止沙盒化进程看到在沙盒外运行的进程。

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐私 > 隐藏非系统进程

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[HideHostProcess](HideHostProcess.md)、[HideSbieProcesses](HideSbieProcesses.md) 