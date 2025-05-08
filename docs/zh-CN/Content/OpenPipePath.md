# 开放管道路径

_OpenPipePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 不会对其应用沙盒化的文件路径模式。

它与 [OpenFilePath](OpenFilePath.md) 设置相同，不同之处在于此设置始终应用，而 _OpenFilePath_ 仅在应用程序从位于沙盒外的文件或文件夹运行时才应用。

有关一般使用说明，请参见 [OpenFilePath](OpenFilePath.md)。

_OpenPipePath_ 设置主要用于允许沙盒化程序访问文件通信设备资源，可以使用 [Sandboxie Trace](SandboxieTrace.md) 识别这些资源。

但是，它也可以用于定义应该豁免的文件和文件夹（就像 _OpenFilePath_ 豁免文件一样），即使对于从沙盒本身内部运行的程序也是如此。

使用示例：
```
   .
   .
   .
   [DefaultBox]
   OpenPipePath=\Device\NamedPipe\wkssvc
   OpenPipePath=\Device\NamedPipe\srvsvc
```

将允许沙盒化程序通过资源 _wkssvc_ 和 _srvsvc_ 管理计算机上的共享和用户账户。

**注意：** 不建议使用此特定示例，因为它会削弱沙盒的保护。

相关的 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 完全访问](ResourceAccessSettings.md#file-access--full-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 对所有程序开放 