# 读取注册表项路径

_读取注册表项路径_ 是 [沙盘配置文件（Sandboxie Ini）](SandboxieIni.md) 中的一项沙箱设置。它指定了注册表键的路径模式，对于这些路径，沙盘不会对注册表键应用沙箱处理，并且不允许写入操作。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   ReadKeyPath=HKEY_LOCAL_MACHINE\SOFTWARE\Policies
```

此示例强制使 _Policies_ 键及其以下的所有内容可被沙箱程序读取，但不可写入（或删除）。

注意：_读取注册表项路径_ 是 [打开注册表项路径](OpenKeyPath.md) 的一种受限形式。与 _打开注册表项路径_ 一样，指定文件或文件夹位置的任何已存在的沙箱内容将被忽略。

相关的 [沙盘控制面板](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > 注册表访问 > 只读访问](ResourceAccessSettings.md#registry-access--read-only-access)

相关的沙盘增强版（Sandboxie Plus）设置：沙箱选项 > 资源访问 > 注册表 > 添加注册表键 > 访问列 > 只读
