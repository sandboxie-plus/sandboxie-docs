# 写入键路径

写入键路径（WriteKeyPath）是 [沙箱ie配置文件（Sandboxie Ini）](SandboxieIni.md) 中的一项沙箱设置。它指定了一些路径模式，对于这些模式，沙箱ie会隐藏沙箱外部的任何注册表项，同时允许在沙箱内创建新的注册表项和注册表值。

可以指定 [程序名称前缀（Program Name Prefix）](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   WriteKeyPath=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

此示例会隐藏沙箱外部 _TypedPaths_ 注册表项中存在的任何数据，同时允许程序在沙箱内对应的 _TypedPaths_ 注册表项中创建新的键和值。这意味着在沙箱中运行的 Windows 资源管理器将无法显示在沙箱外部的 Windows 资源管理器中输入的路径历史记录。但在沙箱中运行的 Windows 资源管理器将能够记录和存储新输入的路径。

注意：_写入键路径（WriteKeyPath）_ 在内部实现为 [封闭键路径（ClosedKeyPath）](ClosedKeyPath.md) 的增强形式。

相关的 [沙箱ie控制（Sandboxie Control）](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > 注册表访问 > 只写访问](ResourceAccessSettings.md#registry-access--write-only-access)

相关的沙箱ie Plus 设置：沙箱选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 仅沙箱内（只写）
