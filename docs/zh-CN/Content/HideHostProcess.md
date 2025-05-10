# 隐藏主机进程

_HideHostProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置，自 v0.3 / 5.42 版本起可用。它用于隐藏未在沙箱中运行的主机进程，也可以用于隐藏沙盒服务。

```
   .
   .
   .
   [DefaultBox]
   HideHostProcess=program.exe
```

相关沙盒 Plus 设置：沙箱选项 > 高级选项 > 进程 > 隐藏进程