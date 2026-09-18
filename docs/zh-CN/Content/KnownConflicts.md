# 已知冲突

* * *
已知冲突可以通过在沙盒设置 > 应用程序或沙盒选项 > 应用程序模板（Plus 版）中激活应用程序配置来解决。
* * *

### 并非所有程序都能在沙盒中安装或运行

问题：某些调用服务或驱动程序的应用程序可能无法在沙盒中安装/运行。

解决方案 1：你可能与系统上安装的第三方安全软件存在冲突（参见问题 [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647) 和 [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293)）。如果你想知道可能涉及哪个安全套件，请查看 [存档论坛](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539)。

解决方案 2：如果你已经尝试在一个新的空沙盒中安装你的应用程序，那么请把它安装到宿主机上，再以沙盒化方式运行它。

如果问题仍然存在，尤其是那些在旧版 Sandboxie 上正常工作的应用程序，请通过在 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie/issues) 上发帖告知我们详细信息。

### Microsoft Store 应用

问题：Microsoft Store 应用无法在 Sandboxie 经典版和 Sandboxie Plus 中运行。

解决方案：目前没有。参见问题 [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) 以跟踪关于此问题的任何可能变化。

### Office 2013/2016/2019 与 Office 365（仅限 C2R 版本）

问题：Microsoft Office 2013、2016、2019 和 Office 365 的即点即用（Click to Run）版本在沙盒化时会崩溃。这包括 Outlook 2013 及更高版本。

解决方案：修复已包含在 [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7) 中。

### Office 2021

问题：Office 2021 无法在沙盒内安装。

解决方案：目前没有。参见问题 [#1675](https://github.com/sandboxie-plus/Sandboxie/issues/1675) 或 [#1900](https://github.com/sandboxie-plus/Sandboxie/issues/1900) 以跟踪关于此问题的任何可能变化。

### Tor 浏览器

问题：Tor 浏览器在沙盒中非常慢、崩溃，或在一段时间后崩溃。

解决方案：修复已包含在 [v1.0.21 / 5.55.21](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.21) 中。

### HP 通用打印驱动

问题：从沙盒化的网页浏览器打印时，HP 通用打印机状态监视器弹出组件会失败。

解决方案：打开沙盒设置 > 资源访问 > COM 访问，点击“添加”并输入此资源名称：
`{D713F357-7920-4B91-9EB6-49054709EC7A}`

### Microsoft Edge 的自动删除功能

问题：自动删除功能在 Microsoft Edge 上不再起作用。

解决方案：Microsoft Edge 更新后新增了一个设置（位于“系统”下），名为“启动提升”（Startup boost），默认启用。它阻止 Edge 完全关闭，因此我们建议禁用该选项，或安装包含修复的 [v1.1.2 / 5.56.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.1.2) 或更新版本。

### Steam 游戏

问题：并非所有 Steam 游戏都能在沙盒化状态下运行。

解决方案：把游戏安装到你的计算机上，而不是沙盒中。大多数游戏可以正常运行。然而，有 [已知报告](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue) 称某些游戏可能确实无法运行。如果你遇到 Steam 游戏问题，应确保宿主机上的 Steam 客户端是最新的。不要以沙盒化方式运行 Steam，在宿主机上下载并安装游戏，然后“右键点击”游戏快捷方式并选择“以沙盒方式运行”作为变通办法。如果问题仍然存在，请通过在 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie/issues) 上发帖告知我们详细信息。

### GOG 游戏与 Galaxy Beta

问题：GOG Galaxy 的游戏在沙盒化时可能无法运行。

解决方案：在 [#1246](https://github.com/sandboxie-plus/Sandboxie/issues/1246) 中有一个部分变通办法。你可以“强制”GOG 程序文件夹，使其在沙盒内正常工作。另请参阅：[强制文件夹](ForceFolder.md)。

### Windows 11 中无法访问麦克风或摄像头

问题：在 Windows 11 系统上，任何沙盒都无法访问麦克风/摄像头。

解决方案：[#1669](https://github.com/sandboxie-plus/Sandboxie/issues/1669) 中有一个变通办法，但没有永久修复。

### Chromium 浏览器的标签页有时无法恢复

问题：当 Chromium 浏览器在沙盒外运行时，标签页会话会丢失。

解决方案：还没有修复，但 [#558](https://github.com/sandboxie-plus/Sandboxie/issues/558) 中有一些变通办法。

### Windows 资源管理器打开文件夹、驱动器或右键菜单时很慢

问题：在 Windows 10 和 11 上，Windows 资源管理器在沙盒化状态下打开可能需要很长时间。

解决方案：还没有修复，参见 [#69](https://github.com/sandboxie-plus/Sandboxie/issues/69)。

### “使用其他应用打开”对话框在沙盒中的文件资源管理器实例里无法使用

问题：“打开方式”功能在 Sandboxie 中无法正常工作。

解决方案：修复已包含在 [v1.0.6 / 5.55.6](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.6) 中。

### 文件资源管理器中的搜索框无法使用

问题：文件资源管理器中的搜索框在沙盒化状态下无法获得焦点，你无法输入任何内容。

解决方案：修复已包含在 [v0.9.8c / 5.53.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.8c) 中。

### 程序在沙盒中运行时可能出现“沙盒服务启动失败：BITS”或“启动 BITS 服务的请求被拒绝”等提示

问题：自几个 Windows 10 版本以来，BITS 服务似乎已损坏，因为它使用了 Sandboxie 中阻止的某些 WMI 部分。

解决方案：变通办法已直接包含在 [v1.0.1 / 5.55.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.1) 中。

### 找不到你的问题？

如果你想搜索更多问题，请参阅 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie)。
