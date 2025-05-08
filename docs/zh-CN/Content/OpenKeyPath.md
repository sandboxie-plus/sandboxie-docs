# 开放注册表键路径

_OpenKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 不会对其应用沙盒化的注册表键路径模式。这允许沙盒化程序直接访问更新_沙盒外_的系统设置。此设置本质上在特定注册表键位置_打了一个洞_。

它与 [OpenConfPath](OpenConfPath.md) 设置相同，只是此设置仅在应用程序从沙盒外的文件或文件夹运行时才应用，而 _OpenConfPath_ 始终应用。

可以指定[程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenKeyPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenKeyPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

这些示例允许 Firefox 程序 _firefox.exe_ 直接访问 Mozilla 注册表键树（包括系统范围和每用户注册表树）。

为 _OpenKeyPath_ 指定的值可以包含通配符，尽管对于注册表键来说，很少需要使用通配符。有关这方面的更多信息，包括显示使用通配符的示例，请参见 [OpenFilePath](OpenFilePath.md)。（_OpenFilePath_ 处理文件而不是注册表键，但使用通配符的原则是相同的。）

**注意：** 出于安全原因，当程序可执行文件位于沙盒内时，此设置不适用。这意味着下载到您的计算机并执行的（潜在恶意）软件无法利用此设置。

相关的 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 注册表访问 > 直接访问](ResourceAccessSettings.md#registry-access--direct-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表键 > 访问列 > 开放 