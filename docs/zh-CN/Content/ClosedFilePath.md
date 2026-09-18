# 封闭文件路径

_ClosedFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 拒绝沙盒化程序对这些路径的_所有_访问，包括_读取_访问。本质上，此设置阻止沙盒化程序访问这些文件和文件夹。

可以指定 [个人文件夹](ShellFolders.md)。可以指定 [程序名称前缀](ProgramNamePrefix.md)。

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

第一个示例阻止 Internet Explorer（_iexplore.exe_）_以外_的任何程序访问当前用户帐户存放下载的 Internet Cookie 的文件夹。这将阻止任何下载的恶意软件窥探 Cookie。

（注意：这并不能阻止浏览器扩展（如附加工具栏）查看 Cookie 文件夹，因为这些扩展在 Internet Explorer 程序进程内执行。）

第二个示例展示如何配置 Sandboxie，阻止沙盒化程序访问_文档_文件夹。

封闭文件路径指定的值可以包含通配符。更多信息（包括展示通配符用法的示例）参见 [开放文件路径](OpenFilePath.md)。

第三个示例（跨四行）禁用沙盒内的互联网访问，Internet Explorer（_iexplore.exe_）_除外_。另请参阅 [沙盒设置 > 限制 > 互联网访问](RestrictionsSettings.md#互联网访问)。

**注意：** 与对应的开放文件路径设置不同，_ClosedFilePath_ 设置始终适用于沙盒化程序，无论程序可执行文件位于沙盒内还是沙盒外。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 阻止访问](ResourceAccessSettings.md#文件访问-阻止访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 封闭
