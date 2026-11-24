# 提示互联网访问 {#prompt-for-internet-access}

*PromptForInternetAccess* 允许 SandMan 在某个进程被 Sandboxie 的互联网访问限制阻止时提供一个交互式例外。提示本身并不是网络强制执行机制。

启用此设置不会创建互联网访问限制，也不会对普通的未受限网络活动弹出提示。必须已经对该进程实施封锁，才有可授予的例外。

<div id="configuration"></div>

## 配置

```ini
PromptForInternetAccess=y
PromptForInternetAccess=n
```

这是一项沙盒范围的布尔设置。它不接受按可执行文件限定的值。默认值为 `n`，即禁用交互式例外提示。

该设置于 Sandboxie Plus 0.5.0 引入。

<div id="when-the-prompt-appears"></div>

## 提示出现时机

只有在另一项 Sandboxie 策略已拒绝该进程的互联网或网络访问之后，该提示才会起作用。当前的强制执行路径包括 Windows 过滤平台（WFP）阻断，以及阻止访问与互联网相关的网络设备。

该对话框针对的是被阻止的进程，而不是逐个分类的远程目标。在 WFP 路径中，可能在创建套接字时、尚不知道远程目标之前就请求作出决定。因此，不应把它理解为对每个服务器、LAN 地址或连接的单独批准。

在询问是否应允许该进程访问互联网时，SandMan 会识别可执行文件并显示其完整路径。

<div id="prompt-choices"></div>

## 提示中的选项

| 选项 | 对当前进程的影响 | 持久配置 |
| --- | --- | --- |
| **是** | 为当前进程实例/PID 授予运行时互联网例外。 | 无。 |
| **否** | 不授予例外；现有封锁继续有效。 | 无。 |
| **是且添加到允许的程序** | 授予运行时例外。 | 把该可执行文件添加到现有的 `<InternetAccess>` 允许程序组。 |
| **终止** | 终止该进程。 | 无。 |

对于互联网访问提示，**记住对此进程的选择** 初始处于选中状态。它不是一个单独的允许或拒绝操作：它使 SandMan 对来自同一正在运行的进程实例的后续请求复用已选的 **是** 或 **否** 决定。记住的决定随该进程结束而失效，不会创建 `Sandboxie.ini` 规则。

只选择 **是** 同样是临时的。当需要把该可执行文件加入持久的互联网访问允许配置时，请使用 **是且添加到允许的程序**。

<div id="enforcement-behavior"></div>

## 强制执行行为

由底层的互联网访问限制继续负责强制执行，SandMan 仅处理例外决定：

- 在使用 WFP 阻断时，除非授予运行时例外，驱动程序与网络策略会继续阻断流量；
- 在使用网络设备封锁时，除非授予例外，受保护的设备打开操作会继续被拒绝。

如果 SandMan 无法给出决定，则不会授予例外，现有的阻止继续有效。仅仅等待提示并不会给该进程不受限制的网络访问。

该提示是一个例外工作流，而不是防火墙或完整的网络策略。允许程序模型参见 [限制设置](RestrictionsSettings.md#internet-access)，单独的网络强制执行机制参见 [WFP（Windows 过滤平台）支持](../PlusContent/WFPSupport.md)。

[*NotifyInternetAccessDenied*](NotifyInternetAccessDenied.md) 是独立的：它控制访问被拒绝时的通知，而 *PromptForInternetAccess* 可以提供例外。启用其中任一设置都不会自动启用另一项。

<div id="sandboxie-plus-interface"></div>

## Sandboxie Plus 界面

在 SandMan 中，请打开：

**沙盒选项** > **网络选项** > **程序限制**

复选框的标签为 **询问用户是否允许例外。** 当互联网访问设为不受限制的 **允许访问** 模式时，该复选框被禁用，因为没有已配置的封锁可供豁免。

在配置互联网访问封锁时，新建沙盒向导也会提供该提示选项。

<div id="runtime-changes"></div>

## 运行时更改

当被阻止的访问尝试需要作出决定时，会查询 *PromptForInternetAccess*。因此，更改该设置可以影响之后的被阻止访问事件，而无需重建沙盒，也无需重启 SandMan 或 Sandboxie 服务。

现有的运行时例外或为当前进程实例记住的决定，可能会使该进程不再弹出提示。通过 **是且添加到允许的程序** 进行的持久批准，会遵循常规的互联网访问允许程序配置。

<div id="sandboxie-plus-and-classic"></div>

## Sandboxie Plus 与 Classic

底层的网络与运行时机制是共享的，但当前的交互式提示由 SandMan 提供。源码审查未发现 Sandboxie Control Classic 中有处理该请求的等效当前处理程序。如果没有兼容的管理界面作出响应，则不会授予运行时例外，现有封锁继续有效。

<div id="version-history"></div>

## 版本历史

- Sandboxie Plus 0.5.0 / Classic 5.45.0 时期的代码引入了交互式互联网封锁例外机制。
- Sandboxie Plus 0.5.5 / Classic 5.46.4 添加了持久允许该程序的选项。
- Sandboxie Plus 1.14.2 把该提示选项加入新建沙盒向导。

这些历史上的对应版本并不意味着当前的 Classic 界面提供与 SandMan 相同的交互式提示。

<div id="related-settings"></div>

## 相关设置

- [限制设置](RestrictionsSettings.md#internet-access) — 配置互联网访问的允许/阻止模型
- [互联网访问被拒绝时通知](NotifyInternetAccessDenied.md) — 控制拒绝通知，而不是授予例外
- [WFP（Windows 过滤平台）支持](../PlusContent/WFPSupport.md) — 介绍 Sandboxie 单独的 WFP 强制执行
- [Sandboxie Ini](SandboxieIni.md) — 说明手动配置沙盒的方法
