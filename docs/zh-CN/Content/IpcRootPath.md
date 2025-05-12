# IPC 根目录

_IpcRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定在 NT 对象命名空间内创建特定沙箱的位置。

和所有沙箱设置一样，该设置也可以在全局部分指定，此时将在未在沙箱部分单独指定该设置的所有沙箱中生效。

更多信息请参见 [沙箱层级结构](SandboxHierarchy.md)。

用法示例：
```
   .
   .
   .
   [DefaultBox]
   IpcRootPath=\Sandbox\%BOXNAME%
```

在该路径中，以下替换变量可能会用到：

*   变量 %SANDBOX%：展开为沙箱的名称
*   变量 %USER%：展开为用户名
*   变量 %SID%：展开为用户的安全 ID（SID）
*   变量 %SESSION%：展开为终端服务会话号

如果未指定 IPC 根目录，其默认值为：

*   _\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%_

通常没有理由更改该设置的默认值，并且不建议更改。