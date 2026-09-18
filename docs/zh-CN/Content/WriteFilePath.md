# 只写文件路径

只写文件路径是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径隐藏沙盒外的任何文件或文件夹，同时允许在沙盒中创建新文件和文件夹。

可以指定 [个人文件夹](ShellFolders.md)。可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   WriteFilePath=%Cookies%
```

此示例表示：沙盒中的程序将无法看到沙盒外 Internet Explorer Cookie 文件夹中的任何文件，但可以在沙盒中的相应文件夹中创建文件。换句话说，沙盒外现有的 Cookie 将不可见，但程序可以像 Cookie 文件夹为空一样创建新 Cookie。

此设置不适用于文件。如果设置中指定的路径匹配某个文件，该文件将被视作匹配封闭文件路径设置。

注意：只写文件路径在内部实现为 [封闭文件路径](ClosedFilePath.md) 的增强形式。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 只写访问](ResourceAccessSettings.md#文件访问-只写访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 仅盒内（只写）
