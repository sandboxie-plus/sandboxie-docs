# 开放管道路径

_OpenPipePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径的文件不应用沙盒化。

它与 [开放文件路径](OpenFilePath.md) 设置相同，区别在于此设置始终生效，而 _OpenFilePath_ 只在应用程序从位于沙盒外的文件或文件夹运行时才生效。

一般使用说明参见 [开放文件路径](OpenFilePath.md)。

_OpenPipePath_ 设置主要用于允许沙盒化程序访问文件通信设备资源，这些资源可以用 [Sandboxie 跟踪](SandboxieTrace.md) 识别。

不过，它也可以用来定义应被免除的文件和文件夹（以 _OpenFilePath_ 免除文件的方式），即使对从沙盒内部运行的程序也是如此。

用法示例：
```
   .
   .
   .
   [DefaultBox]
   OpenPipePath=\Device\NamedPipe\wkssvc
   OpenPipePath=\Device\NamedPipe\srvsvc
```

将允许沙盒化程序通过资源 _wkssvc_ 和 _srvsvc_ 管理计算机上的共享和用户帐户。

**注意：** 不建议使用此特定示例，因为它会削弱沙盒的保护。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 完全访问](ResourceAccessSettings.md#文件访问-完全访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 全部开放
