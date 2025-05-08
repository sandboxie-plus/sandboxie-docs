# Internet Explorer 提示

## Internet Explorer 特定提示

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [应用程序 > Web 浏览器 > Internet Explorer](ApplicationsSettings.md#web-browser)

![](../Media/WebBrowserSettings1.png)

* * *

#### 始终在沙盒中运行

* 设置：强制 Internet Explorer 在此沙盒中运行

此设置告诉 Sandboxie 在 Internet Explorer 启动时自动监督其任何实例，即使它不是通过 Sandboxie 功能或命令直接启动的。

* * *

#### 启用 UAC 的 Internet Explorer

在启用 UAC 的 Windows Vista/7/8/8.1 中，Internet Explorer 维护两组配置：普通配置和管理员配置。每组都包含自己的 cookie、主页和其他一些设置。当您正常启动 Internet Explorer 时，您会获得普通配置。当您右键单击 Internet Explorer 并选择_以管理员身份运行_操作时，您会获得管理员配置。

在 Sandboxie 下，Internet Explorer 选择管理员配置。（但 Internet Explorer 在 Sandboxie 下不一定以管理员身份运行。）要微调管理员配置，请在沙盒外运行 Internet Explorer 时使用_以管理员身份运行_右键操作。

* * *

#### Windows XP 上的 Windows Update

当您希望访问 Windows Update 网站时，应该在沙盒外运行 Internet Explorer。如果 Internet Explorer 被强制始终在 Sandboxie 下运行（如上所述），则在访问 Windows Update 网站之前和之后使用[禁用强制程序](FileMenu.md#disable-forced-programs)命令来禁用强制沙盒化。

请注意，Windows 中的自动更新功能不依赖于 Internet Explorer，不应受到任何与 Internet Explorer 相关的 Sandboxie 设置的影响。同样，Windows Vista 中的 Windows 更新窗口也不依赖于 Internet Explorer，也不受 Sandboxie 的影响。

* * *

#### 收藏夹

* 设置：允许直接访问 Internet Explorer 收藏夹
* 设置：将 Internet Explorer 收藏夹添加到快速恢复文件夹

这些设置允许在 Sandboxie 下运行的 Internet Explorer 将收藏夹存储在沙盒外，这样即使在删除沙盒后它们也能保留。当未设置此选项时，收藏夹仅存储在沙盒中，并在删除沙盒时被删除。

第一个设置（直接访问）将收藏夹直接存储在沙盒外。第二个设置（[快速恢复](QuickRecovery.md)）最初将收藏夹保留在沙盒中，但在添加新收藏夹时提供恢复（移出沙盒）功能。

第一个设置更灵活，因为您可以自由添加、编辑和删除收藏夹。第二个设置更安全，但代价是牺牲了一些便利性。

**底线：** 为了更大的便利性，选择设置"允许直接访问 Internet Explorer 收藏夹"。

* * *

#### Cookie

* 设置：允许直接访问 Internet Explorer cookie

此设置允许在 Sandboxie 下运行的 Internet Explorer 将 cookie 存储在沙盒外，这样即使在删除沙盒后它们也能保留。当未设置此选项时，cookie 仅存储在沙盒中，并在删除沙盒时被删除。

此设置的另一种方法是使用普通的 Internet Explorer 访问您喜欢的网站一次，让这些网站在其 cookie 中记住您。然后切换到 Sandboxie 下的 Internet Explorer，这样任何新的 cookie 都会保留在沙盒中，直到您删除沙盒。

**底线：**

* 如果您定期删除 cookie，并计划开始定期使用 Sandboxie，那么您可以保持此设置未选中，这样您就不必定期删除 cookie。
* 如果您需要您在沙盒化 Internet Explorer 中访问的网站记住您，则选择此设置。

* * *

#### 源

* 设置：允许直接访问 Internet Explorer 源

此设置允许在 Sandboxie 下运行的 Internet Explorer 将源链接存储在沙盒外，这样即使在删除沙盒后它们也能保留。当未设置此选项时，源链接仅存储在沙盒中，并在删除沙盒时被删除。

Internet Explorer 定期从在 Web 浏览器外运行的组件检查其源。当此设置未生效时，该组件将看不到（也不会检查或刷新）在沙盒中创建的源。（从技术上讲，该组件是一个计划任务。每当您在 Internet 选项对话框中使用源设置选项卡时，都会创建和更改该任务。）

**底线：** 如果您使用 Internet Explorer 源，建议您选择此设置。

* * *

#### 在沙盒外保存

* 设置：在沙盒外保存：搜索字符串和已调用命令的历史记录。
* ~~设置：在沙盒外保存：Hotmail 和 Messenger 的账户信息。~~（自 Sandboxie v0.8.0 / 5.50.0 起被 [OpenCredentials](OpenCredentials.md) 替换）

第一个设置允许在 Sandboxie 下运行的 Internet Explorer 存储"自动完成"信息，通常用于保存历史记录：搜索字符串的历史记录，或输入到输入框中的命令的历史记录。

~~第二个设置允许在 Sandboxie 下运行的 Internet Explorer 存储"凭据"信息，通常由 Microsoft 网站（如 Hotmail）使用，以记住您的 Windows Live ID。它也由 Windows (Live) Messenger 使用。~~

**底线：** 这些设置更关注隐私而不是安全性。您输入到网站的信息可以永久保存（就像普通浏览器一样）或仅在您删除沙盒之前保存。要永久保存，请选择这些设置。否则，保持设置未选中。

* * *

## 一般提示

#### 自动删除沙盒

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [删除](DeleteSettings.md) > [调用](DeleteSettings.md#invocation)

![](../Media/DeleteInvocationSettings.png)

* 设置：自动删除沙盒内容

此设置告诉 Sandboxie 在沙盒中的所有程序停止运行时删除沙盒。

* * *

#### 突出显示在 Sandboxie 下运行的程序窗口

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [外观设置](AppearanceSettings.md)

![](../Media/AppearanceSettings.png)

* 设置：在窗口周围显示边框

此设置告诉 Sandboxie 在属于在此沙盒中运行的程序窗口周围绘制彩色边框。默认颜色是黄色，但您可以为每个沙盒选择不同的颜色。

或者，如果您希望模糊在 Sandboxie 监督下运行的程序与未在监督下运行的程序之间的区别，请选择设置"不在窗口标题中显示 Sandboxie 指示器"。 