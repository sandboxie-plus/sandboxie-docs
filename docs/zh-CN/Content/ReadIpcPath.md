# 读取 IPC 路径

_ReadIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.0.16 / 5.55.16 起可用。它指定路径模式，Sandboxie 对这些路径允许读取非沙盒化进程或其他沙盒中进程的访问。这让沙盒化程序可以访问由沙盒外运行的程序提供的资源和服务。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   ReadIpcPath=$:program.exe
```

此示例允许沙盒内运行的程序读取访问在沙盒外运行或位于其他沙盒中的目标进程的地址空间。目标进程的进程名必须匹配设置中指定的名称。

也可以完全恢复旧行为，通过指定：
```
   .
   .
   .
   [DefaultBox]
   ReadIpcPath=$:*
```

默认情况下，唯一可读取其内存的进程是 _explorer.exe_。许多进程需要它，而且 Windows 文件资源管理器反正不应保留任何秘密。要阻止这一点，你可以使用：
```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=$:explorer.exe
```

相关 Sandboxie Plus 设置：

沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 只读

沙盒选项 > 常规选项 > 限制 > 其他限制 > 允许读取非沙盒化进程的内存（不推荐）
