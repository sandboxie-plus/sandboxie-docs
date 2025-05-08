# IPC 根路径

_IpcRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定了在 NT 对象命名空间中创建特定沙盒的位置。

与所有沙盒设置一样，它也可以在全局部分中指定，在这种情况下，它将适用于在沙盒部分中未指定该设置的所有沙盒。

有关更多信息，请参见[沙盒层次结构](SandboxHierarchy.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   IpcRootPath=\Sandbox\%BOXNAME%
```

在此路径中可以使用以下替换变量：

*   %SANDBOX% 变量，展开为沙盒的名称
*   %USER% 变量，展开为用户名
*   %SID% 变量，展开为用户安全标识符（SID）
*   %SESSION% 变量，展开为终端服务会话号

如果未指定 IpcRootPath，其默认值为：

*   _\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%_

可能没有理由更改此设置的默认值，不建议这样做。 