# 开放管道路径

_OpenPipePath_ 是 [沙箱配置文件（Sandboxie Ini）](SandboxieIni.md) 中的一个沙箱设置项。它用于指定一系列路径模式，使得对于这些模式所匹配的文件（夹），沙箱软件（Sandboxie）不会对其执行沙箱化隔离（也就是允许沙箱访问的意思）。

它与 [OpenFilePath](OpenFilePath.md) 设置类似，不同之处在于该设置始终生效，而 _OpenFilePath_ 仅在当应用程序从沙箱外部的文件或文件夹运行时生效。

关于一般使用方法，请参考 [OpenFilePath](OpenFilePath.md)。

_OpenPipePath_ 设置主要用于允许沙箱内的程序访问文件通信设备资源，这些资源可以通过 [沙箱跟踪（Sandboxie Trace）](SandboxieTrace.md) 进行识别。

另外，它也可以用来定义应该被豁免的文件和文件夹（就像 _OpenFilePath_ 豁免文件的方式一样），即使这些程序是从沙盒内部运行的。

示例用法：
```
   .
   .
   .
   [DefaultBox]
   OpenPipePath=\Device\NamedPipe\wkssvc
   OpenPipePath=\Device\NamedPipe\srvsvc
```

这将允许沙箱内的程序通过 _wkssvc_ 和 _srvsvc_ 这两个资源来管理计算机上的共享和用户账户。

**注意：** 请不要将本示例纳入实际使用，因为它会削弱沙箱的保护能力。

相关的 [Sandboxie 经典版控制面板（Sandboxie Control）](SandboxieControl.md) 设置： [沙箱设置 > 资源访问 > 文件访问 > 完全开放](ResourceAccessSettings.md#file-access--full-access)

相关的 Sandboxie Plus 设置： 沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 完全开放