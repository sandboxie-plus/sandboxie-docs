# 隐藏非系统进程

“隐藏非系统进程”（HideNonSystemProcesses）是[沙盘配置文件](SandboxieIni.md)中的一个设置。

```
   .
   .
   .
   [DefaultBox]
   HideNonSystemProcesses=y
```

使用 'HideNonSystemProcesses=y' 选项可防止沙箱内的进程看到沙箱外运行的进程。

相关的沙盘增强版设置：沙箱选项 > 高级选项 > 隐私 > 隐藏非系统进程

相关的[沙盘配置文件](SandboxieIni.md)设置：[隐藏主机进程](HideHostProcess.md)，[隐藏沙盘进程](HideSbieProcesses.md)
