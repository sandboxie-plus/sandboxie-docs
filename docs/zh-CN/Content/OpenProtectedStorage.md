# 开放受保护的存储

_OpenProtectedStorage_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。通常指定为 _OpenProtectedStorage=y_（参见 [是/否设置](YesOrNoSettings.md)），表示 Sandboxie 不应在沙盒中隔离 [受保护的存储](ProtectedStorage.md)。例如：
```
   .
   .
   .
   [DefaultBox]
   OpenProtectedStorage=y
```

表示在 DefaultBox 沙盒中运行的程序将更新全局系统的 [受保护的存储](ProtectedStorage.md)，而不是其沙盒化实例。

相关 Sandboxie Plus 设置：沙盒选项 > 应用程序模板 > 模板 > 开放受保护的存储

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 应用程序 > Web 浏览器](ApplicationsSettings.md#web-浏览器) 中的 _在沙盒外保存：搜索字符串和已调用命令的历史记录_
