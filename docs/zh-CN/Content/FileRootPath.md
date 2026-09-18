# 文件根路径

_FileRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定特定沙盒的根文件夹。

与所有沙盒设置一样，它也可以出现在全局节中，此时它适用于所有未在沙盒节中另行指定该设置的沙盒。

更多信息参见 [沙盒层级](SandboxHierarchy.md)。

用法：

```
   .
   .
   .
   [DefaultBox]
   FileRootPath=C:\Sandbox\MySandbox
```

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒菜单 > 设置容器文件夹](SandboxMenu.md#设置容器文件夹)

相关 Sandboxie Plus 设置：选项菜单 > 全局设置 > 高级配置 > Sandboxie 配置 > 沙盒文件系统根目录

**技术细节**

以下替换变量在此路径中可能有用。

*   [个人文件夹](ShellFolders.md) 变量，如 %Personal%，展开为用户"文档"文件夹
*   变量 %SBIEHOME%，展开为 Sandboxie 安装根目录
*   变量 %SANDBOX%，展开为沙盒名称
*   变量 %USER%，展开为用户名称
*   变量 %SID%，展开为用户安全 ID（SID）
*   变量 %SESSION%，展开为终端服务会话编号

如果未指定 _FileRootPath_，则使用_已弃用的_[沙盒根文件夹](BoxRootFolder.md) 设置构造其默认值，即：

*   `BoxRootFolder\Sandbox\%SANDBOX%`

如果也未指定 _BoxRootFolder_，则默认设置为：

*   `C:\Sandbox\%USER%\%SANDBOX%`
