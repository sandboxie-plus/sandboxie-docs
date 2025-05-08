# 配置菜单

[Sandboxie Control](SandboxieControl.md) > 配置菜单

![](../Media/ConfigureMenu.png)

* * *

### 程序警报

_程序警报_命令打开以下窗口，您可以在其中配置 Sandboxie，以便在特定程序在任何沙盒外启动时发出消息 [SBIE1301](SBIE1301.md)。

![](../Media/AlertPrograms.png)

* 使用_添加程序_按钮打开程序组窗口并选择要添加的程序。

* 例如，Internet Explorer 的 _iexplore.exe_，或 Firefox 的 _firefox.exe_。
* 或者，Internet Explorer 通常位于文件夹 _C:\Program Files\Internet Explorer_ 中。
* Mozilla Firefox 通常位于文件夹 _C:\Program Files\Mozilla Firefox_ 中。

如果所需程序已经在沙盒中运行，您也可以使用[程序设置](ProgramSettings.md#page-1)来指定应该为该程序发出消息 [SBIE1301](SBIE1301.md)。

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[AlertProcess](AlertProcess.md)。

* * *

### Windows Shell 集成

_Windows Shell 集成_命令打开一个窗口，控制 [Sandboxie Control](SandboxieControl.md) 如何集成到您的 Windows 桌面并与之关联。它还可以用于创建桌面快捷方式图标以在沙盒中运行您的程序。默认情况下，窗口中的所有设置都已启用。

![](../Media/ShellIntegration.png)

* 顶部框架指示 [Sandboxie Control](SandboxieControl.md) 何时应该启动：

* _当 Windows 启动时_将 [Sandboxie Control](SandboxieControl.md) 集成到启动序列中

* _当沙盒程序启动时_将在沙盒程序启动时启动 [Sandboxie Control](SandboxieControl.md)（如果它尚未运行）。这适用于通过 Sandboxie 显式启动的程序，例如使用[在沙盒中运行](SandboxMenu.md#sandbox-menu)命令或使用_添加快捷方式图标_创建的快捷方式（见下文）。它也适用于[强制程序](ProgramStartSettings.md#forced-programs)和[强制文件夹](ProgramStartSettings.md#forced-folders)。

* 中间框架处理快捷方式图标：

* _添加桌面快捷方式以在 Sandboxie 下启动 Web 浏览器_在选中时创建或在清除时删除桌面上的_沙盒化 Web 浏览器_快捷方式图标。

* _添加快速启动快捷方式以在 Sandboxie 下启动 Web 浏览器_在选中时创建或在清除时删除快速启动栏上的_沙盒化 Web 浏览器_快捷方式图标。快速启动栏通常位于 Windows 开始菜单按钮旁边。

* _添加快捷方式图标_在桌面上创建一个快捷方式图标，以在 Sandboxie 的监督下运行特定程序。该程序从 Sandboxie 开始菜单中选择。请注意，如果有任何程序安装到沙盒中，Sandboxie 开始菜单将包括安装期间创建的快捷方式，它们可用于创建桌面快捷方式。要删除使用_添加快捷方式图标_创建的桌面快捷方式，只需从桌面删除它们即可。

* 底部框架控制"右键单击"shell 集成：

* _为文件和文件夹添加右键单击操作"在沙盒中运行"_在选中时启用或在清除时删除当您在桌面或 Windows 资源管理器中的文件或文件夹上单击鼠标右键时出现的_在沙盒中运行_选项。

* _将沙盒添加为"发送到"操作的目标_在选中时启用或在清除时删除可用沙盒作为当您在桌面或 Windows 资源管理器中的文件或文件夹上单击鼠标右键时出现的_发送到_操作中的选项。如果启用此设置，[Sandboxie Control](SandboxieControl.md) 将在沙盒[创建](SandboxMenu.md#create-new-sandbox)或删除时自动更新_发送到_目标列表。

* * *

### 软件兼容性

_软件兼容性_命令打开一个窗口，显示可用兼容性模板列表。

* * *

### 忘记隐藏的消息

每当 [Sandboxie Control](SandboxieControl.md) 显示一个或多个 [SBIE 消息](SBIEMessages.md)时，您都可以选择隐藏该消息的未来实例。这是通过高亮并单击_隐藏_命令来实现的：

![](../Media/MessagesFromSandboxie.png)

请注意，消息仅按消息代码过滤。例如，上图显示了带有信息详情 _osk.exe_ 的消息 [SBIE1304](SBIE1304.md)。隐藏该消息将隐藏消息 SBIE1304 的所有未来实例，无论信息详情如何。

_忘记隐藏的消息_命令告诉 Sandboxie 停止过滤消息，并恢复显示所有发生的 SBIExxxx 消息。

* * *

### 提示

当 [Sandboxie Control](SandboxieControl.md) 显示警告或通知消息框时，它通常包含一个标记为_将来不要显示此消息_的复选框。如果您标记该复选框，将不再显示该特定消息。

_显示所有提示_命令告诉 Sandboxie 忽略复选框的任何此类使用，并恢复显示所有警告和通知。

_隐藏所有提示_命令告诉 Sandboxie 将所有复选框视为已选中，并且不显示任何警告或通知。

* * *

### 锁定配置

![](../Media/LockConfiguration.png)

请参阅[配置保护](ConfigurationProtection.md)。

* * *

### 编辑配置

打开系统文本编辑器（通常是 _Windows 记事本_）以编辑 [Sandboxie Ini](SandboxieIni.md) 配置文件。关闭编辑器时将自动调用_重新加载配置_命令。

注意：不建议手动编辑 Sandboxie.ini。建议您使用 [Sandboxie Control](SandboxieControl.md) 中的[沙盒设置](SandboxSettings.md)和其他配置窗口来对 Sandboxie 的配置进行任何更改。

注意：[Sandboxie Ini](SandboxieIni.md) 配置文件通常位于 _Windows_ 文件夹中，非特权用户账户无法修改。如果您使用带有用户账户控制 (UAC) 的 Windows，您可能必须先提升到管理员账户才能修改 Sandboxie.ini。

* * *

### 重新加载配置

强制 Sandboxie 从 [Sandboxie Ini](SandboxieIni.md) 配置文件重新加载其配置。

* * *

转到 [Sandboxie Control](SandboxieControl.md#menus)、[帮助主题](HelpTopics.md)。 