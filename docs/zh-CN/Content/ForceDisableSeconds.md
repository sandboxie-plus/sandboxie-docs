# 强制禁用秒数

_ForceDisableSeconds_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。它指定[禁用强制程序](FileMenu.md#disable-forced-programs)模式将保持生效的时间（以秒为单位）。

用法：
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableSeconds=25
   ForceDisableSeconds=0
```

此设置的默认值为 10 秒。将值设置为零实际上会禁用_禁用强制程序_功能本身。另见：[ForceDisableAdminOnly](ForceDisableAdminOnly.md)。

_禁用强制程序_模式通过 [Sandboxie 控制](SandboxieControl.md)启用，它也可以配置秒数。使用[文件菜单 > 禁用强制程序](FileMenu.md#disable-forced-programs)命令，或[托盘图标菜单](TrayIconMenu.md)中的相同命令。

当激活时，_禁用强制程序_模式会导致 Sandboxie 在启动强制程序时发出消息 [SBIE1301](SBIE1301.md)。 