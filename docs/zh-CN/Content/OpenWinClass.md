# 开放窗口类

_OpenWinClass_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定非沙盒化窗口的类名，这些窗口应可供沙盒化程序访问。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenWinClass=ConsoleWindowClass
   OpenWinClass=$:program.exe/IgnoreUIPI
   OpenWinClass=#
   OpenWinClass=*
```

第一个示例让由 _cmd.exe_ 进程创建的控制台窗口可供沙盒化程序访问。

通常，Sandboxie 不允许沙盒化程序访问、通信、关闭或销毁沙盒外的窗口。_OpenWinClass_ 设置对此规则做出例外，允许特定的非沙盒化窗口可被访问。

**特殊形式**
```
   OpenWinClass=$:program.exe/IgnoreUIPI
```

这允许沙盒内运行的程序使用 PostThreadMessage API，把消息直接发送到沙盒外运行的某个目标进程中的线程。此形式的 _OpenWinClass_ 设置不支持通配符，因此目标进程的进程名必须匹配设置中指定的名称。
```
   OpenWinClass=#
```

此设置告诉 Sandboxie 不更改由沙盒化程序创建的窗口类名。通常，Sandboxie 会把 _IEFrame_ 之类的类名转换为 _Sandbox:DefaultBox::IEFrame_，以便更好地把属于沙盒化程序的窗口与系统中的其他窗口分开。

然而，在某些情况下，沙盒外的程序可能期望窗口类名是特定名称，因此可能无法识别沙盒化程序创建的窗口。指定 OpenWinClass=# 可以解决此问题，代价是分离程度较低。

注意：OpenWinClass=# 不允许与沙盒外的任何窗口通信，并可能干扰某些拖放操作。
```
   OpenWinClass=*
```

此设置告诉 Sandboxie 不按上述方式转换窗口类名，同时让沙盒化程序可以访问系统中的所有窗口，并且更进一步，禁用其他几个与窗口相关的 Sandboxie 功能。这也可能导致 Sandboxie 指示符 [#] 不显示在窗口标题中。

注意：OpenWinClass=* 允许与沙盒外的所有窗口完全通信，但可能干扰某些拖放操作。

**识别窗口类名**

非沙盒化窗口通过其_窗口类名_来识别，窗口类名是创建窗口的应用程序赋予窗口的内部名称。你可以使用 [WinSpy](https://www.catch22.net/software/winspy) 之类的工具识别窗口类名。Sandboxie 经典版中的 [资源访问监视器](ResourceAccessMonitor.md) 工具和 Sandboxie Plus 中的 [跟踪日志](../PlusContent/TraceLog.md) 工具也会显示窗口类名。

相关 Sandboxie Plus 设置：

沙盒选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 开放

沙盒选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 忽略 UIPI

沙盒选项 > 资源访问 > 窗口 > 不更改由沙盒化程序创建的窗口类名

另请参阅：[不重命名窗口类](NoRenameWinClass.md)。
