# 已知冲突

* * *
已知冲突可以通过在“沙箱设置 > 应用程序”或“沙箱选项 > 应用模板”（Plus 版本）中启用对应的应用配置来解决。
* * *

### 并非所有程序都能在沙箱中安装或运行

问题：某些调用服务或驱动程序的应用程序可能无法在沙箱中安装或运行。

解决方案 #1：你可能与系统中安装的第三方安全软件存在冲突（参见问题 [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647) 和 [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293)）。想了解更多可能有关的安全套件，可以查看 [归档论坛](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539)。

解决方案 #2：如果你已经尝试在一个新建的空沙箱中安装该应用，但仍失败，请改为先在宿主系统中安装，然后再以沙箱方式运行。

如果问题仍然存在，尤其是之前在旧版沙盘能运行的程序，请在 [GitHub 项目](https://github.com/sandboxie-plus/Sandboxie/issues) 中提交详细信息。

### Microsoft Store 应用

问题：Microsoft Store 的应用在 Sandboxie Classic 和 Sandboxie Plus 中无法运行。

解决方案：目前无解。请关注问题 [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) 了解后续更新。

### Office 2013/2016/2019 与 Office 365（仅限 C2R 版本）

问题：Microsoft Office 2013, 2016, 2019 及 Office 365 的 Click to Run 版本（包括 Outlook 2013 及以上）在沙箱中会崩溃。

解决方案：在 [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7) 中已修复该问题。

### Office 2021

问题：Office 2021 无法在沙箱中安装。

解决方案：目前无解。请关注问题 [#1675](https://github.com/sandboxie-plus/Sandboxie/issues/1675) 或 [#1900](https://github.com/sandboxie-plus/Sandboxie/issues/1900) 了解后续更新。

### Tor 浏览器

问题：Tor 浏览器在沙箱中运行很慢，容易崩溃，或运行一段时间后崩溃。

解决方案：该问题已在 [v1.0.21 / 5.55.21](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.21) 中修复。

### HP 通用打印驱动

问题：从沙箱中的网页浏览器打印时，HP 通用打印机的状态弹窗组件无法正常运行。

解决方案：打开“沙箱设置 > 资源访问 > COM 访问”，点击“添加”，输入以下资源名：
`{D713F357-7920-4B91-9EB6-49054709EC7A}`

### Microsoft Edge 的自动删除功能

问题：Microsoft Edge 的自动删除功能失效。

解决方案：Edge 默认启用了“系统”设置中的“启动加速”选项，这会阻止 Edge 完全关闭。建议关闭该选项，或安装已修复此问题的 [v1.1.2 / 5.56.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.1.2) 或更高版本。

### Steam 游戏

问题：并非所有 Steam 游戏都能在沙箱中运行。

解决方案：建议将游戏直接安装在宿主系统中，大部分游戏可以正常运行。但也有[已知问题报告](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue)，有些游戏就是无法运行。遇到问题时，请确保 Steam 客户端是最新版本。建议在宿主系统中运行 Steam 并安装游戏，然后在游戏快捷方式上点击右键选择“沙箱中运行”作为替代方法。如果问题依旧，请在 [GitHub 项目](https://github.com/sandboxie-plus/Sandboxie/issues) 提交详细信息。

### GOG 游戏与 Galaxy Beta

问题：来自 GOG Galaxy 的游戏可能无法在沙箱中运行。

解决方案：[#1246](https://github.com/sandboxie-plus/Sandboxie/issues/1246) 中提供了一个部分解决方法。你可以“强制” GOG 的程序目录，使其在沙箱中能正确运行。另请参阅：[ForceFolder](ForceFolder.md)。

### Windows 11 中无法访问麦克风或摄像头

问题：在 Windows 11 系统中的任意沙箱里无法访问麦克风或摄像头。

解决方案：[#1669](https://github.com/sandboxie-plus/Sandboxie/issues/1669) 中提供了一个临时方法，但尚无永久解决方案。

### Chromium 浏览器的标签页有时无法恢复

问题：当 Chromium 浏览器在沙箱外运行时，标签页会丢失。

解决方案：目前没有修复，但在 [#558](https://github.com/sandboxie-plus/Sandboxie/issues/558) 中有部分替代方案。

### Windows 资源管理器打开文件夹、驱动器或右键菜单时很慢

问题：在 Windows 10 和 11 上，沙箱中的 Windows 资源管理器打开速度很慢。

解决方案：尚无修复，请参阅 [#69](https://github.com/sandboxie-plus/Sandboxie/issues/69)。

### “使用其他应用打开”对话框在沙箱中的文件管理器里无法使用

问题：“使用其他应用打开”功能在沙箱中无法使用。

解决方案：该问题已在 [v1.0.6 / 5.55.6](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.6) 中修复。

### 文件资源管理器中的搜索框无法使用

问题：在沙箱中，文件资源管理器的搜索框无法获得焦点，也无法输入内容。

解决方案：该问题已在 [v0.9.8c / 5.53.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.8c) 中修复。

### 出现“沙箱服务启动失败：BITS”或“启动 BITS 服务的请求被拒绝”等提示

问题：从某些 Windows 10 版本开始，BITS 服务似乎已损坏，因为它依赖 WMI 的某些功能，而这些在沙箱中被阻止了。

解决方案：[v1.0.1 / 5.55.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.1) 中已加入替代方法解决。

### 找不到你的问题？

如需查找更多问题，请访问 [GitHub 项目](https://github.com/sandboxie-plus/Sandboxie)。
