# 允许原始磁盘读取

_AllowRawDiskRead_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置，自 v0.7.0 / 5.48.0 版本起可用。该设置可用于禁用阻止提权的沙箱内程序读取卷/磁盘的保护措施。


```ini
.
.
.
[DefaultBox]
AllowRawDiskRead=y
```

相关 Sandboxie Plus 设置：沙箱选项 > 文件选项 > 允许提权的沙箱内程序读取硬盘
