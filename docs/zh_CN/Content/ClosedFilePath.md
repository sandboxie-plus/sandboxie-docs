# 封闭文件路径

_ClosedFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置项。它用于指定路径模式，对于这些路径，Sandboxie 会拒绝沙箱内程序的 _所有_ 访问权限，包括 _读取_ 权限。该设置本质上阻止沙箱程序访问指定的文件和文件夹。

可以指定 [Shell 文件夹](ShellFolders.md)；也可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ClosedFilePath=!iexplore.exe,%Cookies%
   ClosedFilePath=%Personal%
```

```
   ClosedFilePath=!iexplore.exe,\Device\RawIp
   ClosedFilePath=!iexplore.exe,\Device\Ip*
   ClosedFilePath=!iexplore.exe,\Device\Tcp*
   ClosedFilePath=!iexplore.exe,\Device\Afd*
```

上述第一个示例表示阻止除了 Internet Explorer（_iexplore.exe_）之外的任何程序访问当前用户账户下存放下载的 Internet Cookie 的文件夹。这样可以阻止任何下载的恶意软件窃取 Cookie。

（注意，这并不能阻止诸如附加工具栏之类的浏览器扩展程序访问 Cookies 文件夹，因为这些扩展是在 Internet Explorer 程序进程内执行的。）

第二个示例演示了如何配置 Sandboxie 阻止沙箱程序访问 _Documents_ 文件夹。

为 ClosedFilePath 指定的值可以包含通配符。有关这部分的详细信息，包括带有通配符用法的示例，请参阅 [开放文件路径](OpenFilePath.md)。

第三个示例（包含四行）配置了在沙箱内禁用 Internet 访问，_除了_ Internet Explorer（_iexplore.exe_）外均不允许访问。另请参见 [沙箱设置 > 限制 > 互联网访问](RestrictionsSettings.md#internet-access)。

**注意：** 与对应的 开放文件路径 设置不同，_ClosedFilePath_ 设置始终对沙箱程序生效，无论程序的可执行文件是在沙箱内还是沙箱外。

相关 [Sandboxie 控制](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > 文件访问 > 封禁访问](ResourceAccessSettings.md#file-access--blocked-access)

相关 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 封禁
