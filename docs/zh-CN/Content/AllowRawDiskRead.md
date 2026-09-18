# 允许原始磁盘读取

_AllowRawDiskRead_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.7.0 / 5.48.0 起可用。此设置可用于禁用阻止提升的沙盒化进程为读取目的访问卷/磁盘的保护。

```
   .
   .
   .
   [DefaultBox]
   AllowRawDiskRead=y
```

相关 Sandboxie Plus 设置：沙盒选项 > 文件选项 > 允许提升的沙盒化应用程序读取硬盘
