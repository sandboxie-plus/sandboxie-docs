# 通知设置 {#notification-settings}

Sandboxie 的通知设置通常控制特定事件发生时是否生成 SBIE 消息。它们不改变允许或拒绝该操作的策略。例如，禁用 `NotifyInternetAccessDenied` 会抑制其拒绝消息；它不会授予互联网访问权限。

消息的生成也与呈现相互独立。SandMan 或 Sandboxie Control Classic 会按各自的呈现设置，把生成的消息显示在日志、弹窗或其他界面中。只有部分通知设置具有专门的用户界面控件。

本页的设置由多个 Sandboxie 组件实现，而不是一个统一的通知子系统。有些设置在沙盒化进程初始化时被缓存，另一些则在事件发生时读取。这里涉及的布尔设置都没有可执行文件限定的语法。

典型的沙盒设置：

```ini
[DefaultBox]
NotifyInternetAccessDenied=y
```

典型的全局设置：

```ini
[GlobalSettings]
NotifyForceProcessEnabled=y
```

<div id="reference"></div>

## 参考

| 设置 | 默认值 | 范围 | 触发条件或消息 | 应用更改 / 界面说明 |
| --- | --- | --- | --- | --- |
| `AlwaysShowReminder` | `n` | 全局 | 支持/提醒对话框的调度；不是 SBIE 事件消息 | 参见 [支持提醒](#support-reminder)。 |
| `NotifyBoxProtected` | `n` | 受保护沙盒 | 当宿主进程被拒绝访问受保护的沙盒化进程时产生 SBIE1318 | 事件发生时读取；SandMan 复选框目前只更改这一项设置。 |
| `NotifyDirectDiskAccess` | `n` | 沙盒 | 某些被拒绝的直接打开磁盘设备的尝试产生 [SBIE1313](SBIE1313.md)；并非每一次被拒绝的磁盘访问请求 | 在沙盒化进程内缓存。例外情况参见 [直接磁盘访问时通知](NotifyDirectDiskAccess.md)。 |
| `NotifyForceProcessDisabled` | `n` | 全局 | 当匹配强制规则的进程因强制被临时禁用而未被强制时产生 [SBIE1301](SBIE1301.md) | 事件发生时读取；全局程序警报复选框。 |
| `NotifyForceProcessEnabled` | `n` | 全局 | 当进程匹配强制规则并被分配到某个沙盒时产生 SBIE1321 | 事件发生时读取；全局程序警报复选框。 |
| `NotifyImageLoadDenied` | `y` | 沙盒 | 当 [保护主机镜像](ProtectHostImages.md) 阻止沙盒内的映像或 DLL 映射到受保护的主机映像进程时产生 SBIE1305 | 事件发生时读取；SandMan 复选框。 |
| `NotifyInternetAccessDenied` | `y` | 沙盒 | 当 Sandboxie 的互联网访问策略拒绝某个进程时产生 [SBIE1307](SBIE1307.md)；通常每个受影响进程只产生一次 | 在进程内缓存。参见 [互联网访问被拒绝时通知](NotifyInternetAccessDenied.md)。 |
| `NotifyMsiInstaller` | `y` | 沙盒 | 当 MSI 安装程序启动时未启用推荐的 [MSI 安装程序豁免](MsiInstallerExemptions.md) 行为，产生 SBIE2194 | 在进程启动期间求值。未找到专门的 SandMan 复选框。 |
| `NotifyNoCopy` | `n` | 沙盒 | 针对有文档记载的文件迁移情形产生 SBIE2113、SBIE2114 或 SBIE2115 | 在进程内缓存。参见 [不复制通知](NotifyNoCopy.md)。 |
| `NotifyProcessAccessDenied` | `n` | 沙盒 | 受支持的显式进程或线程访问请求被 Sandboxie 的保护路径拒绝时产生 [SBIE2111](SBIE2111.md) | 在进程内缓存。参见 [进程访问被拒绝时通知](NotifyProcessAccessDenied.md)。 |
| `NotifyRootProtected` | `n` | 全局 | 当另一进程或沙盒对受保护的沙盒根目录的访问被拒绝时产生 SBIE1317 | 拒绝发生时读取。该设置没有可用的专门 SandMan 复选框。 |
| `NotifyStartRunAccessDenied` | `y` | 沙盒 | 当该沙盒的启动/运行限制机制拒绝相关操作时产生 [SBIE1308](SBIE1308.md)；通常每个受影响进程只产生一次 | 在进程内缓存。参见 [启动/运行访问被拒绝时通知](NotifyStartRunAccessDenied.md)。 |
| `AlertStartRunAccessDenied` | `y` | 全局 | 由独立的全局程序警报拒绝路径产生 [SBIE1308](SBIE1308.md) | 事件发生时读取；全局程序警报复选框；与 `NotifyStartRunAccessDenied` 相互独立。 |

<div id="policy-generation-and-presentation"></div>

## 策略、生成与呈现

通知设置只控制消息的生成。它不会禁用底层的磁盘、网络、进程、启动、映像加载或沙盒保护规则。同样，`NotifyForceProcessDisabled` 与 `NotifyForceProcessEnabled` 报告的是强制机制所做的决定；它们不会开启或关闭强制。

组件生成 SBIE 消息之后，由 SandMan 或 Sandboxie Control Classic 决定如何呈现它。SandMan 的通用弹窗与消息日志选项位于 **全局设置 > 常规选项 > 消息通知**。抑制弹窗与禁用源消息的生成是两件不同的事。

SandMan 的复选框 **当沙盒外程序尝试访问沙盒根目录或沙盒化进程对象时，发出 SBIE1318 / SBIE1317 警告** 比它当前的配置处理范围更宽：它读写的是 `NotifyBoxProtected`，该设置控制 SBIE1318。`NotifyRootProtected` 单独控制 SBIE1317，在当前界面中没有可用的专门复选框。

`NotifyImageLoadDenied` 同样与强制执行相互独立。关闭它的消息不会禁用 [保护主机镜像](ProtectHostImages.md)，而且该消息专门针对被这项保护拒绝的映像映射，而不是每一次失败的 DLL 加载。

`NotifyMsiInstaller` 并不报告每一次 MSI 启动。当安装程序启动时未启用推荐的 [MSI 安装程序豁免](MsiInstallerExemptions.md) 行为，它才会发出警告。它与其他 MSI 或 COM 失败消息相互独立。

<div id="applying-changes"></div>

## 应用更改

更改那些缓存在进程状态中的设置后，请重启受影响的沙盒化进程：

- `NotifyDirectDiskAccess`
- `NotifyInternetAccessDenied`
- `NotifyNoCopy`
- `NotifyProcessAccessDenied`
- `NotifyStartRunAccessDenied`

以下设置在事件发生时才会被查询，因此在常规配置更新或重新加载之后即可影响后续事件，无需重建受影响的进程状态：

- `NotifyBoxProtected`
- `NotifyImageLoadDenied`
- `NotifyRootProtected`
- `NotifyForceProcessDisabled`
- `NotifyForceProcessEnabled`
- `AlertStartRunAccessDenied`

同时更改多个通知设置时，重启受影响的进程树仍是最可预测的做法。

<div id="startrun-messages-and-confirmation"></div>

## 启动/运行消息与确认

`NotifyStartRunAccessDenied` 与 `AlertStartRunAccessDenied` 是彼此独立的设置。两者都可能产生 SBIE1308，但它们由不同的拒绝路径使用。禁用其中任一设置只会抑制对应的消息；它不会撤销拒绝。

[启动前警报](AlertBeforeStart.md) 则不同。它可以在符合条件的沙盒启动之前请求确认，而用户的回答可以决定该启动是否继续。它不只是一个用于抑制信息性 SBIE 消息的开关。

<div id="support-reminder"></div>

## 支持提醒

`AlwaysShowReminder` 是一项全局设置，影响 Sandboxie 支持/提醒对话框的调度。它默认为 `n`，不生成 SBIE 事件消息，也不参与允许/拒绝策略。

<div id="user-interface-availability"></div>

## 用户界面可用性

SandMan 提供以下控件：

- **沙盒选项 > 常规选项 > 文件选项 > “磁盘/文件”访问权限 > 有程序打开硬盘句柄时警示** 控制 `NotifyDirectDiskAccess`。
- **沙盒选项 > 网络选项 > 访问 > 程序被拒绝访问网络时，提示问题代码 SBIE1307** 控制 `NotifyInternetAccessDenied`。
- **沙盒选项 > 常规选项 > 限制选项 > 其它限制 > 进程被拒绝访问非沙盒进程内存时，提示问题代码 SBIE2111** 控制 `NotifyProcessAccessDenied`。
- **沙盒选项 > 程序控制 > 启动限制 > 程序启动失败时，提示问题代码 SBIE1308** 控制 `NotifyStartRunAccessDenied`。
- **沙盒选项 > 安全选项 > 沙盒保护 > 当沙盒外程序尝试访问沙盒根目录或沙盒化进程对象时，发出 SBIE1318 / SBIE1317 警告** 控制 `NotifyBoxProtected`。尽管标签如此，它并不保存 `NotifyRootProtected`。
- **沙盒选项 > 其它杂项 > Dll && 扩展 > 映像保护 > 当一个程序试图加载一个沙盒内部的 DLL 文件时，提示问题代码 SBIE1305** 控制 `NotifyImageLoadDenied`。
- **全局设置 > 程序控制 > 程序警报** 提供 **当强制沙盒化进程被禁止时，提示问题代码 SBIE1301**、**当进程被强制沙盒化时，提示问题代码 SBIE1321**，以及全局的 **程序启动失败时，提示问题代码 SBIE1308** 控件。

Sandboxie Control Classic 提供互联网访问与启动/运行访问的通知控件。对于 `NotifyDirectDiskAccess`、`NotifyProcessAccessDenied`、`NotifyBoxProtected` 或 `NotifyImageLoadDenied`，未找到等效的当前专用 Classic 控件；兼容的 INI 设置仍可通过共享的运行时使用。未找到 `NotifyRootProtected` 或 `NotifyMsiInstaller` 的专门 SandMan 控件。

<div id="version-history"></div>

## 版本历史

- 设置元数据把 `AlwaysShowReminder` 列为在 1.3.0 版本中添加。
- `NotifyForceProcessDisabled` 在 Sandboxie Plus 1.3.2 / Classic 5.58.2 中添加。
- 设置元数据把 `AlertStartRunAccessDenied` 列为在 1.6.0 版本中添加。
- 设置元数据把 `NotifyNoCopy` 列为在 1.7.0 版本中添加。
- 设置元数据把 `NotifyImageLoadDenied` 列为在 1.9.0 版本中添加。
- 设置元数据把 `NotifyBoxProtected` 列为在 1.9.4 版本中添加。
- `NotifyProcessAccessDenied` 在 Sandboxie Plus 1.0.18 / Classic 5.55.18 中添加。
- `NotifyMsiInstaller` 在 Sandboxie Plus 1.15.2 / Classic 5.70.2 中添加。
- `NotifyForceProcessEnabled` 在 Sandboxie Plus 1.15.3 / Classic 5.70.3 中添加。
- 设置元数据把 `NotifyRootProtected` 列为在 1.15.5 版本中添加。
