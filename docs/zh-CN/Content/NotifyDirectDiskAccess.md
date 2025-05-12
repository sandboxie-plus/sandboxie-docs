# 直接磁盘访问时通知

_NotifyDirectDiskAccess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。通常写作 _NotifyDirectDiskAccess=y_。

用法如下：
```
   .
   .
   .
   [DefaultBox]
   NotifyDirectDiskAccess=y
```

请注意，沙箱的默认行为是拒绝所有直接访问请求，除非通过 [开放文件路径](OpenFilePath.md) 或 [打开管道路径](OpenPipePath.md) 设置为硬盘设备显式授予直接访问权限。通常，在此类访问被拒绝时不会发出提示消息。

该设置无法通过 [沙盘控制](SandboxieControl.md) 更改，必须在 [Sandboxie Ini](SandboxieIni.md) 中手动编辑。