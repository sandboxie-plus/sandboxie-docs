# 不重命名窗口类

_NoRenameWinClass_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定不应由 Sandboxie 转换的窗口类名。

用法：
```
   .
   .
   .
   [DefaultBox]
   NoRenameWinClass=ExampleWinClass
   NoRenameWinClass=program.exe,*
```

第一个设置告诉 Sandboxie：让 _ExampleWinClass_ 窗口类名可供沙盒化程序访问，从而不转换它，并且更进一步，禁用其他几个与窗口相关的 Sandboxie 功能。这也可能导致 Sandboxie 指示符 [#] 不显示在窗口标题中。

第二个设置告诉 Sandboxie：让 _program.exe_ 创建的窗口类名可供沙盒化程序访问，从而不转换它们，并且更进一步，禁用其他几个与窗口相关的 Sandboxie 功能。这也可能导致 Sandboxie 指示符 [#] 不显示在窗口标题中。

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 不重命名
