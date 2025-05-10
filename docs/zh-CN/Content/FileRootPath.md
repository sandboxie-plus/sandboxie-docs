# 文件根路径

_FileRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定特定沙箱的根文件夹。

与所有沙箱设置一样，该项也可以在全局部分进行指定。在此情况下，对于所有未在沙箱部分单独指定该项的沙箱，该配置将适用。

更多信息请参见 [沙箱层次结构](SandboxHierarchy.md)。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   FileRootPath=C:\Sandbox\MySandbox
```

相关的 [沙盒控制](SandboxieControl.md) 设置：[沙盒菜单 > 设置容器文件夹](SandboxMenu.md#set-container-folder)

相关的 Sandboxie Plus 设置：选项菜单 > 全局设置 > 高级配置 > Sandboxie 配置 > 沙箱文件系统根目录

**技术细节**

下列替换变量在此路径中可能会有用：

*   [Shell Folders](ShellFolders.md) 变量，例如 %Personal%，其会展开为用户的文档文件夹
*   变量 %SBIEHOME%，其会展开为 Sandboxie 安装的根目录
*   变量 %SANDBOX%，其会展开为沙箱的名称
*   变量 %USER%，其会展开为用户名
*   变量 %SID%，其会展开为用户的安全标识（SID）
*   变量 %SESSION%，其会展开为终端服务会话号

如果未指定 _FileRootPath_，其默认值将通过已弃用的 [BoxRootFolder](BoxRootFolder.md) 设置构造，如下所示：

*   `BoxRootFolder\Sandbox\%SANDBOX%`

如果也未指定 _BoxRootFolder_，则默认设置为：

*   `C:\Sandbox\%USER%\%SANDBOX%`