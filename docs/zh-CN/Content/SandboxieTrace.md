# Sandboxie 跟踪

### Sandboxie 经典版请参阅 [资源访问监视器](ResourceAccessMonitor.md)。

### Sandboxie Plus 请参阅 [跟踪日志](../PlusContent/TraceLog.md)。

---

### 概述

在某些情况下，程序可能无法在沙盒内正常运行，因为它需要访问默认受 Sandboxie 保护的某个系统资源，而对该资源的访问被拒绝。

注意：在这种情况下，沙盒化程序并不是在创建资源本身；相反，它期望该资源已经可用于访问和使用。

跟踪显示访问尝试，使识别哪些正常运行所需的资源被阻止变得相对容易。

### 启用跟踪

跟踪可以通过不同的 [Sandboxie Ini](SandboxieIni.md) 设置激活：

*   **FileTrace** 记录对文件、文件夹和文件系统卷的访问；
*   **KeyTrace** 记录对注册表项（但不包括项内的值）的访问；
*   **PipeTrace** 记录对用于进程间通信的命名管道和邮槽对象的访问；
*   **IpcTrace** 记录对其他用于进程间通信的对象的访问，也记录一个进程对另一个进程的访问尝试；
*   **GuiTrace** 记录窗口到窗口的通信；
*   **ClsidTrace** 记录 COM 通信；
*   **NetFwTrace** 跟踪防火墙组件的操作（自版本 0.9.0 / 5.51.0 起）；
*   **LogAPI** 库用于获取额外跟踪输出（更多信息参见 [此主题](https://forum.xanasoft.com/threads/how-to-get-malawre-trace-in-sandboxie.143/)）。

每个设置接受一系列指定记录内容的字符。字符 _a_ 记录被允许的请求；字符 _d_ 记录被拒绝的请求。对于 **FileTrace** 和 **PipeTrace** 设置，字符 _i_ 记录因访问被 Sandboxie 忽略的设备（如 CD-ROM）而被允许的请求。

设置 **PipeTrace**、**IpcTrace** 和 **GuiTrace** 与本页讨论更相关。**FileTrace** 和 **KeyTrace** 通常无法提供沙盒化程序为何出故障的洞察。

因此，通常通过在 [Sandboxie Ini](SandboxieIni.md) 中做如下更改来启用跟踪：
```
   [GlobalSettings]
   IpcTrace=ad
   PipeTrace=ad
   GuiTrace=ad
```

然后使用 Sandboxie 重新加载配置：
* **配置** 菜单 -> **重新加载配置**（Sandboxie 经典版）
* **选项** 菜单 -> **重新加载 ini 文件**（Sandboxie Plus）

跟踪选项可以按沙盒设置，这样只有你需要的沙盒才会生成跟踪日志。

你还可以通过添加 ```TraceBufferPages=2560``` 调整缓冲区大小，它会扩大十倍。

### 查看 **NetFwTrace**、**IpcTrace** 和 **PipeTrace** 的跟踪

自版本 0.9.0 / 5.51.0 起，新增了选项 `NetFwTrace=*` 用于跟踪防火墙组件的操作。请注意，驱动程序只记录到内核调试输出，你可以用 [DbgView.exe](https://docs.microsoft.com/en-us/sysinternals/downloads/debugview) 查看。

在 Windows Vista 及更高版本上，系统调试器日志的输出默认禁用。[这篇博客文章](https://web.archive.org/web/20080731211018/http://blogs.msdn.com:80/doronh/archive/2006/11/14/where-did-my-debug-output-go-in-vista.aspx) 和 [这个主题](https://web.archive.org/web/20230324011501/https://stackoverflow.com/questions/65015739/outputdebugstring-not-showing-message-in-debugview-windows-10-x64) 解释了如何启用它。

以下跟踪将以下列格式显示输出。（假设启用了 **IpcTrace** 和 **PipeTrace**。）
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

```(pid) SBIE (ca) (access) (resource)```

- `pid` 标识尝试访问的进程；
- `c` 表示资源的 Sandboxie 类别——稍后详细介绍；
- `a` 表示访问是被允许（A）还是被拒绝（D）；
- `access` 表示对对象请求的访问，通常不有趣也不重要；
- `resource` 标识想要访问的资源；在进程到进程访问的情况下，其中 _ca_ 为 (PA) 或 (PD)，资源名称是被访问进程的进程 id。

一些示例：

```(001404) SBIE (IA) 001F0001 \ThemeApiPort```

这里发出请求的进程是进程 id 1404，它被允许访问名为 _ThemeApiPort_ 的资源。资源类别是 I，因此这是一个进程间对象。访问被允许，因为默认情况下 Sandboxie 允许这一特定访问。

```(001404) SBIE (ID) 001F0001 \RPC Control\protected_storage```

这里对资源 _protected_storage_ 的访问被拒绝。默认情况下 Sandboxie 不允许此访问；不过 OpenProtectedStorage 设置会改变此行为。

```(001404) SBIE (FA) 00000001.0F.FFFFFFFF \Device\Afd\Endpoint```

这里对资源 _Endpoint_ 的访问被允许。资源类别是 F，因此这是一个命名管道或邮槽资源。访问默认被允许，因为 _\Device\Afd_ 前缀命名了互联网访问所需的资源。

### 查看 **GuiTrace** 条目

启用 **GuiTrace** 时，跟踪还会产生如下条目：
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
这些条目有几种格式。(GA) 或 (GD) 之后的第一个词标识条目的类型。

当第一个词是 _WinHook_ 或 _AccHook_ 时，条目指示钩子的安装。对 (GA) 条目允许其安装，对 (GD) 条目拒绝其安装。_WinHook_ 是标准 Windows 钩子，后跟钩子类型（参见 [MSDN 中的 SetWindowsHookEx](https://www.google.com/search?hl=en&q=setwindowshookex+msdn)）。_AccHook_ 是辅助功能钩子（参见 [MSDN 中的 SetWinEventHook](https://www.google.com/search?hl=en&q=setwineventhook+msdn)）。

两个条目都标识钩子将被安装到的线程号（tid）和进程号（pid）。

当第一个词是 _PostMessage_、_SendMessage_ 或 _ThrdMessage_ 时，条目显示被拒绝的窗口通信。随后的两个数字指示窗口消息号（十进制和十六进制）。条目还指示目标窗口的窗口句柄（hwnd）、拥有此窗口的进程号（pid），最后是该窗口的内部窗口类名。

### 分析跟踪

使用跟踪的目的通常是识别导致沙盒化程序无法正常运行的资源。

例如，考虑以下跟踪记录：

```(001404) SBIE (ID) 001F0001 \BaseNamedObjects\Xyzzy```

这显示对某个 _Xyzzy_ 资源的访问被拒绝。Sandboxie 不认识此资源，默认情况下它拒绝访问未知资源。

如果沙盒化程序在此记录出现在跟踪中后不久开始出故障（它可能锁死、突然结束，或只是抱怨某事），那么有理由认为该程序期望此资源可访问。

下一步是为该资源添加 [OpenIpcPath](OpenIpcPath.md) 设置：

```OpenIpcPath=\BaseNamedObjects\Xyzzy```

此设置告诉 Sandboxie 不应阻止对 _Xyzzy_ 资源的访问。

然后重新加载 Sandboxie 配置，清除跟踪显示的旧内容，并重新启动沙盒化程序。如果程序现在运行得更好，_Xyzzy_ 确实是问题资源。

但如果程序仍然失败，可以再次检查跟踪日志以查找更晚（或可能更早）的失败访问尝试。

### 资源类别

跟踪记录显示对象的 Sandboxie 资源类别。这指示需要哪个 OpenXxxPath 设置来允许访问该对象。

*   当资源类别是 F（如 (FA) 或 (FD)）时，相关设置是 [开放文件路径](OpenFilePath.md) 和 [封闭文件路径](ClosedFilePath.md)。
*   当资源类别是 K（如 (KA) 或 (KD)）时，相关设置是 [开放注册表路径](OpenKeyPath.md) 和 [封禁注册表项路径](ClosedKeyPath.md)。
*   当资源类别是 I（如 (IA) 或 (ID)）时，相关设置是 [开放 IPC 路径](OpenIpcPath.md) 和 [封禁 IPC 路径](ClosedIpcPath.md)。
*   当资源类别是 G（如 (GA) 或 (GD)）时，相关设置是 [开放窗口类](OpenWinClass.md)。
*   对于 ClsidTrace 显示的 COM 对象，相关设置是 [开放 Clsid](OpenClsid.md)。
