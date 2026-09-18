# Internet Explorer 使用技巧

## Internet Explorer 专属提示

[沙盒管理器](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [应用程序 > Web 浏览器 > Internet Explorer](ApplicationsSettings.md#web-浏览器)

![](../Media/WebBrowserSettings1.png)

* * *

#### 总是以沙盒方式运行

*   设置：强制 Internet Explorer 在此沙盒中运行

此设置让 Sandboxie 自动监管 Internet Explorer 启动的任何实例，即使它不是通过 Sandboxie 的设施或命令直接启动的。

* * *

#### 启用 UAC 的 Internet Explorer

在启用 UAC 的 Windows Vista/7/8/8.1 中，Internet Explorer 维护两套配置：普通配置和管理员配置。每套配置都有自己的 Cookie、主页和一些其他设置。正常启动 Internet Explorer 时，你得到的是普通配置。右键点击 Internet Explorer 并选择 _以管理员身份运行_ 操作时，你得到的是管理员配置。

在 Sandboxie 下，Internet Explorer 会选择管理员配置。（但 Internet Explorer 在 Sandboxie 下不一定以管理员身份运行。）要微调管理员配置，请在沙盒外运行 Internet Explorer 时使用 _以管理员身份运行_ 右键操作。

* * *

#### Windows XP 下的 Windows Update

当你想访问 Windows Update 网站时，应该在沙盒外运行 Internet Explorer。如果 Internet Explorer 被强制始终在 Sandboxie 下运行（如上所述），请在访问 Windows Update 网站之前和之后，使用 [禁用强制程序](FileMenu.md#禁用强制程序) 命令禁用强制沙盒化。

注意：Windows 的自动更新功能不依赖 Internet Explorer，不应受任何与 Internet Explorer 相关的 Sandboxie 设置影响。同样，Windows Vista 中的 Windows 更新窗口也不依赖 Internet Explorer，同样不受 Sandboxie 影响。

* * *

#### 收藏夹

*   设置：允许直接访问 Internet Explorer 收藏夹
*   设置：将 Internet Explorer 收藏夹添加到快速恢复文件夹

这些设置允许在 Sandboxie 下运行的 Internet Explorer 把收藏夹存储在沙盒外，因此即使在沙盒被删除后它们也能保留。当未设置此选项时，收藏夹只存储在沙盒中，沙盒被删除时会被删除。

第一个设置（直接访问）把收藏夹直接存储在沙盒外。第二个设置（[快速恢复](QuickRecovery.md)）最初把收藏夹保留在沙盒中，但随着新收藏夹的添加，会提供恢复（移出沙盒）选项。

第一个设置更灵活，你可以自由地添加、编辑和删除收藏夹。第二个设置更安全，但以牺牲一些便利为代价。

**底线：** 为获得更大便利，请选择“允许直接访问 Internet Explorer 收藏夹”设置。

* * *

#### Cookie

*   设置：允许直接访问 Internet Explorer Cookie

此设置允许在 Sandboxie 下运行的 Internet Explorer 把 Cookie 存储在沙盒外，因此即使在沙盒被删除后它们也能保留。当未设置此选项时，Cookie 只存储在沙盒中，沙盒被删除时会被删除。

此设置的替代方法是：先用普通的 Internet Explorer 访问一次你最喜欢的网站，让这些网站通过 Cookie 记住你。然后切换到 Sandboxie 下的 Internet Explorer，这样任何新 Cookie 都会保留在沙盒中，直到你删除沙盒。

**底线：**

*   如果你经常删除 Cookie，并计划开始经常使用 Sandboxie，那么可以保持此设置不选中，这样你就不必继续经常删除 Cookie。
*   如果你需要沙盒化 Internet Explorer 中访问的网站记住你，请选中此设置。

* * *

#### 订阅源

*   设置：允许直接访问 Internet Explorer 订阅源

此设置允许在 Sandboxie 下运行的 Internet Explorer 把订阅源链接存储在沙盒外，因此即使在沙盒被删除后它们也能保留。当未设置此选项时，订阅源链接只存储在沙盒中，沙盒被删除时会被删除。

Internet Explorer 通过一个在浏览器之外运行的组件定期检查其订阅源。当此设置未生效时，该组件将看不到（也不会检查或刷新）在沙盒中创建的订阅源。（从技术上讲，该组件是一个计划任务。每当你使用 Internet 选项对话框中的“订阅源设置”选项卡时，该任务就会被创建和更改。）

**底线：** 如果你使用 Internet Explorer 订阅源，建议选中此设置。

* * *

#### 在沙盒外保存

*   设置：在沙盒外保存：搜索字符串和已调用命令的历史记录。
*   ~~设置：在沙盒外保存：Hotmail 和 Messenger 的帐户信息。~~（自 Sandboxie v0.8.0 / 5.50.0 起由 [开放凭据](OpenCredentials.md) 取代）

第一个设置允许在 Sandboxie 下运行的 Internet Explorer 存储“自动完成”信息，它通常用于保留历史记录：搜索字符串的历史记录，或在输入框中输入的命令的历史记录。

~~第二个设置允许在 Sandboxie 下运行的 Internet Explorer 存储“凭据”信息，Microsoft 网站（如 Hotmail）通常使用它来记住你的 Windows Live ID。Windows（Live）Messenger 也使用它。~~

**底线：** 这些设置更多关乎隐私而非安全。你在网站上输入的信息可以被永久保留（就像普通浏览器一样），也可以只保留到删除沙盒为止。要永久保留，请选中这些设置。否则，保持这些设置不选中。

* * *

## 通用提示

#### 自动删除沙盒

[沙盒管理器](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [删除](DeleteSettings.md) > [调用方式](DeleteSettings.md#调用方式)

![](../Media/DeleteInvocationSettings.png)

*   设置：自动删除沙盒内容

此设置让 Sandboxie 在沙盒中的所有程序停止运行时删除沙盒。

* * *

#### 高亮显示在 Sandboxie 下运行的程序窗口

[沙盒管理器](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [外观设置](AppearanceSettings.md)

![](../Media/AppearanceSettings.png)

*   设置：在窗口周围显示边框

此设置让 Sandboxie 在属于此沙盒中运行程序的窗口周围绘制彩色边框。默认颜色是黄色，但你可以为每个沙盒选择不同的颜色。

或者，如果你希望模糊在 Sandboxie 监管下运行的程序与未在其监管下运行的程序之间的区别，请选择“不在窗口标题中显示 Sandboxie 指示符”设置。
