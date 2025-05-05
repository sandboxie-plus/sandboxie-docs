# 分离沙箱进程

_BreakoutProcess_ 是 [沙盘配置文件](SandboxieIni.md) 中的一项沙箱设置，自 v1.0.8 / 5.55.8 版本起可用。它指定了在沙箱内启动时哪些应用程序应在沙箱外运行。结合使用此设置和 _ForceProcess_ 可以实现一个简单的优先级系统。

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

- `*` 表示 Program 之后的任意名称（例如 Program0Test1.exe、Program5Test92G.exe 等）。
- `?` 表示名称中的任意一个字符（例如 Program1.exe、Programg.exe 等）。

此外，您可以组合使用多个通配符来匹配指定的名称。

指定 _ProgramName_ 表示应在沙箱外启动的应用程序。或者，也可以指定程序的路径。

优先级系统：
如果您设置某个程序从一个沙箱中分离出来，并强制它在另一个沙箱中运行，这就形成了一个有用的优先级系统。

示例：
假设您使用浏览器作为 PDF 查看器，并且有两个沙箱 “Browser” 和 “Email”。假设您通过电子邮件收到了一个 PDF 文件，并且希望该 PDF 文件在相应的 “Browser” 沙箱中打开一个浏览器标签，而不是在当前的 “Email” 沙箱中打开。您可以在 “Email” 沙箱中设置浏览器可分离沙箱运行，并在 “Browser” 沙箱中强制它运行。

更多信息请查看 [强制进程](ForceProcess.md)。

