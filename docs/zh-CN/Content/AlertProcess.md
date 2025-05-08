# 警告进程

_AlertProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。它指定了程序名称，如果在沙盒外启动这些程序，Sandboxie 将发出 [SBIE1301](SBIE1301.md) 消息。

用法：
```
   .
   .
   .
   [GlobalSettings]
   AlertProcess=iexplore.exe
   AlertProcess=firefox.exe
```

相关 [Sandboxie Control](SandboxieControl.md) 设置：
* [程序设置](ProgramSettings.md)
* [配置菜单 > 警告程序](ConfigureMenu.md#program-alerts)

相关 Sandboxie Plus 设置：
* 选项菜单 > 全局设置 > 程序控制 > 程序警告

另请参阅：[警告文件夹](AlertFolder.md)。 