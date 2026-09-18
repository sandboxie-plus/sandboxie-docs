# IPC 根目录

_IpcRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定特定沙盒在 NT 对象命名空间内被创建的位置。

与所有沙盒设置一样，它也可以出现在全局节中，此时它适用于所有未在沙盒节中另行指定该设置的沙盒。

更多信息参见 [沙盒层级](SandboxHierarchy.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   IpcRootPath=\Sandbox\%BOXNAME%
```

以下替换变量在此路径中可能有用。

*   变量 %SANDBOX%，展开为沙盒名称
*   变量 %USER%，展开为用户名称
*   变量 %SID%，展开为用户安全 ID（SID）
*   变量 %SESSION%，展开为终端服务会话编号

如果未指定 IPC 根目录，其默认值为：

*   _\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%_

可能没有理由更改此设置的默认值，也不建议这样做。
