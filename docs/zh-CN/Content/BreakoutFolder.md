# 分离文件夹

_BreakoutFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.0.8 / 5.55.8 起可用。它强制文件夹内容以非沙盒化方式运行，即使是从沙盒内启动的。

用法：

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

第一个示例指定 "C:\Downloads" 文件夹中的任何内容都将以非沙盒化方式启动。

也可以指定整个驱动器，如第二个示例所示。

第三和第四行展示了通配符的基本字符。

- `*` 表示 App 文件夹之后的任何子文件夹（App\1、App\1\1 等）。
- `?` 表示文件夹名称中的单个字符（Appa、App8 等），但不包括子文件夹。

此外，你可以组合多个通配符来匹配指定的文件夹名称和子文件夹。

注意：
 * 指向指定文件夹之外程序的快捷方式将以沙盒化方式启动。例如：如果你把一个快捷方式放在已分离的文件夹内，而它链接到未分离文件夹中的某个程序，那么该快捷方式将以沙盒化方式启动。

关于分离程序的信息，请查看 [分离沙盒进程](BreakoutProcess.md)。

也请查看 [强制文件夹](ForceFolder.md)——本设置的对立面，它强制文件夹内容以沙盒化方式启动。
