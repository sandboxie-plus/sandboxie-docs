# 突破文件夹限制

_BreakoutFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置，自 v1.0.8 / 5.55.8 版本起可用。它强制文件夹内的内容在沙盒外运行，即使是从沙盒内启动的。

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

第一个示例指定"C:\Downloads"文件夹内的任何内容都将在沙盒外启动。

如第二个示例所示，也可以指定整个驱动器。

第三行和第四行展示了通配符的基本字符。

- `*` 定义 App 文件夹之后的任何子文件夹（App\1、App\1\1 等）。
- `?` 定义文件夹中的单个字符（Appa、App8 等），但不包括子文件夹。

此外，您可以组合多个通配符来匹配指定的文件夹名称和子文件夹。

注意：
 * 指向指定文件夹外程序的快捷方式将在沙盒内启动。例如：如果您在突破限制的文件夹内放置一个快捷方式，而它链接到非突破限制文件夹中的某个程序，那么该快捷方式将在沙盒内启动。

有关突破程序限制的信息，请查看 [突破进程限制](BreakoutProcess.md)。

另请查看 [强制文件夹](ForceFolder.md)，这是此设置的对应设置，它强制文件夹内容在沙盒内启动。 