# 隐藏主机进程

_HideHostProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置，自 v0.3 / 5.42 版本起可用。它用于隐藏未沙盒化的主机进程。它也可以用于隐藏 Sandboxie 服务。

```
   .
   .
   .
   [DefaultBox]
   HideHostProcess=program.exe
```

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐藏进程 