# 直接磁盘访问时通知

_NotifyDirectDiskAccess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。通常指定为 _NotifyDirectDiskAccess=y_。

用法：
```
   .
   .
   .
   [DefaultBox]
   NotifyDirectDiskAccess=y
```

注意：Sandboxie 的默认行为是拒绝所有直接访问请求，除非通过 [开放文件路径](OpenFilePath.md) 或 [开放管道路径](OpenPipePath.md) 设置显式授予对硬盘设备的直接访问。通常，此类访问被拒绝时不会发出消息。

此设置无法使用 [沙盒管理器](SandboxieControl.md) 更改，必须在 [Sandboxie Ini](SandboxieIni.md) 中编辑。
