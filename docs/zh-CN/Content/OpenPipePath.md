# 开放管道路径

_OpenPipePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定某些路径模式，使得沙盘不会对这些文件应用沙箱隔离。

它与 [开放文件路径](OpenFilePath.md) 设置类似，不同之处在于该设置始终生效，而 _OpenFilePath_ 仅在应用程序从沙箱外部的文件或文件夹运行时生效。

关于一般使用方法，请参考 [开放文件路径](OpenFilePath.md)。

_OpenPipePath_ 设置主要用于允许沙箱内的程序访问文件通信设备资源，这些资源可以通过 [沙盘跟踪](SandboxieTrace.md) 进行识别。

此外，它也可用于为即使在沙箱中运行的程序定义需要豁免（以 _OpenFilePath_ 的方式豁免）的文件和文件夹。

示例用法：
```
   .
   .
   .
   [DefaultBox]
   OpenPipePath=\Device\NamedPipe\wkssvc
   OpenPipePath=\Device\NamedPipe\srvsvc
```

将允许沙箱内的程序通过 _wkssvc_ 和 _srvsvc_ 这两个资源来管理计算机上的共享和用户账户

**注意：** 不建议使用此具体示例，因为它会削弱沙箱的保护能力

相关的 [沙盘控制](SandboxieControl.md) 设置： [沙箱设置 > 资源访问 > 文件访问 > 完全开放](ResourceAccessSettings.md#file-access--full-access)

相关的 Sandboxie Plus 设置： 沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 完全开放