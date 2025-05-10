# 已知冲突

* * *
已知冲突可以通过在“沙箱设置 > 应用程序”或“沙箱选项 > 应用模板（Plus 版）”中激活应用配置进行解决。
* * *

### 并非所有程序都能在沙箱中安装或运行

问题：某些调用服务或驱动程序的应用程序可能无法在沙箱中安装/运行。

解决方法一：你系统中安装的第三方安全软件可能与沙盒存在冲突（参见问题 [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647) 和 [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293)）。如果你想了解可能涉及哪些安全套件，可查阅 [已归档论坛](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539)。

解决方法二：若你已尝试在新的空沙箱中安装应用，但仍失败，请在主机上安装该应用后使用沙箱方式运行。

如果问题依然存在，特别是以前版本的沙盒中可正常运行的应用，请通过在 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie/issues) 发表详细信息与我们沟通。

### Microsoft Store 应用

问题：Microsoft Store 应用无法在 Sandboxie Classic 和 Sandboxie Plus 中运行。

解决方法：目前暂无可用方案。请关注问题 [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) 以获取可能的变更进展。

### Office 2013/2016/2019 与 Office 365（仅 C2R 版本）

问题：Microsoft Office 2013、2016、2019 及 Office 365 的 Click to Run 版本在沙箱中会崩溃。这包括 Outlook 2013 及更高版本。

解决方法：已于 [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7) 版本中修复。

### Office 2021

问题：Office 2021 无法在沙箱中安装。

解决方法：目前暂无可用方案。请关注问题 [#1675](https://github.com/sandboxie-plus/Sandboxie/issues/1675) 或 [#1900](https://github.com/sandboxie-plus/Sandboxie/issues/1900) 以获取可能的变更进展。

### Tor 浏览器

问题：Tor 浏览器在沙箱中速度非常慢、容易崩溃或运行一段时间后崩溃。

解决方法：已于 [v1.0.21 / 5.55.21](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.21) 版本中修复。

### HP 通用打印驱动

问题：从沙箱中的 Web 浏览器打印时，HP 通用打印机状态监控弹窗组件无法正常工作。

解决方法：打开 “沙箱设置 > 资源访问 > COM 访问”，点击“添加”，并输入以下资源名称：
`{D713F357-7920-4B91-9EB6-49054709EC7A}`

### Microsoft Edge 的自动删除功能

问题：Microsoft Edge 的自动删除功能不再可用。

解决方法：Microsoft Edge 已增加一个新的设置项（位于系统设置下）名为“启动加速”，默认启用。该设置会阻止 Edge 完全关闭，建议禁用该选项，或安装包含修复的 [v1.1.2 / 5.56.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.1.2) 及以上版本。

### Steam 游戏

问题：并非所有 Steam 游戏都能在沙箱中正常运行。

解决方法：请在计算机上安装游戏，而非在沙箱中。大部分游戏可正常运行。然而，[部分游戏已知可能无法运行](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue)。如遇到 Steam 游戏问题，请确保主机上的 Steam 客户端已更新。避免沙箱运行 Steam，先在主机下载并安装游戏，然后“右键点击”游戏快捷方式，选择“沙箱中运行”作为替代。如问题仍未解决，请在 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie/issues) 提交详细信息。

### GOG 游戏及 Galaxy Beta

问题：来自 GOG Galaxy 的游戏可能无法在沙箱中运行。

解决方法：[问题 #1246](https://github.com/sandboxie-plus/Sandboxie/issues/1246) 中提供了部分临时方案。你可以“强制” GOG 程序文件夹，以便其能在沙箱中正常工作。参见：[ForceFolder](ForceFolder.md)。

### Windows 11 下所有沙箱无法访问麦克风或摄像头

问题：在 Windows 11 系统下，所有沙箱均无法访问麦克风/摄像头。

解决方法：[问题 #1669](https://github.com/sandboxie-plus/Sandboxie/issues/1669) 中提供了临时方案，但尚无永久修复。

### Chromium 浏览器在沙箱中有时无法正确恢复标签页会话

问题：当 Chromium 浏览器在沙箱外运行时，标签页会话会丢失。

解决方法：目前尚无修复，但部分临时方案可参考 [#558](https://github.com/sandboxie-plus/Sandboxie/issues/558)。

### Windows 资源管理器打开文件夹、驱动器或右键菜单速度很慢

问题：在 Windows 10 和 11 上，沙箱中的 Windows 资源管理器打开速度很慢。

解决方法：目前尚无修复，请参见 [#69](https://github.com/sandboxie-plus/Sandboxie/issues/69)。

### “打开方式”对话框在沙箱中的资源管理器实例不能用

问题：“打开方式”功能在沙盒中无法正常使用。

解决方法：已于 [v1.0.6 / 5.55.6](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.6) 版本中修复。

### 无法在资源管理器的搜索框中输入内容

问题：沙箱中的资源管理器搜索框无法获取焦点，也无法输入任何内容。

解决方法：已于 [v0.9.8c / 5.53.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.8c) 版本中修复。

### 沙箱中出现 “沙箱服务启动失败：BITS” 或 “请求启动服务 bits 被拒绝”

问题：自最近几个 Windows 10 版本后，BITS 服务似乎无法在沙箱中工作，因为其部分 WMI 功能被沙箱屏蔽。

解决方法：[v1.0.1 / 5.55.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.1) 版本已直接集成临时方案。

### 未找到你的问题

如需查找更多问题，请参阅 [GitHub 仓库](https://github.com/sandboxie-plus/Sandboxie)。