# 隐藏其他沙盒

_HideOtherBoxes_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置，自 v0.3 / 5.42 版本起可用。默认情况下，Sandboxie 启用此功能，它允许进程对其他沙盒隐藏。禁用此设置的示例：

```
   .
   .
   .
   [DefaultBox]
   HideOtherBoxes=n
```

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐藏进程 > 不允许沙盒化进程查看在其他沙盒中运行的进程 