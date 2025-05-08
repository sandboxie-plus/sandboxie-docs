# Firefox 使用技巧

## Firefox 特定技巧

[Sandboxie 控制](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [应用程序 > Web 浏览器 > Firefox](ApplicationsSettings.md#firefox)

![](../Media/WebBrowserSettings2.png)

* * *

**始终在沙盒中运行**

* 设置：强制 Firefox 在此沙盒中运行

此设置告诉 Sandboxie 在 Firefox 启动时自动监督其任何实例，即使它不是直接通过 Sandboxie 工具或命令启动的。

* * *

**更新 Firefox 及其附加组件**

在默认配置下，Firefox 或其附加组件的任何更新都只会在沙盒内进行。当删除沙盒时，所有此类更新也将被删除。为避免此问题，当您发现有任何可用更新时，应在沙盒外运行 Firefox。让普通的 Firefox 完成更新，包括任何必要的 Firefox 重启。最后，退出 Firefox 并在 Sandboxie 下重新启动它。

如果 Firefox 被强制始终在 Sandboxie 下运行（如上所述），请使用[禁用强制程序](FileMenu.md#disable-forced-programs)命令来禁用强制沙盒化几分钟。然后按照上一段中的步骤操作。最后，再次使用_禁用强制程序_命令恢复强制沙盒化。

* * *

**书签、历史记录和收藏夹**

* 设置：允许直接访问 Firefox 书签和历史数据库

此设置允许在 Sandboxie 下运行的 Firefox 在沙盒外存储书签，这样即使在删除沙盒后它们也能保持。当未设置此选项时，书签仅存储在沙盒中，并将在删除沙盒时被删除。

请注意，从 Firefox 3 开始，同一个文件（称为 _places.sqlite_）同时存储书签和访问过的网站历史记录。因此，此设置也会导致 Firefox 在沙盒外存储访问历史记录。

~~一种方法是安装 [PlainOldFavorites](https://www.iosart.com/firefox/plainoldfavorites) 附加组件，它让 Firefox 除了 Mozilla 风格的书签外，还可以创建和管理 Internet Explorer 风格的收藏夹。然后参考 [Internet Explorer 使用技巧](InternetExplorerTips.md#favorites)中关于收藏夹的讨论。~~

**总结：**

~~* 如果您不介意额外的附加组件，请安装 PlainOldFavorites 来为 Firefox 添加 Internet Explorer 风格的收藏夹功能，然后阅读 [Internet Explorer 使用技巧](InternetExplorerTips.md)中处理收藏夹的建议。~~
* 如果您对 Firefox 书签感到满意，那么请选择此设置。

* * *

**Cookie**

* 设置：允许直接访问 Firefox cookie

此设置允许在 Sandboxie 下运行的 Firefox 在沙盒外存储 cookie（在一个名为 _cookies.sqlite_ 的文件中），这样即使在删除沙盒后它们也能保持。当未设置此选项时，cookie 仅存储在沙盒中，并将在删除沙盒时被删除。

另一种方法是使用普通的 Firefox 访问一次您喜欢的网站，让这些网站在其 cookie 中记住您。然后切换到 Sandboxie 下的 Firefox，这样任何新的 cookie 都会保持在沙盒中，直到您删除沙盒。

**总结：**

* 如果您经常删除 cookie，并计划开始经常使用 Sandboxie，那么您可以保持此设置未选中，这样您就不必继续经常删除 cookie。
* 如果您需要在沙盒化 Firefox 中访问的网站记住您，那么请选择此设置。

* * *

**钓鱼数据库**

* 设置：允许直接访问 Firefox 钓鱼数据库

此设置允许在 Sandboxie 下运行的 Firefox 更新和维护钓鱼网站数据库（一个名为 _urlclassifier*.sqlite_ 的文件）。当未设置此选项时，每当删除沙盒时，Firefox 可能需要花时间将钓鱼数据库（可能是一个非常大的文件）复制到沙盒中，然后下载数据库更新。此设置默认启用。

**总结：**保持此设置选中。

* * *

**完整配置文件访问**

* 设置：允许直接访问整个 Firefox 配置文件文件夹

此设置允许在 Sandboxie 下运行的 Firefox 访问整个 Firefox 配置文件中的任何数据文件。此设置包括上面提到的任何其他 Firefox 数据文件，并覆盖前面讨论的所有其他"直接访问"设置。

**总结：**不要选择此设置。

* * *

## 通用技巧

**自动删除沙盒**

[Sandboxie 控制](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [删除](DeleteSettings.md) > [调用](DeleteSettings.md#invocation)

![](../Media/DeleteInvocationSettings.png)

* 设置：自动删除沙盒内容

此设置告诉 Sandboxie 在沙盒中的所有程序停止运行时删除沙盒。

* * *

**高亮显示在 Sandboxie 下运行的程序窗口**

[Sandboxie 控制](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > [外观设置](AppearanceSettings.md)

![](../Media/AppearanceSettings.png)

* 设置：在窗口周围显示边框

此设置告诉 Sandboxie 在属于此沙盒中运行的程序的窗口周围绘制彩色边框。默认颜色是黄色，但您可以为每个沙盒选择不同的颜色。

或者，如果您希望模糊在 Sandboxie 监督下运行的程序与未运行的程序之间的区别，请选择"不在窗口标题中显示 Sandboxie 指示器"设置。 