# 写入文件路径

WriteFilePath 是 [沙箱配置文件（Sandboxie Ini）](SandboxieIni.md) 中的一个沙箱设置项。它指定了一些路径模式，对于这些模式，沙箱软件（Sandboxie）会隐藏沙箱外部的所有文件或文件夹，同时允许在沙箱内创建新的文件和文件夹。

可以指定 [Shell 文件夹](ShellFolders.md)，也可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   WriteFilePath=%Cookies%
```

此示例意味着沙箱内的程序将无法看到沙箱外部 Internet Explorer 临时文件夹中的任何文件，但可以在沙箱内的相应文件夹中创建文件。换句话说，沙箱外部现有的临时文件将不可见，但程序可以创建新的临时文件，就好像临时文件夹是空的一样。

此设置不适用于文件。如果设置中指定的路径与某个文件匹配，则该文件将被视为与 [ClosedFilePath](ClosedFilePath.md) 设置匹配。

注意：WriteFilePath 在内部实现为 [ClosedFilePath](ClosedFilePath.md) 的增强形式。

相关的 [沙箱控制（Sandboxie Control）](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > 文件访问 > 只写访问](ResourceAccessSettings.md#file-access--write-only-access)

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 仅沙箱内（只写）
