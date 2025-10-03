# 隐藏非系统进程

隐藏非系统进程是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。

```ini
   .
   .
   .
   [DefaultBox]
   HideNonSystemProcesses=y
```

使用 `HideNonSystemProcesses=y` 选项可以防止沙箱中的进程看到运行在沙箱外部的进程。

相关的 Sandboxie Plus 设置：沙箱选项 > 高级选项 > 进程 > 不允许沙箱内的进程查看任何沙箱外运行的进程

相关的 [Sandboxie Ini](SandboxieIni.md) 设置：[隐藏主机进程](HideHostProcess.md)，[隐藏沙盘进程](HideSbieProcesses.md)