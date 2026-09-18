# 强制禁用等待秒数

_ForceDisableSeconds_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。它指定 [禁用强制程序](FileMenu.md#禁用强制程序) 模式保持生效的时间（秒）。

用法：
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableSeconds=25
   ForceDisableSeconds=0
```

此设置的默认值是 10 秒。把值设为零实际上会禁用_禁用强制程序_功能本身。另请参阅：[仅限管理员强制禁用](ForceDisableAdminOnly.md)。

_禁用强制程序_模式通过 [沙盒管理器](SandboxieControl.md) 启动，后者也可以配置秒数。使用 [文件菜单 > 禁用强制程序](FileMenu.md#禁用强制程序) 命令，或 [托盘图标菜单](TrayIconMenu.md) 中的同一命令。

生效时，_禁用强制程序_模式会让 Sandboxie 在强制程序被启动时发出 [SBIE1301](SBIE1301.md) 消息。
