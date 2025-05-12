# 隐藏其他沙箱

_HideOtherBoxes_ 是自 v0.3 / 5.42 起在 [Sandboxie Ini](SandboxieIni.md) 中可用的一个沙箱设置。默认情况下，沙盘会启用此功能，从而使进程在其他沙箱中被隐藏。禁用此设置的示例如下：

```
   .
   .
   .
   [DefaultBox]
   HideOtherBoxes=n
```

相关的 Sandboxie Plus 设置：沙箱选项 > 高级选项 > 进程 > 不允许沙箱内的进程查看其它沙箱里运行的进程