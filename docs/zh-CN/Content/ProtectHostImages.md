# 保护主机镜像

_ProtectHostImages_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.9.0 / 5.64.0 版本起可用。启用此设置后，可防止沙盒外部的进程加载沙盒内的 DLL 文件。

```ini
   .
   .
   .
   [DefaultBox]
   ProtectHostImages=y
```

对应的 Sandboxie Plus 设置路径：沙盒选项 > 各种选项 > DLL 和扩展 > 防止主机上安装的沙盒程序从沙盒加载 DLL
