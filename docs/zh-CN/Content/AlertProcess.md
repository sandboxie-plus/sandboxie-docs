# 警报进程

_AlertProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个全局设置。它用于指定某些程序的名称，如果这些程序在沙箱之外启动， Sandboxie 会发出 [SBIE1301](SBIE1301.md) 警告消息。

用法:
```
   .
   .
   .
   [GlobalSettings]
   AlertProcess=iexplore.exe
   AlertProcess=firefox.exe
```

相关 [沙箱控制](SandboxieControl.md) 设置：
* [程序设置](ProgramSettings.md)
* [配置菜单 > 程序警报](ConfigureMenu.md#program-alerts)

相关 Sandboxie Plus 设置：
* 选项菜单 > 全局设置 > 程序控制 > 程序警报

另请参阅：[警报文件夹](AlertFolder.md)
