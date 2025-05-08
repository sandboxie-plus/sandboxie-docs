# 突破进程限制

_BreakoutProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置，自 v1.0.8 / 5.55.8 版本起可用。它指定在沙盒内启动时应在沙盒外运行的应用程序。将此设置与 _ForceProcess_ 结合使用可以实现一个简单的优先级系统。

用法：

```
   .
   .
   .
   [DefaultBox]
   BreakoutProcess=ProgramName.exe
   BreakoutProcess=Program*.exe
   BreakoutProcess=Program?.exe
   BreakoutProcess=Pro?ram*.exe
```

- `*` 定义 Program 之后的任何名称（Program0Test1.exe、Program5Test92G.exe 等）。
- `?` 定义名称中的一个字符（Program1.exe、Programg.exe 等）。

此外，您可以组合多个通配符来匹配指定的名称。

指定 _ProgramName_ 表示应该在沙盒外启动的应用程序。或者，也可以指定程序的路径。

优先级系统：
如果您设置一个程序在一个沙盒中突破限制，而在另一个沙盒中强制运行，这就形成了一个有用的优先级系统。

示例：
假设您使用浏览器作为 PDF 查看器，并有两个沙盒"浏览器"和"电子邮件"。假设您通过电子邮件收到了一个 PDF 文件，并希望在相应的"浏览器"沙盒中打开浏览器标签页，而不是在当前（"电子邮件"）沙盒中打开。您可以在"电子邮件"沙盒中突破浏览器 exe 的限制，并在"浏览器"沙盒中强制运行它。

更多信息请查看 [ForceProcess](ForceProcess.md)。 