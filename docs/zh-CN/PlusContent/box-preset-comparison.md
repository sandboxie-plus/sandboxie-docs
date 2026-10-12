Sandboxie Plus 提供六种基础沙盒类型，并可选择组合启用加密与保密功能。

沙盒通常用于将主机系统与在沙盒内运行的进程隔离，防止这些进程对计算机中的其他程序和数据进行永久更改。隔离级别会影响您的 [安全性](../PlusContent/security-mode.md) 以及与应用程序的 [兼容性](../PlusContent/compartment-mode.md)。
Sandboxie Plus 还可 [保护您的个人数据](../PlusContent/privacy-mode.md)，防止运行在其监管下的进程访问这些数据。

Sandboxie Plus 还可组合使用[加密沙盒存储](../PlusContent/BoxEncryption.md)和[保密沙盒](../Content/ConfidentialBox.md)保护，后者限制相关的沙盒外宿主机进程通过句柄访问沙盒内的进程和线程。[挂载后的根目录保护（英文）](https://sandboxie-plus.github.io/sandboxie-docs/PlusContent/BoxEncryption/#root-protection-while-mounted)是独立的文件系统保护选项。向导中的组合选项见[黑色沙盒](../PlusContent/black-box.md)。

下表列出六种基础类型的常规配置。“应用程序隔离”表示对应模式，并非一般意义上的兼容性评级。颜色和图标仅用于区分外观，不能保证沙盒实际生效的设置与之相符。

| 沙盒类型 | [安全强化](../PlusContent/security-mode.md) | [数据保护](../PlusContent/privacy-mode.md) | [应用程序隔离](../PlusContent/compartment-mode.md) |
|-|-|-|-|
|![](../Media/sandbox-r-full.png) 红色沙盒（带数据保护的安全加固沙盒）|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|
|![](../Media/sandbox-o-full.png) 橙色沙盒（安全加固沙盒）|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|
|![](../Media/sandbox-b-full.png) 蓝色沙盒（带数据保护的沙盒）|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|
|![](../Media/sandbox-y-full-e1684328804872.png) 黄色沙盒（标准沙盒）|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|
|![](../Media/sandbox-c-full.png) 青色沙盒（带数据保护的应用程序隔离沙盒）|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是|
|![](../Media/sandbox-g-full.png) 绿色沙盒（应用程序隔离沙盒）|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) 否|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) 是|

## 加密与保密选项

新建沙盒向导中的“加密沙盒内容并启用保密功能”选项可与六种基础类型中的任意一种组合使用。在常规向导流程中，它会保留所选基础配置，并添加 `UseFileImage=y` 和 `ConfidentialBox=y`。

| 功能 | 黑色沙盒选项 |
|-|-|
| [加密存储](BoxEncryption.md) | 是 |
| [进程保密保护](../Content/ConfidentialBox.md) | 是 |
| 安全强化 / 数据保护 / 应用程序隔离模式 | 保留所选基础类型的配置 |

![黑色沙盒类型图标](../Media/sandbox-k-full.png) SandMan 可用此深色图标表示加密与保密的组合。它不代表某一种固定的基础模式，也不意味着边框为黑色。外观设置详见[沙盒外观](../Content/BoxPresentation.md)。
