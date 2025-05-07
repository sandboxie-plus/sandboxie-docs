# 隐藏沙盘进程

HideSbieProcesses 是 [沙盘配置文件](SandboxieIni.md) 中的一个设置。

```
   .
   .
   .
   [DefaultBox]
   HideSbieProcesses=y
```
使用 'HideSbieProcesses=y' 选项来隐藏沙盘工作进程（SbieSvc、SandboxieRpcSs 等）。

相关的 [沙盘配置文件](SandboxieIni.md) 设置：[HideHostProcess](HideHostProcess.md)、[HideNonSystemProcesses](HideNonSystemProcesses.md)
