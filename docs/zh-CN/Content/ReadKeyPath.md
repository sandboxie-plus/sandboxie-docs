# 读取注册表项路径

_ReadKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径的注册表项不应用沙盒化，且不允许写入。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   ReadKeyPath=HKEY_LOCAL_MACHINE\SOFTWARE\Policies
```

此示例强制 _Policies_ 项及其下所有内容对沙盒化程序只读，不可写入（或删除）。

注意：_ReadKeyPath_ 是 [开放注册表路径](OpenKeyPath.md) 的限制形式。与 _OpenKeyPath_ 一样，指定文件或文件夹位置中任何已存在的沙盒化内容都会被忽略。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 注册表访问 > 只读访问](ResourceAccessSettings.md#注册表访问-只读访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 只读
