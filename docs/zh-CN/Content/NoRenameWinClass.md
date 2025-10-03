# 不重命名窗口类

_NoRenameWinClass_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。该选项用于指定不应被沙盘重命名的窗口类名。

用法示例：
```ini
   .
   .
   .
   [DefaultBox]
   NoRenameWinClass=ExampleWinClass
   NoRenameWinClass=program.exe,*
```

第一个设置指示沙盘不要重命名 _ExampleWinClass_ 窗口类名，从而允许沙箱内的程序直接访问该窗口类名，同时会进一步禁用与窗口相关的部分沙箱功能。这样可能会导致窗口标题栏不再显示沙盘指示符 [#]。

第二个设置指示沙盘不要重命名 _program.exe_ 程序创建的窗口类名，从而允许沙箱内的程序直接访问这些窗口类名，同时会进一步禁用与窗口相关的部分沙箱功能。这样也可能导致窗口标题栏不再显示沙盘指示符 [#]。

相关的 Sandboxie Plus 设置：沙盘选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 禁止重命名