# 警报文件夹

_AlertFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中自 v0.5.0 / 5.45.0 版本起提供的全局设置。它指定的路径模式，如果在沙箱外部启动，会导致 Sandboxie 发出 [SBIE1301](SBIE1301.md) 警告信息。

用法:
```
.
.
.
[GlobalSettings]
AlertFolder=%ProgramFiles%\Mozilla Firefox
```

相关的 Sandboxie Plus 设置：选项菜单 > 全局设置 > 程序控制 > 程序警报


另请参阅：[警报进程](AlertProcess.md)
