# 沙箱根文件夹

**此设置已弃用。请改用 [文件根路径](FileRootPath.md)。**

_BoxRootFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个全局设置。它用于指定包含所有沙箱的文件夹。系统会在该容器文件夹内为每一个正在使用的沙箱创建一个子文件夹。

在 Sandboxie 3 及更高版本中，[文件根路径](FileRootPath.md) 是指定沙箱位置的首选方式。如果这两个设置同时存在，文件根路径 设置的优先级高于 沙箱根文件夹 设置。请注意，与任何其他沙箱设置一样，[文件根路径](FileRootPath.md) 也可以出现在 _GlobalSettings_ 部分，此时它将适用于所有沙箱。

如需了解更多信息，请参阅 [沙箱层级结构](SandboxHierarchy.md)。

用法示例：

```
   .
   .
   .
   [GlobalSettings]
   BoxRootFolder=C:\Sandbox
```

相关 [沙箱控制](SandboxieControl.md) 设置：请参考 [沙箱菜单 > 设置容器文件夹](SandboxMenu.md#set-container-folder)
