# 开放窗口类

_OpenWinClass_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定沙盒化程序可以访问的非沙盒化窗口的类名。

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

第一个示例使由 _cmd.exe_ 进程创建的控制台窗口可以被沙盒化程序访问。

通常，Sandboxie 不允许沙盒化程序访问、通信、关闭或销毁沙盒外的窗口。_OpenWinClass_ 设置对此规则做了例外，允许访问特定的非沙盒化窗口。

**特殊形式**
```
   OpenWinClass=$:program.exe/IgnoreUIPI
```

这允许在沙盒内运行的程序使用 PostThreadMessage API 直接向沙盒外运行的目标进程中的线程发送消息。这种形式的 _OpenWinClass_ 设置不支持通配符，因此目标进程的进程名称必须与设置中指定的名称匹配。
```
   OpenWinClass=#
```

此设置告诉 Sandboxie 不要更改由沙盒化程序创建的窗口类名。通常，Sandboxie 会将类名（如 _IEFrame_）转换为 _Sandbox:DefaultBox::IEFrame_，以便更好地将属于沙盒化程序的窗口与系统中的其他窗口分开。

但是，在某些情况下，沙盒外的程序可能期望窗口类名具有特定名称，因此可能无法识别由沙盒化程序创建的窗口。指定 OpenWinClass=# 可以解决此问题，但代价是分离程度较低。

请注意，OpenWinClass=# 不允许与沙盒外的任何窗口通信，并可能干扰某些拖放操作。
```
   OpenWinClass=*
```

此设置告诉 Sandboxie 不要如上所述转换窗口类名，并使系统中的所有窗口都可以被沙盒化程序访问，并进一步禁用一些其他与窗口相关的 Sandboxie 功能。这也可能导致 Sandboxie 指示器 [#] 不会出现在窗口标题中。

请注意，OpenWinClass=* 允许与沙盒外的所有窗口进行完全通信，但可能干扰某些拖放操作。

**识别窗口类名**

非沙盒化窗口由其_窗口类名_标识，这是创建它的应用程序给窗口的内部名称。您可以使用 [WinSpy](https://www.catch22.net/software/winspy) 等工具来识别窗口类名。Sandboxie Classic 中的[资源访问监视器](ResourceAccessMonitor.md)工具和 Sandboxie Plus 中的[跟踪日志](../PlusContent/TraceLog.md)工具也显示窗口类名。

相关的 Sandboxie Plus 设置：

沙盒选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 开放

沙盒选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 忽略 UIPI

沙盒选项 > 资源访问 > 窗口 > 不更改由沙盒化程序创建的窗口类名

另请参见：[不重命名窗口类](NoRenameWinClass.md)。 