# 写入注册表项路径

写入注册表项路径是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径隐藏沙盒外的任何注册表项，同时允许在沙盒中创建新的注册表项和注册表值。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   WriteKeyPath=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

此示例隐藏 _TypedPaths_ 注册表项中沙盒外存在的任何数据，同时允许程序在沙盒中相应的 _TypedPaths_ 注册表项内创建新的项和值。这意味着在沙盒中运行的 Windows 资源管理器将无法显示沙盒外曾在 Windows 资源管理器中输入过的路径历史。但在沙盒中运行的 Windows 资源管理器可以记录并存储新输入的路径。

注意：_WriteKeyPath_ 在内部实现为 [封禁注册表项路径](ClosedKeyPath.md) 的增强形式。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 注册表访问 > 只写访问](ResourceAccessSettings.md#注册表访问-只写访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 仅盒内（只写）
