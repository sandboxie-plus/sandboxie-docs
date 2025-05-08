# 已知冲突

* * *
已知冲突可以通过在沙盒设置 > 应用程序或沙盒选项 > 应用程序模板（Plus 版本）中激活应用程序配置来解决。
* * *

### 并非所有程序都可以在 Sandboxie 内安装或运行

问题：某些调用服务或驱动程序的应用程序可能无法在 Sandboxie 内安装/运行。

解决方案 #1：您的系统上安装的第三方安全软件可能存在冲突（参见问题 [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647) 和 [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293)）。如果您想了解可能涉及哪些安全套件，请查看[存档论坛](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539)。

解决方案 #2：如果您已经尝试在新的空沙盒中安装应用程序，那么请在主机上安装它并在沙盒中运行。

如果问题仍然存在，特别是对于在以前的 Sandboxie 版本中可以工作的应用程序，请通过在 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie/issues)上发帖告诉我们详细信息。

### Microsoft Store 应用

问题：Microsoft Store 应用在 Sandboxie Classic 和 Sandboxie Plus 中都无法工作。

解决方案：目前没有解决方案。请参见问题 [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) 以跟踪任何可能的变化。

### Office 2013/2016/2019 & Office 365（仅限 C2R 版本）

问题：Microsoft Office 2013、2016、2019 和 Office 365 的即点即用版本在沙盒化时会崩溃。这包括 Outlook 2013 及更高版本。

解决方案：在 [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7) 中包含了修复。

### Office 2021

问题：Office 2021 无法在沙盒内安装。

解决方案：目前没有解决方案。请参见问题 [#1675](https://github.com/sandboxie-plus/Sandboxie/issues/1675) 或 [#1900](https://github.com/sandboxie-plus/Sandboxie/issues/1900) 以跟踪任何可能的变化。

### Tor 浏览器

问题：Tor 浏览器在沙盒中非常慢，崩溃或在一段时间后崩溃。

解决方案：在 [v1.0.21 / 5.55.21](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.21) 中包含了修复。

### HP 通用打印驱动程序

问题：从沙盒化的 Web 浏览器打印时，HP 通用打印机状态监视器弹出组件失败。

解决方案：打开沙盒设置 > 资源访问 > COM 访问，点击添加并输入此资源名称：
`{D713F357-7920-4B91-9EB6-49054709EC7A}`

### Microsoft Edge 的自动删除功能

问题：Microsoft Edge 的自动删除功能不再工作。

解决方案：Microsoft Edge 更新了一个新设置（在系统下），称为"启动提升"，默认启用。它会阻止 Edge 完全关闭，因此我们建议禁用该选项或安装包含修复的 [v1.1.2 / 5.56.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.1.2) 或更新版本。

### Steam 游戏

问题：并非所有 Steam 游戏都能在沙盒化时运行。

解决方案：在您的计算机上安装游戏，而不是在沙盒中。大多数游戏都可以工作。但是，有[已知报告](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue)表明有些游戏可能无法工作。如果您遇到 Steam 游戏的问题，应确保主机上的 Steam 客户端已更新。不要在沙盒中运行 Steam，在主机上下载并安装游戏，然后"右键单击"游戏快捷方式并选择"在沙盒中运行"作为解决方法。如果问题仍然存在，请通过在 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie/issues)上发帖告诉我们详细信息。

### GOG 游戏和 Galaxy Beta

问题：来自 GOG Galaxy 的游戏在沙盒化时可能无法运行。

解决方案：在 [#1246](https://github.com/sandboxie-plus/Sandboxie/issues/1246) 中提供了部分解决方法。您可以"强制"GOG 程序文件夹，使其在沙盒内正确工作。另见：[ForceFolder](ForceFolder.md)。

### Windows 11 中任何沙盒都无法访问麦克风或摄像头

问题：在 Windows 11 系统中，任何沙盒都无法访问麦克风/摄像头。

解决方案：在 [#1669](https://github.com/sandboxie-plus/Sandboxie/issues/1669) 中提供了解决方法，但没有永久性修复。

### Chromium 浏览器的标签会话有时在 Sandboxie 中无法正确恢复

问题：当 Chromium 浏览器在沙盒外运行时，标签会话会丢失。

解决方案：尚无修复，但在 [#558](https://github.com/sandboxie-plus/Sandboxie/issues/558) 中提供了一些解决方法。

### Windows 资源管理器打开文件夹、驱动器或上下文菜单需要很长时间

问题：在 Windows 10 和 11 上，沙盒化的 Windows 资源管理器可能需要很长时间才能打开。

解决方案：尚无修复，请参见 [#69](https://github.com/sandboxie-plus/Sandboxie/issues/69)。

### 沙盒化的文件资源管理器实例中的"打开方式"对话框不工作

问题："打开方式"功能在 Sandboxie 中不工作。

解决方案：在 [v1.0.6 / 5.55.6](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.6) 中包含了修复。

### 无法使用文件资源管理器中的搜索框

问题：沙盒化时，文件资源管理器中的搜索框无法获得焦点，无法输入任何内容。

解决方案：在 [v0.9.8c / 5.53.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.8c) 中包含了修复。

### 程序沙盒化时可能出现"沙盒化服务启动失败：BITS"或"启动服务 bits 的请求被拒绝"

问题：自几个 Windows 10 版本以来，BITS 服务似乎已损坏，因为它使用了一些在 Sandboxie 中被阻止的 WMI 部分。

解决方案：在 [v1.0.1 / 5.55.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.1) 中直接包含了解决方法。

### 我在此列表中找不到我的问题

如果您想搜索更多问题，请参考 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie)。 