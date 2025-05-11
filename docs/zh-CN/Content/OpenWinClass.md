# 开放窗口类

_OpenWinClass_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定应允许沙盘程序访问的非沙箱窗口的类名。

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

第一个示例允许 _cmd.exe_ 进程创建的控制台窗口可被沙盘中的程序访问。

通常情况下，沙盘不会允许沙箱内的程序访问、通信、关闭或销毁沙箱外的窗口。_OpenWinClass_ 设置为这一规则提供了例外，允许访问特定的非沙箱窗口。

**特殊形式**
```
   OpenWinClass=$:program.exe/IgnoreUIPI
```

此设置允许在沙箱中运行的程序使用 `PostThreadMessage API`，直接向运行在沙箱之外目标进程中的线程发送消息。此种 _OpenWinClass_ 设置形式不支持通配符，因此，目标进程的进程名必须与设置中指定的名称相匹配。
```
   OpenWinClass=#
```

此设置指示沙盘不要更改由沙箱程序创建的窗口类名。通常，沙盘会将 _IEFrame_ 这样的类名转换为 _Sandbox:DefaultBox::IEFrame_，以便更好地区分沙箱程序的窗口和系统中其他窗口。

然而，在某些情况下，沙箱外的程序可能期望窗口类名为特定名称，因此可能无法识别由沙箱程序创建的窗口。指定 `OpenWinClass=#` 可解决此问题，但会降低隔离度。

请注意，`OpenWinClass=#` 不允许与任何沙箱外的窗口通信，并且可能会干扰某些拖放操作。
```
   OpenWinClass=*
```

此设置指示沙盘不要像上述方式转换窗口类名，同时使沙箱程序能够访问系统中的所有窗口，并进一步禁用与窗口相关的其他部分沙盘功能。此时，窗口标题可能不再显示沙盘标志 [#]。

请注意，OpenWinClass=* 允许与所有沙箱外窗口的完全通信，但同样可能干扰一些拖放操作。

**识别窗口类名**

非沙箱窗口通过其 _窗口类名_ 进行识别，该类名是创建该窗口的应用程序分配的内部名称。你可以使用 [WinSpy](https://www.catch22.net/software/winspy) 这类工具来识别窗口类名。[Sandboxie Classic](ResourceAccessMonitor.md) 中的 [资源访问监视器] 工具以及 Sandboxie Plus 中的 [跟踪日志](../PlusContent/TraceLog.md) 工具也能显示窗口类名。

相关 Sandboxie Plus 设置：

沙箱选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 开放

沙箱选项 > 资源访问 > 窗口 > 添加窗口类 > 访问列 > 忽略 UIPI

沙箱选项 > 资源访问 > 窗口 > 不更改沙盘程序创建的窗口类名

另请参阅：[不要重命名窗口类](NoRenameWinClass.md)。