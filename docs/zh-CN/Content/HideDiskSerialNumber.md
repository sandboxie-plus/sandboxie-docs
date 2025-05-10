# 隐藏磁盘序列号

**隐藏磁盘序列号（HideDiskSerialNumber）** 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。

```
   .
   .
   .
   [DefaultBox]
   HideDiskSerialNumber=y
```

使用 `HideDiskSerialNumber=y` 选项后，当应用程序尝试获取磁盘序列号时，将返回一个随机值。

相关的 Sandboxie Plus 设置路径：沙箱选项 > 高级选项 > 隐私 > 隐藏磁盘序列号