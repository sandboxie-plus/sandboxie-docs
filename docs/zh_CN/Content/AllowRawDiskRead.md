# 允许原始磁盘读取

_AllowRawDiskRead_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置，自 v0.7.0 / 5.48.0 版本起可用。该设置可用于禁用阻止提升权限的沙盒进程读取卷/磁盘的保护措施


```
   .
   .
   .
   [DefaultBox]
   AllowRawDiskRead=y
```

相关 Sandboxie Plus 设置：沙盒选项 > 文件选项 > 允许提升权限的沙盒应用程序读取硬盘
