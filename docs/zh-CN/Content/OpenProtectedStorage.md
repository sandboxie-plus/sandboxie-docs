#  开放受保护的存储

_OpenProtectedStorage_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。通常被指定为 _OpenProtectedStorage=y_（参见 [是或否设置](YesOrNoSettings.md)），表示沙盘不应隔离沙箱内的 [受保护存储](ProtectedStorage.md)。例如：
```
   .
   .
   .
   [DefaultBox]
   OpenProtectedStorage=y
```

这表示，在 `DefaultBox` 沙箱内运行的程序将会更新全局系统 [受保护存储](ProtectedStorage.md)，而不是更新沙箱中的受保护存储实例

相关的 Sandboxie Plus 设置： 沙箱选项 > 应用模板 > 模板 > 打开受保护存储

相关的 [沙盘控制](SandboxieControl.md) 设置：[沙箱设置 > 应用程序 > 网页浏览器](ApplicationsSettings.md#web-browser) 中的 _沙箱外保存：搜索字符串历史记录和调用的命令_