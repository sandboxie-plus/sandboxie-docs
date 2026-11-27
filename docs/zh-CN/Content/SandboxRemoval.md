# 沙盒删除与移除生命周期 {#sandbox-deletion-and-removal-lifecycle}

删除沙盒内容与移除沙盒定义是不同的操作。SandMan 在沙盒化应用程序之外执行这两项操作；两者都不受 Delete V1/V2 文件或注册表虚拟化设置的控制。

| 操作 | 结果 |
| --- | --- |
| **删除内容**（清理沙盒） | 丢弃或重置已存储的沙盒更改，同时保留沙盒定义。若保留了快照，结果状态可能是已保存的快照，而不是空目录。 |
| **移除沙盒** | 移除沙盒定义。普通的手动移除会先处理其已存储的内容；如果存储不为空，移除可能失败。 |

**文件根范围：** 对于普通沙盒，**删除内容** 与 **移除沙盒** 作用于当前解析出的文件根。更改 [文件根路径](FileRootPath.md) 不会把数据从先前的根移走，因此留在那里的文件不会被这些操作清理。快速恢复扫描的是当前根，而不是先前的根。更改根之前，请单独处理旧根中的数据。

<div id="automatic-content-cleanup"></div>

## 自动内容清理

[`AutoDelete=y`](AutoDelete.md) 要求 SandMan 在观察到先前活动的沙盒运行进程数归零时清理其内容。该设置缺失时处于关闭状态。它本身**不会**移除沙盒定义。在正常的沙盒关闭路径上，SandMan 先运行 [`OnBoxTerminate`](SandManTriggers.md#onboxterminate)，然后检查 `NeverDelete` 与 `AutoDelete`。如果清理符合条件，[恢复](QuickRecovery.md) 可能在删除前提供可恢复文件；取消该工作流会停止本次清理，而没有可见的可恢复文件则可能让它静默继续。恢复并不保证能找到每一个有价值的文件。

如果清理继续，SandMan 会在常规内容清理操作之前运行 [`OnBoxDelete`](SandManTriggers.md#onboxdelete)。该触发器是宿主侧的自动化，而不是执行删除的命令。SandMan 可以通过等待式非队列路径或队列作业执行清理。启动清理选项也可以对已是空的沙盒调用沙盒关闭处理。

<div id="snapshots-and-cleanup-results"></div>

## 快照与清理结果

自动清理只能丢弃实时更改，并把沙盒返回到保留的活动或默认快照状态。[`AutoDeleteSnapshotTarget`](AutoDeleteSnapshotTarget.md) 为自动清理选择该目标；它不会开启 `AutoDelete`。手动的 **删除内容** 有其自身的快照选项，包括是否删除所有快照。参见 [沙盒快照（适用于 Sandboxie Plus）](../PlusContent/BoxSnapshots.md)。

清理可能在部分内容已经改变之后失败；它不是带保证回滚的事务。底层文件夹删除会等待访问权限并重试失败，但仍可能返回错误。快照还原也可能单独失败。

<div id="automatic-definition-removal"></div>

## 自动移除定义

`AutoRemove=y` 是一项独立的沙盒设置。SandMan 在处理内容清理完成时查询它，然后尝试移除定义。它本身不会在沙盒关闭时启动清理：在 `AutoDelete=n` 时，仅关闭最后一个进程不会移除沙盒。不过，之后的手动 SandMan 清理仍可到达同一移除转换点。

新建沙盒向导的 **使用后删除** 选项会**同时**写入 `AutoDelete=y` 与 `AutoRemove=y`。在普通清理使存储清空的情况下，这会把内容清理与定义移除配对。保留快照的清理可能使存储仍然存在，此时底层移除操作会拒绝移除定义。

不要把清理与移除当作全有或全无的事务。失败的队列清理作业不会到达 `BoxCleaned` 完成转换点；非队列的等待路径即使其清理进度报告错误，也可能尝试 `AutoRemove` 转换。底层普通移除仍会拒绝存储非空的沙盒。在假定定义或数据已消失之前，请检查实际结果。

<div id="protection-settings"></div>

## 保护设置

`NeverDelete=y` 阻止自动内容清理，并会被普通完整清理与队列清理路径检查。`NeverRemove=y` 保护正常的手动 SandMan **移除沙盒** 操作。它们保护不同的操作，且都不是文件系统访问控制。

在 **沙盒选项 > 文件选项 > 沙盒删除选项** 中，三态的 **保护此沙盒免受删除或清空** 复选框映射如下：

| 复选框 | 保存的设置 | 含义 |
| --- | --- | --- |
| 已勾选 | `NeverDelete=y`, `NeverRemove=y` | 通过各自的正常路径保护内容与定义。 |
| 部分勾选 | `NeverRemove=y`；`NeverDelete` 关闭 | 通过手动移除保护定义，但允许普通内容清理。 |
| 未勾选 | 两者均关闭 | 未选择任何保护。 |

这些保护有路径特定的限制。对于普通沙盒，`NeverDelete` 可能阻止手动移除所需的清理。在非队列的手动清理路径中，`OnBoxDelete` 命令可能在普通完整清理守卫拒绝受保护沙盒之前运行。该路径还可以在不经过该 `NeverDelete` 守卫的情况下选择保留的快照；对未挂载的映像支持型沙盒的移除还有另一条特殊路径。不要把 `NeverDelete` 当作通用的数据保全保证。反过来，当前清理之后的 `AutoRemove` 转换**不会**查询 `NeverRemove`，尽管正常的手动移除会。因此，手写组合 `AutoRemove=y` 与 `NeverRemove=y` 在自动与手动路径上的结果不同。

<div id="manual-actions"></div>

## 手动操作

对于 **删除内容**，SandMan 会根据其偏好请求确认或提供恢复窗口，终止正在运行的沙盒化进程，并启动普通或感知快照的内容清理。`OnBoxDelete` 在适用时先于该清理运行。定义通常会保留，但 `AutoRemove=y` 可以在清理之后发起后续的移除尝试。

对于 **移除沙盒**，SandMan 会请求确认、处理已挂载的映像存储、对普通沙盒检查 `NeverRemove`，并在移除定义之前以移除模式请求清理。此直接移除模式不运行 `OnBoxDelete`。普通移除要求存储为空；清理失败或残留映像可能阻止定义移除。内部临时/影子对象有单独的路径，不是普通的面向用户配置选项。

<div id="configuration-and-applying-changes"></div>

## 配置与应用更改

这些是沙盒生命周期设置，不是映像限定或进程限定的资源规则。当前 SandMan 中 `AutoDelete`、`AutoRemove`、`NeverDelete` 与 `NeverRemove` 的布尔值使用方直接读取沙盒值，缺失时使用 `n`；它们的调用不请求 `GlobalSettings` 或模板回退。`AutoDeleteSnapshotTarget` 在自动清理开始时从有效配置读取，包括适用的全局/模板值。生命周期开关在其对应的沙盒关闭、清理或手动移除事件中求值，因此更改它们通常不需要重启沙盒化进程、服务或 Windows。

<div id="sandboxie-plus-and-classic"></div>

## Sandboxie Plus 与 Classic

本页描述当前 SandMan 的行为。较早的 [删除设置](DeleteSettings.md) 页面保留了 Sandboxie Control / Classic 界面。Classic 的 [`DeleteCommand`](DeleteCommand.md) 选择其旧有的删除命令，与 SandMan 清理前的 `OnBoxDelete` 触发器仍然是两回事。

<div id="version-history"></div>

## 版本历史

较早的 `AutoDelete` 与 `NeverDelete` 设置在当前的设置元数据中没有确定的引入版本。`AutoRemove` 在 Sandboxie Plus 1.7.1 中加入；`NeverRemove` 在 1.10.1 中加入；`AutoDeleteSnapshotTarget` 在 1.18.2 中加入。这些版本并不意味着完整的生命周期或 Classic 界面始于这些发行版。

<div id="related-pages"></div>

## 相关页面

- [自动删除](AutoDelete.md)
- [从不删除](NeverDelete.md)
- [AutoDeleteSnapshotTarget](AutoDeleteSnapshotTarget.md)
- [删除设置](DeleteSettings.md)
- [删除沙盒](DeleteSandbox.md)
- [快速恢复](QuickRecovery.md)
- [SandMan Triggers](SandManTriggers.md)
- [沙盒快照（适用于 Sandboxie Plus）](../PlusContent/BoxSnapshots.md)
