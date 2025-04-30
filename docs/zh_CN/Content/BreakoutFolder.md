# 分离文件夹

_BreakoutFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置项，自 v1.0.8 / 5.55.8 版本起提供。它强制指定文件夹内的内容，即使在沙箱内启动，也以非沙箱方式运行。

用法如下：

```
   .
   .
   .
   [DefaultBox]
   BreakoutFolder=C:\Downloads
   BreakoutFolder=E:\
   BreakoutFolder=C:\App\*
   BreakoutFolder=C:\App?
   BreakoutFolder=C:\?pp\*
```

第一个示例指定 “C:\Downloads” 文件夹中的任何内容都将以非沙箱方式启动。

如第二个示例所示，也可以指定整个驱动器。

第三行和第四行展示了基本的通配符用法。

- `*` 表示 App 文件夹下的任意子文件夹（如 App\1，App\1\1 等）。
- `?` 表示文件夹名中的任意单个字符（如 Appa，App8 等），但不包括子文件夹。

此外，你可以组合多个通配符来匹配指定文件夹名及其子文件夹。

注意事项：
 * 指向非指定文件夹之外程序的快捷方式，仍会以沙箱方式启动。例如：如果你将快捷方式放在已设置的分离文件夹内，但其目标程序位于未被设置分离文件夹的位置，则该快捷方式将以沙箱方式启动。

有关分离程序启动的详细信息，请参阅 [分离进程](BreakoutProcess.md)。

另请参考 [强制文件夹](ForceFolder.md)，该设置与本功能相对，用于强制文件夹内内容以沙箱方式启动。
