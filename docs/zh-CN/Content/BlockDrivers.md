# BlockDrivers

**此功能已在 SBIE 4.+ 及以上版本中被移除，不再可用**

_BlockDrivers_ 是 [Sandboxie Ini](SandboxieIni.md) 配置文件中的一个沙箱设置。它用于指定 Sandboxie 是否允许沙箱内的程序向操作系统加载驱动程序。但需要注意的是，该设置 _并不_ 控制新驱动程序的_安装_——详情请参见下文。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BlockDrivers=n
```

指定 _n_ 表示允许沙箱内程序向操作系统加载驱动程序。如果没有这样设置，Sandboxie 将拒绝加载驱动的操作，并显示 [SBIE2103](SBIE2103.md) 消息。

**注意：** 不建议禁用 BlockDrivers 所提供的安全保护。

**驱动程序安装**

在加载驱动程序之前，必须先完成其安装。驱动程序的安装不会受到 BlockDrivers 设置的影响。如需允许驱动程序安装，应添加如下 OpenKeyPath 设置：

```
OpenKeyPath=HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
```

此外，还应通过 OpenFilePath _开放_ 驱动文件。这是因为注册表中（在 CurrentControlSet\Services 下新建的键中）设置的驱动路径通常不会指向沙箱内部。

```
OpenFilePath=c:\program files\MyNewSoftware\SoftwareDriver.sys
```

**注意：** 不建议允许沙箱内的程序安装驱动程序。

相关的 [沙箱控制](SandboxieControl.md) 设置： [沙箱设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed)
