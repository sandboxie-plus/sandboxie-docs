# 阻止驱动程序

**此功能已在 SBIE 4.0 及更高版本中移除，不再可用。**

_BlockDrivers_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否应允许沙盒化程序向操作系统加载驱动程序。不过，此设置_不_控制新驱动程序的_安装_——详见下文。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockDrivers=n
```

指定 _n_ 表示允许沙盒化程序向操作系统加载驱动程序。如果不这样设置，Sandboxie 会拒绝驱动程序加载尝试，并发出 [SBIE2103](SBIE2103.md) 消息。

**注意：** 不建议禁用阻止驱动程序所提供的保护。

**驱动程序安装**

驱动程序在被加载之前，必须先被安装。驱动程序安装不受阻止驱动程序设置影响。要允许驱动程序安装，你应该添加以下开放注册表路径设置：

```
OpenKeyPath=HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
```

并且你还应该使用开放文件路径 _开放_该驱动程序文件。这是必需的，因为将在注册表（在 CurrentControlSet\Services 之下创建的项中）设置的驱动程序路径，通常不会指向沙盒内部。

```
OpenFilePath=c:\program files\MyNewSoftware\SoftwareDriver.sys
```

**注意：** 不建议允许沙盒化程序安装驱动程序。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#低级访问-已移除)
