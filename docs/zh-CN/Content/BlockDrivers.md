# 阻止驱动程序

**此功能已在 SBIE 版本 4.+ 及更高版本中移除。它不再可用。**

_BlockDrivers_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否应该允许沙盒化程序将驱动程序加载到操作系统中。但是，此设置_不_控制新驱动程序的_安装_ -- 详见下文。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockDrivers=n
```

指定 _n_ 表示允许沙盒化程序将驱动程序加载到操作系统中。如果不这样做，Sandboxie 将拒绝驱动程序加载尝试，并发出消息 [SBIE2103](SBIE2103.md)。

**注意：** 不建议禁用 BlockDrivers 提供的保护。

**驱动程序安装**

在加载驱动程序之前，必须先安装它。驱动程序安装不受 BlockDrivers 设置的影响。要允许驱动程序安装，您应该添加以下 OpenKeyPath 设置：

```
OpenKeyPath=HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
```

此外，您还应该使用 OpenFilePath _打开_驱动程序文件。这是必需的，因为在注册表中设置的驱动程序路径（在 CurrentControlSet\Services 下创建的键中）通常不会指向沙盒内。

```
OpenFilePath=c:\program files\MyNewSoftware\SoftwareDriver.sys
```

**注意：** 不建议允许沙盒化程序安装驱动程序。

相关 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed) 