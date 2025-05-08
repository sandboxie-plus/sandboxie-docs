# 警告文件夹

_AlertFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置，自 v0.5.0 / 5.45.0 版本起可用。它指定了路径模式，如果在沙盒外启动这些路径，Sandboxie 将发出 [SBIE1301](SBIE1301.md) 消息。

用法：
```
   .
   .
   .
   [GlobalSettings]
   AlertFolder=%ProgramFiles%\Mozilla Firefox
```

相关 Sandboxie Plus 设置：选项菜单 > 全局设置 > 程序控制 > 程序警告

另请参阅：[警告进程](AlertProcess.md)。 