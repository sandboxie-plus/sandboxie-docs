# 隐私问题

* * *
这是一个高级主题，说明即使你在 Sandboxie 中运行了程序，你的计算机仍可能记录**运行了哪些程序**以及它们的行为。这并不代表出现了安全漏洞，因为这些记录**不会**让沙盘程序感染或滥用你的计算机。但如果你关心使用 Sandboxie 时的隐私问题，这篇文章值得一读。

---

**概述**

Sandboxie 的核心原则是：隔离并控制其监督下程序的行为，目的是保持计算机和操作系统的干净与健康。

大多数在 Sandboxie 中运行程序的“副作用”，其实来自程序本身，并且会在沙盘被删除后一起消失。例如，在沙盘中运行的浏览器会将浏览记录保存在沙盘内，而这些记录在删除沙盘时会被完全清除。

因此，用户很容易从上述原则中得出推论：Sandboxie 的目标是保护你的隐私，并清除所有由其监管程序直接或间接产生的痕迹。但这种假设是不准确的。

Sandboxie 虽然非常注重控制程序行为，但它**不会试图阻止 Windows 操作系统本身**记录你在计算机上的活动。

如果有人错误地认为 Sandboxie 会极度保护隐私，他们可能会惊讶地发现 Windows 系统中仍然可以找到一些记录程序运行痕迹（哪怕是在沙盘中运行）。

本文将解释在 Windows 中用于记录程序活动的各种机制——无论程序是否在 Sandboxie 的监督下运行。

---

**Prefetch 与 SuperFetch**

Prefetch（预取）最早出现在 Windows XP，SuperFetch 出现在 Windows Vista，它们共同构成了 Windows 的 [预取器](https://en.wikipedia.org/wiki/Prefetcher) 组件。

这个组件用于加快程序启动速度，它会将程序文件的副本保存在一个可快速访问的位置。副本通常被存储在 Windows 主目录下的 `Prefetch` 文件夹中，通常路径是 `C:\Windows\Prefetch`

即使是在 Sandboxie 中运行的程序，Windows 也可能会将其文件副本写入 Prefetch 文件夹。

你可以通过修改设置，限制预取器只缓存启动时使用的程序，甚至完全禁用预取功能。更多信息请见：

* [https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters](https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters)
* [https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista](https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista)
* [https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista](https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista)

---

**MUI 缓存**

Windows 资源管理器会在注册表中记录通过它启动的程序名称。这包括从开始菜单、桌面、快速启动栏或文件夹中启动程序的情况。即使使用右键“沙盘运行”功能，也会被记录。

记录信息存储在以下注册表项中：
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache
```

如果你是通过 Sandboxie 的界面（如 Sandboxie 内的启动菜单）或通过一个已在沙盘中运行的程序来启动其他程序，那么这些记录就会被保存在沙盘的注册表中。

你可以使用第三方注册表清理工具来清除这些信息。

---

**Windows 任务栏**

在 Windows 7 及更高版本中，资源管理器会记录任务栏图标相关信息，包括图标及其启动命令。这些信息存储在用户配置文件夹的以下路径中：
```
%Appdata%\Microsoft\Internet Explorer\Quick Launch\User Pinned\ImplicitAppShortcuts
```

若在 [Sandbox 设置 > 应用程序 > 杂项](ApplicationsSettings.md#miscellaneous) 中启用了“允许程序更新 Windows 7 任务栏跳转列表”选项，还会在以下文件夹中生成其他记录：
```
%Appdata%\Microsoft\Windows\Recent\CustomDestinations
%Appdata%\Microsoft\Windows\Recent\AutomaticDestinations
```

---

**Windows 页面文件**

在正常操作中，Windows 会将部分程序使用的内存内容写入 [页面文件](https://www.howtogeek.com/126430/what-is-the-windows-page-file)，以便为其他程序腾出内存。

由于沙盘程序仍运行于操作系统之中，因此其内存内容可能与普通程序一起被写入同一个页面文件。

你可以设置 Windows 在关机时清除页面文件的内容。参考：
* [关机时清理页面文件（Win 10）](https://winaero.com/clear-pagefile-shutdown-windows-10)
* [关机时清理页面文件（Vista）](https://www.vistax64.com/threads/virtual-memory-paging-file-clear-at-shutdown.157323)

你也可以加密页面文件内容：

1. 运行 `secpol.msc` 打开“本地安全策略”
2. 展开“`公钥策略`”组
3. 右键“`加密文件系统`”，选择“`属性`”
4. 选择“`允许`”
5. 点击“`应用`”和“`确定`”
6. 重启电脑生效

---

**Windows 休眠文件**

与页面文件类似，休眠文件会在电脑休眠前保存系统状态及内存内容。因此，它也可能包含沙盘程序使用过的内存数据。

---

**系统还原**

还原点是操作系统在某一时间点的状态快照。从 Windows XP 起的系统还原功能会记录并可恢复这些快照。

这些快照会被保存到一个名为 _System Volume Information_ 的（通常无法访问的）文件夹中，其中可能包含系统各处的[多种类型文件](https://docs.microsoft.com/en-us/windows/win32/sr/monitored-file-extensions)，包括沙盘中的内容。

因此，系统还原有可能会为**只存在于沙盘中的文件或程序**创建备份副本。

你可以设置系统还原组件忽略临时文件夹中的文件和目录。只需将沙盘位置[移动](FileRootPath.md)到 `%TEMP%\SANDBOX`（而非默认的 `C:\SANDBOX`），并在注册表键 [FilesNotToSnapshot](https://learn.microsoft.com/en-us/windows/win32/vss/excluding-files-from-shadow-copies#using-the-filesnottosnapshot-registry-key) 中添加该路径，系统还原在创建影子副本快照时就会跳过沙盘内容。更多信息请见 [此处](https://learn.microsoft.com/en-us/windows/win32/backup/registry-keys-for-backup-and-restore)。

---

**系统、审计与事件日志**

Windows 会在其 [事件日志](https://en.wikipedia.org/wiki/Event_Viewer) 中记录某些程序行为。通常记录不多，但如果开启了安全审计功能，Windows 将详细记录沙盘内程序的行为。

你可以使用“事件查看器”来查看和删除日志，详见：
* [如何使用事件查看器](https://www.howtogeek.com/123646/htg-explains-what-the-windows-event-viewer-is-and-how-you-can-use-it)

---

**系统托盘图标**

当沙盘程序尝试在[系统托盘](https://www.computerhope.com/issues/chsys.htm)放置图标时，Sandboxie 会允许其真实显示在右下角的托盘区。

这样做的好处是用户可以方便地与图标交互。但这也意味着 Windows 会将图标及其说明记录到历史中。

你可以通过以下方法清除这些历史：
* [手动清除通知图标历史](https://www.howtogeek.com/739/clean-up-past-notification-icons-in-windows-vista)
* 也可以使用第三方注册表清理工具来删除这些记录。

---

**磁盘碎片整理**

磁盘碎片整理工具可以在磁盘底层对数据块重新排序，以提升读写性能。

虽然这并不是隐私问题，但确实有人关心沙盘程序是否能影响磁盘数据。

Sandboxie 的隔离是在文件系统层完成的，而非底层数据块。因此磁盘碎片整理**不会**影响沙盘隔离，也不会被恶意程序用来“转移”数据到沙盘外。

---

**IP 隐私**

Sandboxie 的隔离只在本地计算机上起作用，远程服务器无法感知你是否使用了沙盘。无论是否沙盘运行，访问互联网的行为在远端看来是一样的，远程主机会通过你的 IP 地址识别你。

如果你希望匿名访问网络，可以使用第三方匿名解决方案。参考：
* [匿名上网](https://en.wikipedia.org/wiki/Anonymous_web_browsing)

---

**Windows DNS 主机缓存**

Sandboxie 并不会阻止 Windows 保存或使用 DNS 缓存（hosts 文件），该文件位于：
```
C:\Windows\System32\drivers\etc
```