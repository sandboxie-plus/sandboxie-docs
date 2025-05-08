# 关闭的文件路径

_ClosedFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置。它指定了 Sandboxie 将拒绝沙盒程序进行 _所有_ 访问（包括 _读取_ 访问）的路径模式。此设置实际上阻止沙盒程序访问特定的文件和文件夹。

可以指定 [Shell 文件夹](ShellFolders.md)。可以指定 [程序名称前缀](ProgramNamePrefix.md)。

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

第一个示例阻止除 Internet Explorer (_iexplore.exe_) 之外的任何程序访问包含活动用户账户下载的 Internet cookie 的文件夹。这将阻止任何下载的恶意软件窥探 cookie。

（请注意，这并不会阻止浏览器扩展（如附加工具栏）查看 Cookies 文件夹，因为这些扩展在 Internet Explorer 程序进程内执行。）

第二个示例展示了如何配置 Sandboxie 以阻止沙盒程序访问 _文档_ 文件夹。

为 ClosedFilePath 指定的值可以包含通配符。有关此内容的更多信息，包括展示通配符使用的示例，请参见 [开放文件路径](OpenFilePath.md)。

第三个示例（跨越四行）禁用沙盒内的 Internet 访问，_除了_ Internet Explorer (_iexplore.exe_)。另请参见 [沙盒设置 > 限制 > Internet 访问](RestrictionsSettings.md#internet-access)。

**注意：** 与相应的 OpenFilePath 设置不同，_ClosedFilePath_ 设置始终适用于沙盒程序，无论程序可执行文件是位于沙盒内还是沙盒外。

相关的 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 阻止访问](ResourceAccessSettings.md#file-access--blocked-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 关闭 