# Firefox 技巧

## Firefox 专属技巧

[沙盘控制](SandboxieControl.md) > [沙盘设置](SandboxSettings.md) > [应用程序 > Web 浏览器 > Firefox](ApplicationsSettings.md#firefox)

![](../Media/WebBrowserSettings2.png)

* * *

**始终在沙箱中运行**

*   设置：强制 Firefox 在此沙箱中运行

此设置指示沙盘自动监管每一个启动的 Firefox 实例，即使它并非通过沙盘的操作或命令直接启动。

* * *

**更新 Firefox 及其附加组件**

在默认配置下，任何针对 Firefox 或其附加组件的更新仅会发生在沙箱内。当该沙箱被删除时，所有这些更新也将被删除。为避免此问题，当你发现有更新可用时，应当在沙箱外运行 Firefox。让正常的 Firefox 完成更新，包括 Firefox 可能需要的重启。最后，退出 Firefox 并在沙盘下重新启动。

如果 Firefox 被强制始终在沙盘下运行（如上所述），请使用 [禁用强制程序](FileMenu.md#disable-forced-programs) 功能，在几分钟之内禁用强制沙箱。然后按照前述流程进行。最后，再次使用 _禁用强制程序_ 功能以恢复强制沙箱。

* * *

**书签、历史记录及收藏夹**

*   设置：允许直接访问 Firefox 书签与历史数据库

此设置允许在沙盘中运行的 Firefox 将书签存储在沙箱外，从而在沙箱被删除后仍能保留这些书签。如果未启用该选项，书签仅存储在沙箱中，并将在沙箱被删除时一同移除。

请注意，从 Firefox 3 开始，相同的文件（即 _places.sqlite_）同时存储书签和访问历史记录。因此，此设置将导致 Firefox 也会在沙箱外保存访问历史。

~~一种方案是安装 [PlainOldFavorites](https://www.iosart.com/firefox/plainoldfavorites) 附加组件，使 Firefox 能额外创建和管理类似 Internet Explorer 风格的收藏夹，并参阅 [Internet Explorer 技巧](InternetExplorerTips.md#favorites) 中关于收藏夹的讨论。~~

**结论建议：**

~~*   如果你不介意额外安装一个附加组件，可通过 PlainOldFavorites 为 Firefox 增添 Internet Explorer 风格的收藏夹，并参阅 [Internet Explorer 技巧](InternetExplorerTips.md) 的收藏夹处理建议。~~
*   如果你对 Firefox 的书签已感到满意，请勾选此设置。

* * *

**Cookies**

*   设置：允许直接访问 Firefox Cookies

此设置允许在沙盘中运行的 Firefox 将 cookie 文件存储于沙箱外（对应文件为 _cookies.sqlite_），从而在沙箱被删除后依然保留这些 cookies。若未启用该设置，cookies 仅保存在沙箱中，并会在沙箱删除时一同消失。

另一种做法是在正常环境下用 Firefox 访问你喜欢的网站一次，使这些网站将你的信息存入 cookies。然后再在沙盘下运行 Firefox，这样生成的新 cookies 只会保存于沙箱，待你删除沙箱时一同清理。

**结论建议：**

*   如果你习惯定期删除 cookies，并计划长期用沙盘，则可将此项保持未勾选，这样以后无需频繁手动删除 cookies
*   若需要让你在沙箱中访问的网站记住你，则应勾选此项

* * *

**反钓鱼数据库**

*   设置：允许直接访问 Firefox 反钓鱼数据库

此设置允许在沙盘中运行的 Firefox 更新和维护钓鱼网站数据库（对应文件名为 _urlclassifier*.sqlite_）。如果未启用此项，每当沙箱被删除，Firefox 可能需要花费时间重新将反钓鱼数据库（文件可能较大）拷贝进沙箱，并下载新数据库更新。此选项默认启用。

**结论建议：** 建议保持该选项勾选状态。

* * *

**完整资料夹访问权限**

*   设置：允许直接访问 Firefox 的完整配置文件文件夹

此设置允许在沙盘中运行的 Firefox 访问完整配置文件夹内的任意数据文件。包括上述所有 Firefox 数据文件，并覆盖早前讨论的所有“直接访问”相关设置。

**结论建议：** 建议不要勾选此项。

* * *

## 通用技巧

**自动删除沙箱**

[沙盘控制](SandboxieControl.md) > [沙盘设置](SandboxSettings.md) > [删除](DeleteSettings.md) > [调用方式](DeleteSettings.md#invocation)

![](../Media/DeleteInvocationSettings.png)

*   设置：自动删除沙箱内容

此设置指示沙盘在沙箱中所有程序全部退出后，自动删除该沙箱内容。

* * *

**高亮显示沙箱运行的程序窗口**

[沙盘控制](SandboxieControl.md) > [沙盘设置](SandboxSettings.md) > [外观设置](AppearanceSettings.md)

![](../Media/AppearanceSettings.png)

*   设置：在窗口周围显示边框

此设置指示沙盘为运行在沙箱内的程序窗口绘制彩色边框。默认颜色为黄色，你也可以为每个沙箱选择不同的颜色。

另外，如果你希望模糊沙盘监管程序与非沙盘程序的界限，可以选择“窗口标题不显示沙盘指示器”选项。