# 开放配置路径

_OpenConfPath_ 是 [Sandboxie Ini](SandboxieIni.md) 配置文件中的一项沙箱设置，自 v1.0.0 / 5.55.0 版本起可用。它用于指定一个路径模式，对于该路径下的注册表项，沙盘将不会应用沙箱机制。这允许沙箱内的程序能够直接访问及修改 _沙箱外_ 的系统设置。该设置本质上是在指定的注册表项位置为沙箱“打了一个洞”。

它与 [开放注册表路径](OpenKeyPath.md) 设置类似，但不同之处在于，此设置始终生效，而 _OpenKeyPath_ 仅在应用程序从沙箱外的文件或文件夹运行时才会生效。

可指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```ini
   .
   .
   .
   [DefaultBox]
   OpenConfPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenConfPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

这些示例允许 Firefox 程序（_firefox.exe_）直接访问 Mozilla 相关注册表项（包括系统范围和每个用户的注册表路径）。

_OpenConfPath_ 的值可以包含通配符，尽管对于注册表项来说，通常很少需要使用通配符。有关此内容的更多信息，包括通配符使用示例，请参见 [OpenFilePath](OpenFilePath.md)。(_OpenFilePath_ 用于文件而非注册表项，但通配符的使用原理是一样的。)

**注意：** 即使程序可执行文件位于沙箱内，该设置依然有效。这意味着（潜在的恶意）软件下载到您的计算机并被执行后，仍可以利用该设置。

相关 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 完全开放