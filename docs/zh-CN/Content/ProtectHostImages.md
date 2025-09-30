# 保护主机镜像

_ProtectHostImages_ 是 [沙盘配置文件](SandboxieIni.md) 中的一项沙箱设置，自 v1.9.0 / 5.64.0 版本起可用。启用此设置后，可防止沙箱外部的进程加载沙箱内的 DLL 文件。

```ini
   .
   .
   .
   [DefaultBox]
   ProtectHostImages=y
```

对应的沙盘增强版（Sandboxie Plus）设置路径：沙箱选项 > 各种选项 > DLL 和扩展 > 防止主机上安装的沙箱程序从沙箱加载 DLL
