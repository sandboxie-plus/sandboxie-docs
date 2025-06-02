# 强制禁用等待秒数

_ForceDisableSeconds_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置项。它用于指定 [禁用强制程序](FileMenu.md#disable-forced-programs) 模式保持生效的时间（以秒为单位）。

用法如下：
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableSeconds=25
   ForceDisableSeconds=0
```

该设置项的默认值为 10 秒。如果将其设置为零，则实际上会禁用 _禁用强制程序_ 功能。另请参阅：[ForceDisableAdminOnly](ForceDisableAdminOnly.md)。

_禁用强制程序_ 模式可通过 [沙盘控制](SandboxieControl.md) 启用，该界面也可配置生效的时间秒数。请使用 [文件菜单 > 禁用强制程序](FileMenu.md#disable-forced-programs) 命令，或通过 [托盘图标菜单](TrayIconMenu.md) 执行相同命令。

当该模式处于活动状态时，每当启动强制进程时，沙盘会发出消息 [SBIE1301](SBIE1301.md)。