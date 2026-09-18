# 隐藏宿主进程

_HideHostProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.3 / 5.42 起可用。它用于隐藏非沙盒化的宿主进程。也可用于隐藏 Sandboxie 服务。

```
   .
   .
   .
   [DefaultBox]
   HideHostProcess=program.exe
```

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐藏进程
