# 只读文件路径

_ReadFilePath_ 是 [沙箱配置文件](SandboxieIni.md) 中的一个沙箱设置。它指定路径模式，使得相匹配的文件不会应用 Sandboxie 的沙箱化限制（即允许访问），同时也不允许写入操作。

可以指定 [Shell 文件夹](ShellFolders.md)，也可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   ReadFilePath=C:\WINDOWS
```

此示例强制规定，C:\WINDOWS 文件夹及其所有子文件夹对于沙箱内的程序是可读的，但不可写入（或删除）。

注意：_ReadFilePath_ 是 [OpenFilePath](OpenFilePath.md) 的一种受限形式。与 _OpenFilePath_ 一样，对于指定文件或文件夹位置中已存在的沙箱内容将被忽略。

相关的 [Sandboxie 控制面板](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > 文件访问 > 只读访问](ResourceAccessSettings.md#file-access--read-only-access)

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 只读

