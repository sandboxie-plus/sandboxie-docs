# 沙盒根文件夹

**此设置已弃用。请改用 [文件根路径](FileRootPath.md)。**

_BoxRootFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。它指定包含所有沙盒的文件夹。每个正在使用的沙盒都会在容器文件夹内创建一个子文件夹。

在 Sandboxie 3 及更高版本中，[文件根路径](FileRootPath.md) 设置是指定沙盒位置的首选方式，并且如果两个设置都存在，文件根路径优先于沙盒根文件夹。注意：与任何其他沙盒设置一样，[文件根路径](FileRootPath.md) 可以出现在 _GlobalSettings_ 节中，此时它适用于所有沙盒。

更多信息参见 [沙盒层级](SandboxHierarchy.md)。

用法：

```
   .
   .
   .
   [GlobalSettings]
   BoxRootFolder=C:\Sandbox
```

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒菜单 > 设置容器文件夹](SandboxMenu.md#设置容器文件夹)
