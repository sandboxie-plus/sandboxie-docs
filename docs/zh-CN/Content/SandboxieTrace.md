# Sandboxie 跟踪

### 对于沙盘经典版，请参阅[资源访问监视器](ResourceAccessMonitor.md)。

### 对于沙盘增强版，请参阅[跟踪日志](../PlusContent/TraceLog.md)。

---

### 概述

在某些情况下，程序在沙箱内可能无法正常运行，因为它需要访问某个系统资源，而该资源默认受沙盘保护，访问会被拒绝。

请注意，在这种情况下，沙箱内的程序并非自行创建该资源；相反，它期望该资源已经可供访问和使用。

跟踪功能会显示访问尝试，从而能够较为轻松地识别出哪些为确保程序正常运行所需的资源被阻止了。

### 启用跟踪

可以通过不同的[沙盘配置文件](SandboxieIni.md)设置来激活跟踪功能：

* **文件跟踪（FileTrace）**：记录对文件、文件夹和文件系统卷的访问；
* **注册表项跟踪（KeyTrace）**：记录对注册表项的访问（但不包括注册表项内的值）；
* **命名管道跟踪（PipeTrace）**：记录对用于进程间通信的命名管道和邮件槽对象的访问；
* **进程间通信跟踪（IpcTrace）**：记录对其他用于进程间通信的对象的访问，还会记录一个进程对另一个进程的访问尝试；
* **图形用户界面跟踪（GuiTrace）**：记录窗口间的通信；
* **COM 类标识符跟踪（ClsidTrace）**：记录 COM 通信；
* **防火墙跟踪（NetFwTrace）**：跟踪防火墙组件的操作（自 0.9.0 / 5.51.0 版本起）；
* **日志 API（LogAPI）**：用于获取额外跟踪输出的库（有关更多信息，请参阅[这篇帖子](https://forum.xanasoft.com/threads/how-to-get-malawre-trace-in-sandboxie.143/)）。

每个设置都接受一个字符序列，用于指定要记录的内容。字符 _a_ 记录被允许的请求；字符 _d_ 记录被拒绝的请求。对于 **文件跟踪（FileTrace）** 和 **命名管道跟踪（PipeTrace）** 设置，字符 _i_ 记录因访问被沙盘忽略的设备（如 CD - ROM）而被允许的请求。

**命名管道跟踪（PipeTrace）**、**进程间通信跟踪（IpcTrace）** 和 **图形用户界面跟踪（GuiTrace）** 设置与本页面的讨论更为相关。**文件跟踪（FileTrace）** 和 **注册表项跟踪（KeyTrace）** 通常无法提供有关沙箱内程序为何出现故障的信息。

因此，通常通过在[沙盘配置文件](SandboxieIni.md)中进行以下更改来启用跟踪：
```
   [GlobalSettings]
   IpcTrace=ad
   PipeTrace=ad
   GuiTrace=ad
```

然后使用沙盘重新加载配置：
* 在沙盘经典版中，选择“配置”菜单 -> “重新加载配置”
* 在沙盘增强版中，选择“选项”菜单 -> “重新加载 ini 文件”

可以按沙箱设置跟踪选项，这样只有需要的沙箱才会生成跟踪日志。

还可以通过添加 `跟踪缓冲区页面（TraceBufferPages）=2560` 来调整缓冲区大小，这将使其增大 10 倍。

### 查看 **防火墙跟踪（NetFwTrace）**、**进程间通信跟踪（IpcTrace）** 和 **命名管道跟踪（PipeTrace）** 的跟踪信息

自 0.9.0 / 5.51.0 版本起，添加了一个新选项 `防火墙跟踪（NetFwTrace）=*` 来跟踪防火墙组件的操作。请注意，驱动程序仅将日志记录到内核调试输出，你可以使用 [DbgView.exe](https://docs.microsoft.com/en-us/sysinternals/downloads/debugview) 查看。

在 Windows Vista 及更高版本中，系统调试器日志的输出默认是禁用的。[这篇博客文章](https://web.archive.org/web/20080731211018/http://blogs.msdn.com:80/doronh/archive/2006/11/14/where-did-my-debug-output-go-in-vista.aspx) 和 [这篇帖子](https://web.archive.org/web/20230324011501/https://stackoverflow.com/questions/65015739/outputdebugstring-not-showing-message-in-debugview-windows-10-x64) 解释了如何启用它。

以下跟踪信息将以以下格式显示输出（假设启用了 **进程间通信跟踪（IpcTrace）** 和 **命名管道跟踪（PipeTrace）**）：
```
...
(001404) SBIE (FA) 00120116.01.00000000 \Device\NamedPipe\ShimViewer
...
(001404) SBIE (IA) 001F0001 \ThemeApiPort
...
(001404) SBIE (PD) 00000040 001136
(001404) SBIE (PA) 00020400 001136
...
(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd\Endpoint
(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd
...
(001404) SBIE (ID) 001F0001 \RPC Control\protected_storage
...
```
格式如下：

```(进程 ID) 沙盘（类别访问标识）（访问请求）（资源）```

- `进程 ID` 标识尝试进行访问的进程；
- `类别` 表示该资源的沙盘类别 —— 稍后会详细介绍；
- `访问标识` 表示访问是否被允许（A 表示允许，D 表示拒绝）；
- `访问请求` 表示对对象请求的访问，通常不太重要或不感兴趣；
- `资源` 标识所需访问的资源；在进程间访问的情况下，当 `类别访问标识` 为 (PA) 或 (PD) 时，资源名称是被访问进程的进程 ID。

一些示例：

```(001404) SBIE (IA) 001F0001 \ThemeApiPort```

在此示例中，发起请求的进程的进程 ID 为 1404，并且被允许访问名为 _ThemeApiPort_ 的资源。资源类别为 I，因此这是一个进程间对象。该访问被允许是因为默认情况下，沙盘允许此特定访问。

```(001404) SBIE (ID) 001F0001 \RPC Control\protected_storage```

在此示例中，对资源 _protected_storage_ 的访问被拒绝。默认情况下，沙盘不允许此访问；但是，`打开受保护存储（OpenProtectedStorage）` 设置会更改此行为。

```(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd\Endpoint```

在此示例中，对资源 _Endpoint_ 的访问被允许。资源类别为 F，因此这是一个命名管道或邮件槽资源。该访问默认被允许，因为 _\Device\Afd_ 前缀命名了 Internet 访问所需的资源。

### 查看 **图形用户界面跟踪（GuiTrace）** 条目

当启用 **图形用户界面跟踪（GuiTrace）** 时，跟踪还会生成如下条目：
```
...
(001404) SBIE (GA) WinHook 0002 on tid=001484 pid=001960
(001404) SBIE (GA) AccHook on tid=000000 pid=000000
...
(001404) SBIE (GD) PostMessage 01224 (04C8) to hwnd=00050060 pid=001324 DDEMLMom
(001404) SBIE (GD) SendMessage 49376 (C0E0) to hwnd=00010014 pid=000804 #32769
...
(001404) SBIE (GD) SendInput
(001404) SBIE (GA) SendInput
```
这些条目有几种格式。(GA) 或 (GD) 之后的第一个单词标识条目的类型。

当第一个单词是 _窗口钩子（WinHook）_ 或 _辅助功能钩子（AccHook）_ 时，该条目表示钩子的安装。对于 (GA) 条目，钩子安装被允许；对于 (GD) 条目，钩子安装被拒绝。_窗口钩子（WinHook）_ 是标准的 Windows 钩子，后面跟着钩子的类型（请参阅 [MSDN 中的 SetWindowsHookEx](https://www.google.com/search?hl=en&q=setwindowshookex+msdn)）。_辅助功能钩子（AccHook）_ 是辅助功能钩子（请参阅 [MSDN 中的 SetWinEventHook](https://www.google.com/search?hl=en&q=setwineventhook+msdn)）。

这两种条目都标识了钩子要安装到的线程号（线程 ID）和进程号（进程 ID）。

当第一个单词是 _投递消息（PostMessage）_、_发送消息（SendMessage）_ 或 _线程消息（ThrdMessage）_ 时，该条目显示被拒绝的窗口通信。接下来的两个数字表示窗口消息编号，分别为十进制和十六进制。该条目还表示目标窗口的窗口句柄（窗口句柄）、拥有此窗口的进程号（进程 ID），最后是窗口的内部窗口类名。

### 分析跟踪信息

使用跟踪功能的目的通常是识别出导致沙箱内程序无法正常运行的资源。

例如，考虑以下跟踪记录：

```(001404) SBIE (ID) 001F0001 \BaseNamedObjects\Xyzzy```

This shows that access to some _Xyzzy_ resource was denied. Sandboxie does not know this resource, and by default, it denies access to unknown resources.

If a sandboxed program begins to malfunction (it may lock up, or it may end abruptly, or just complain about something) soon after this record appears in the trace, it stands to reason that the program was expecting the resource to be accessible.

The next step is to add an [OpenIpcPath](OpenIpcPath.md) setting for this resource:

```OpenIpcPath=\BaseNamedObjects\Xyzzy```

这表明对某个 _Xyzzy_ 资源的访问被拒绝。沙盘不识别此资源，并且默认情况下，它会拒绝访问未知资源。

如果沙箱内的程序在这条记录出现在跟踪信息中后不久开始出现故障（可能会锁定、突然结束或只是抱怨某些问题），那么很可能该程序原本期望该资源是可访问的。

下一步是为该资源添加一个 [打开进程间通信路径（OpenIpcPath）](OpenIpcPath.md) 设置：

```打开进程间通信路径（OpenIpcPath）=\BaseNamedObjects\Xyzzy```

此设置告诉沙盘，对 _Xyzzy_ 资源的访问不应被阻止。

然后重新加载沙盘配置，清除跟踪显示中的旧内容，并重新启动沙箱内的程序。如果程序现在运行得更好，那么 _Xyzzy_ 确实是有问题的资源。

但如果程序仍然失败，可以再次检查跟踪日志，查找后续（或可能更早）的失败访问尝试。

### 资源类别

跟踪记录显示了对象的沙盘资源类别。这表明需要哪个 `打开xxx路径（OpenXxxPath）` 设置来允许访问该对象。

* 当资源类别为 F，如 (FA) 或 (FD) 时，相关设置是 [打开文件路径（OpenFilePath）](OpenFilePath.md) 和 [关闭文件路径（ClosedFilePath）](ClosedFilePath.md)。
* 当资源类别为 K，如 (KA) 或 (KD) 时，相关设置是 [打开注册表项路径（OpenKeyPath）](OpenKeyPath.md) 和 [关闭注册表项路径（ClosedKeyPath）](ClosedKeyPath.md)。
* 当资源类别为 I，如 (IA) 或 (ID) 时，相关设置是 [打开进程间通信路径（OpenIpcPath）](OpenIpcPath.md) 和 [关闭进程间通信路径（ClosedIpcPath）](ClosedIpcPath.md)。
* 当资源类别为 G，如 (GA) 或 (GD) 时，相关设置是 [打开窗口类（OpenWinClass）](OpenWinClass.md)。
* 对于 **COM 类标识符跟踪（ClsidTrace）** 显示的 COM 对象，相关设置是 [打开 COM 类标识符（OpenClsid）](OpenClsid.md)。
