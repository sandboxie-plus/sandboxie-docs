# 隐私问题

这是一个高级主题，说明即使在 Sandboxie 下运行程序之后，你的计算机仍可能记录_哪些_程序被执行过或它们做了什么。必须强调，这不是安全漏洞，因为它绝不允许沙盒化程序感染或以其他方式滥用你的计算机。不过，对于关心使用 Sandboxie 的隐私方面的人来说，这可能是值得一读的内容。

**概述**

Sandboxie 的指导原则是隔离并遏制其所监管程序采取的任何行动，目的是让计算机和操作系统保持干净健康的状态。

在 Sandboxie 下运行程序产生的大多数副作用，实际上正是由该程序本身造成的，并且会在沙盒被删除时消失。例如，在 Sandboxie 下运行的网页浏览器会把你的浏览历史记录在沙盒中，删除沙盒时这段历史会被完全擦除。

因此，人们很容易从上面的指导原则做一个小的逻辑跳跃，假设 Sandboxie 的原则之一是保护你的隐私，并清除任何受其监管程序直接或间接造成的痕迹。然而，这种假设并不正确。

Sandboxie 在遏制其监管程序采取的行动上投入了大量努力，但 Sandboxie 完全没有做任何事来阻止你自己的 Windows 操作系统保留你在计算机上所做事情的记录。

如果一个人错误地假设 Sandboxie 极度关心隐私，他可能会惊讶地发现 Windows 中有多种痕迹和日志会记录哪些程序一直在运行，即使是在沙盒内。

本页将解释记录你所运行程序信息的各种已知机制——无论在 Sandboxie 的监管之内还是之外。

**预读取和超级预读取**

预读取（Prefetch）在 Windows XP 中引入，超级预读取（SuperFetch）在 Windows Vista 中引入，它们共同构成 Windows 中的 [预读取器](https://en.wikipedia.org/wiki/Prefetcher) 组件。

该组件旨在通过把程序文件的副本保存在可快速访问的位置来改善应用程序的启动时间。副本保存在主 Windows 文件夹内的名为 _Prefetch_ 的文件夹中；通常为 _C:\Windows\Prefetch_。

即使程序是在 Sandboxie 下执行的，Windows 也可能在此 Prefetch 文件夹中存储程序文件的副本。

预读取行为可以减少为仅缓存启动序列期间使用的程序，或完全不缓存任何内容。更多信息请访问以下链接：

* [https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters](https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters)
* [https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista](https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista)
* [https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista](https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista)

**MUI 缓存**

Windows 资源管理器会在注册表中记录直接通过它启动的程序的名称。这包括通过开始菜单、桌面、快速启动区域或任何文件夹视图启动的程序。即使使用右键"以沙盒方式运行"操作在 Sandboxie 下启动程序，情况也是如此。

记录的信息保存在此注册表项中：
```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache
```

如果你通过 Sandboxie 的设施（如 Sandboxie 开始菜单）启动程序，或通过已在 Sandboxie 下运行的程序启动，则此信息保存在沙盒内的注册表中。

有多种第三方注册表清理工具可以擦除此信息。

**Windows 任务栏**

在 Windows 7 及更高版本中，Windows 资源管理器存储与任务栏图标关联的信息。此信息包括程序图标和用于启动它的命令。信息存储在用户配置文件文件夹内以下文件夹的文件中：
```
   %Appdata%\Microsoft\Internet Explorer\Quick Launch\User Pinned\ImplicitAppShortcuts
```

[沙盒设置 > 应用程序 > 其他](ApplicationsSettings.md#其他) 设置页包含设置"允许程序更新 Windows 任务栏中的跳转列表"。如果启用此设置，会在用户配置文件文件夹内的以下文件夹中创建额外文件：
```
   %Appdata%\Microsoft\Windows\Recent\CustomDestinations
   %Appdata%\Microsoft\Windows\Recent\AutomaticDestinations
```

**Windows 页面文件**

在正常运行过程中，Windows 有时需要把一个程序使用的内存内容暂存起来，以便为另一个程序腾出空间。内存内容存储在 Windows [页面文件](https://www.howtogeek.com/126430/what-is-the-windows-page-file) 中。

在 Sandboxie 下运行的程序与计算机中的任何其他程序一样，仍运行在同一个 Windows 操作系统中，因此沙盒化程序和普通程序的部分内容可能并排出现在同一个页面文件中。

可以配置 Windows 在关闭时清除页面文件的内容。更多信息见 [此处](https://winaero.com/clear-pagefile-shutdown-windows-10) 和 [此处](https://www.vistax64.com/threads/virtual-memory-paging-file-clear-at-shutdown.157323)。

可以配置 Windows 加密页面文件的内容：

*   运行 _secpol.msc_ 打开_本地安全策略_编辑器
*   展开标记为_公钥策略_的组
*   右键点击标记为_加密文件系统_的项目上的_属性_
*   选择_允许_以启用加密文件系统（EFS）
*   点击_应用_，然后点击_确定_
*   重启使新设置生效

**Windows 休眠文件**

与 Windows 页面文件类似，休眠文件在计算机休眠关机前存储系统内存和状态的副本。因此，休眠文件可能包含沙盒化程序使用过的内存片段。

**系统还原**

还原点是操作系统在某些时间点状态的快照。Windows XP 及更高版本中的系统还原组件会记录并还原这些快照。

快照记录在（通常无法访问的）名为 _System Volume Information_ 的文件夹中，可能包含系统各处的 [多种文件](https://docs.microsoft.com/en-us/windows/win32/sr/monitored-file-extensions)，包括沙盒文件夹内。

因此，系统还原可能会在其文件夹中为仅存在于沙盒中的文件或程序创建备份副本。

系统还原组件可以设置为忽略临时文件夹中的文件和文件夹，因此 [把沙盒移动](FileRootPath.md) 到 _%TEMP%\SANDBOX_（而不是默认的 _C:\SANDBOX_），并在注册表项 [FilesNotToSnapshot](https://learn.microsoft.com/en-us/windows/win32/vss/excluding-files-from-shadow-copies#using-the-filesnottosnapshot-registry-key) 中添加路径后，系统还原在创建卷影副本快照时应忽略沙盒。更多信息见 [此处](https://learn.microsoft.com/en-us/windows/win32/backup/registry-keys-for-backup-and-restore)。

**系统日志、审核日志和其他事件日志**

Windows 有时会在其各种 [事件日志](https://en.wikipedia.org/wiki/Event_Viewer) 中记录关于运行程序的信息片段。通常，关于程序记录的信息即使有也极少。然而，如果系统的某些方面启用了安全审核，Windows 将毫无困难地记录在 Sandboxie 下运行的程序所采取任何操作的详细信息。

Windows 有一个事件查看器程序，可用于查看和删除事件日志。更多信息见 [此处](https://www.howtogeek.com/123646/htg-explains-what-the-windows-event-viewer-is-and-how-you-can-use-it)。

**Windows 系统托盘图标**

当在 Sandboxie 下运行的程序请求在 [系统托盘区域](https://www.computerhope.com/issues/chsys.htm) 放置图标时，Sandboxie 会允许该程序把图标放在真实的系统托盘中，后者通常位于显示器右下角。

这样做的好处是，与沙盒化程序托盘图标的交互就像与任何其他托盘图标交互一样容易。但这也意味着 Windows 会在它曾显示过的所有托盘图标历史中记录该图标及其描述。

可以手动清除 Windows 中的这段历史。也可能有第三方注册表清理工具可以擦除此信息。

**磁盘碎片整理**

磁盘碎片整理软件可用于在数据块层面组织硬盘内容，以便操作系统更快地访问文件。

虽然这不是隐私问题，但沙盒化程序能否对磁盘进行碎片整理的问题已被提出，应当加以说明。

Sandboxie 的隔离发生在较高的文件层面，而非较低的数据块层面。在磁盘上移动数据块对沙盒的隔离没有影响，恶意程序也无法借此以某种方式把自己的数据"移出"沙盒。

**IP 隐私**

Sandboxie 的隔离和保护完全发生在本地计算机内，任何远程计算机都看不到。因此，用沙盒化程序访问互联网，看起来与用不在 Sandboxie 下运行的程序访问互联网是一样的。两种情况下，远程计算机都是通过 IP 地址来识别访问的计算机。

有多种第三方匿名网页访问解决方案。更多信息见 [此处](https://en.wikipedia.org/wiki/Anonymous_web_browsing)。

**Windows DNS 主机缓存**

Sandboxie 不会阻止 Windows 机器上 _hosts_ 文件（DNS 缓存）的记录和存储。该文件写入 _C:\Windows\System32\drivers\etc_。
