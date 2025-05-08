# 文件根路径

_FileRootPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定特定沙盒的根文件夹。

与所有沙盒设置一样，它也可以在全局部分中指定，在这种情况下，它将适用于在沙盒部分中未指定该设置的所有沙盒。

有关更多信息，请参见[沙盒层次结构](SandboxHierarchy.md)。

用法：

```
   .
   .
   .
   [DefaultBox]
   FileRootPath=C:\Sandbox\MySandbox
```

相关 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒菜单 > 设置容器文件夹](SandboxMenu.md#set-container-folder)

相关 Sandboxie Plus 设置：选项菜单 > 全局设置 > 高级配置 > Sandboxie 配置 > 沙盒文件系统根目录

**技术细节**

以下替换变量可能在此路径中很有用：

* [Shell 文件夹](ShellFolders.md) 变量，如 %Personal%，它扩展为用户文档文件夹
* 变量 %SBIEHOME%，它扩展为 Sandboxie 安装的根目录
* 变量 %SANDBOX%，它扩展为沙盒的名称
* 变量 %USER%，它扩展为用户名
* 变量 %SID%，它扩展为用户安全 ID (SID)
* 变量 %SESSION%，它扩展为终端服务会话编号

如果未指定 _FileRootPath_，则其默认值使用_已弃用_的 [BoxRootFolder](BoxRootFolder.md) 设置构建，如下所示：

* `BoxRootFolder\Sandbox\%SANDBOX%`

如果也未指定 _BoxRootFolder_，则默认设置为：

* `C:\Sandbox\%USER%\%SANDBOX%` 