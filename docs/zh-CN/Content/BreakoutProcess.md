# 分离沙盒进程

_BreakoutProcess_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.0.8 / 5.55.8 起可用。它指定哪些应用程序在沙盒内启动时应以非沙盒化方式运行。它和 _ForceProcess_ 的组合可以实现简单的优先级系统。

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

- `*` 表示 Program 之后的任意名称（Program0Test1.exe、Program5Test92G.exe 等）。
- `?` 表示名称中的一个字符（Program1.exe、Programg.exe 等）。

此外，你可以组合多个通配符来匹配指定名称。

指定 _ProgramName_ 表示该应用程序应以非沙盒化方式启动。也可以指定程序的路径。

优先级系统：
如果你让某个程序从沙盒中分离，同时又强制它沙盒化到另一个沙盒中，这就构成一个有用的优先级系统。

示例：
假设你把浏览器当作 PDF 查看器使用，并有 "Browser" 和 "Email" 两个沙盒。假设你通过电子邮件收到一个 PDF，你希望 PDF 在相应的 "Browser" 沙盒中启动一个浏览器标签页，而不是在当前（"Email"）沙盒中。你可以在 "Email" 沙盒中分离浏览器 exe，并在 "Browser" 沙盒中强制它。

更多信息请查看 [强制进程](ForceProcess.md)。
