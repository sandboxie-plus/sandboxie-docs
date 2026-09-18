# 只读文件路径

_ReadFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径的文件不应用沙盒化，且不允许写入。

可以指定 [个人文件夹](ShellFolders.md)。可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   ReadFilePath=C:\WINDOWS
```

此示例强制 C:\WINDOWS 文件夹及其下所有内容对沙盒化程序只读，不可写入（或删除）。

注意：_ReadFilePath_ 是 [开放文件路径](OpenFilePath.md) 的限制形式。与 _OpenFilePath_ 一样，指定文件或文件夹位置中任何已存在的沙盒化内容都会被忽略。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 只读访问](ResourceAccessSettings.md#文件访问-只读访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 只读
