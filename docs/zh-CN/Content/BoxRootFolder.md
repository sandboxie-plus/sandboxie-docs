# 沙盒根文件夹

**此设置已过时。请改用 [FileRootPath](FileRootPath.md)。**

_BoxRootFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。它指定包含所有沙盒的文件夹。在容器文件夹中，会为每个正在使用的沙盒创建一个子文件夹。

在 Sandboxie 3.0 及更高版本中，[FileRootPath](FileRootPath.md) 设置是指定沙盒位置的首选方式，如果两个设置同时存在，FileRootPath 将优先于 BoxRootFolder。请注意，与任何其他沙盒设置一样，[FileRootPath](FileRootPath.md) 可以出现在 _GlobalSettings_ 部分，在这种情况下，它适用于所有沙盒。

更多信息请参见[沙盒层次结构](SandboxHierarchy.md)。

用法：

```
   .
   .
   .
   [GlobalSettings]
   BoxRootFolder=C:\Sandbox
```

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒菜单 > 设置容器文件夹](SandboxMenu.md#set-container-folder) 