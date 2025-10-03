# 开放注册表路径

_OpenKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定一个路径模式，沙盘不会对该路径下的注册表键应用沙箱隔离，从而允许受沙箱保护的程序直接访问并更新 _沙箱外部_ 的系统设置。此设置本质上是在特定的注册表键位置为沙箱“打了一个洞”。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```ini
   .
   .
   .
   [DefaultBox]
   OpenKeyPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenKeyPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

上述示例允许 Firefox 程序（firefox.exe）可以直接访问 Mozilla 的注册表键树（包括系统范围和当前用户范围的注册表树）。

_OpenKeyPath_ 的取值支持通配符，虽然对于注册表键，通常很少需要使用通配符。关于更多信息，包括使用通配符的示例，请参考 [OpenFilePath](OpenFilePath.md)。(_OpenFilePath_ 针对的是文件，而不是注册表键，但通配符的使用原理是相同的。)

**注意：**出于安全原因，当程序可执行文件位于沙箱内部时，此设置不会生效。这意味着在你的计算机上下载并运行的（潜在恶意的）软件无法利用该设置。

相关的 [沙盘控制](SandboxieControl.md) 设置： [沙箱设置 > 资源访问 > 注册表访问 > 直接访问](ResourceAccessSettings.md#registry-access--direct-access)

相关的 Sandboxie Plus 设置： 沙箱选项 > 资源访问 > 注册表 > 添加注册表键 > 访问列 > 开放