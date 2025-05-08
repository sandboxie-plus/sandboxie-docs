# 开放配置路径

_OpenConfPath_ 是自 v1.0.0 / 5.55.0 版本起在 [Sandboxie Ini](SandboxieIni.md) 中可用的沙盒设置。它指定一个路径模式，Sandboxie 将不会对注册表键应用沙盒化。这允许沙盒化程序直接访问更新_沙盒外_的系统设置。此设置本质上在沙盒的特定注册表键位置_打了一个洞_。

它与 [OpenKeyPath](OpenKeyPath.md) 设置相同，不同之处在于此设置始终应用，而 _OpenKeyPath_ 仅在应用程序从位于沙盒外的文件或文件夹运行时才应用。

可以指定[程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenConfPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenConfPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

这些示例允许 Firefox 程序 _firefox.exe_ 直接访问 Mozilla 注册表键树（包括系统范围和每用户注册表树）。

为 _OpenConfPath_ 指定的值可以包含通配符，尽管对于注册表键来说，很少需要使用通配符。有关这方面的更多信息，包括显示使用通配符的示例，请参见 [OpenFilePath](OpenFilePath.md)。（_OpenFilePath_ 处理文件而不是注册表键，但使用通配符的原则是相同的。）

**注意：** 即使程序可执行文件位于沙盒内，此设置也会应用。这意味着下载到您的计算机并执行的（潜在恶意）软件可以利用此设置。

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表键 > 访问列 > 对所有程序开放 