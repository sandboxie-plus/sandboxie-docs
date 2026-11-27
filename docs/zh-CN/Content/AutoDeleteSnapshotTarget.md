# AutoDeleteSnapshotTarget

*AutoDeleteSnapshotTarget* 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.18.2 起可用。它选择 SandMan 在自动删除沙盒内容后要返回的保留快照状态。

本设置不会启用自动删除，也不会删除选定的快照。它只在启用了 [自动删除](AutoDelete.md) 且沙盒保留了快照时才有意义。

<div id="usage"></div>

## 用法

```ini
[DefaultBox]
AutoDelete=y
AutoDeleteSnapshotTarget=Current
```

有效值为 `Current` 与 `Default`。`y`、`n` 这类布尔值无效。

<div id="restore-targets"></div>

## 恢复目标

### Current

`AutoDeleteSnapshotTarget=Current` 会在自动删除后把沙盒返回到当前活动的快照状态。活动状态也可能是空沙盒状态。该状态之上的实时更改会被丢弃，而已保存的快照树会保留。

### Default

`AutoDeleteSnapshotTarget=Default` 会把沙盒返回到标记为默认的快照。如果未配置默认快照，则返回到空沙盒状态。默认快照不会被删除，所有已保存的快照仍然可用。

例如：

```text
空状态
└── 快照 A（默认）
    └── 快照 B（活动）
        └── 未保存的实时更改
```

使用 `Current` 时，实时更改被丢弃，快照 B 保持活动；快照 A 与 B 仍为已保存状态。使用 `Default` 时，实时更改被丢弃，快照 A 成为活动的默认状态；快照 B 同样保持已保存状态。

> [!WARNING]
> 自动删除会永久丢弃所选目标状态之上的实时文件和注册表更改。除非你另行选择删除所有快照，已保存的快照历史会保留。快速恢复可以在删除前提供恢复符合条件文件的机会，但它并非防止数据丢失的通用保障。

<div id="default-and-invalid-values"></div>

## 默认值与无效值

当本设置缺失或无效时，并不存在单一固定的回退值。正常的同步自动清理返回活动状态，而异步或静默清理返回默认状态。包括 `y` 与 `n` 在内的无效值，沿用同样取决于上下文的旧有行为。需要可预测的行为时，请显式配置 `Current` 或 `Default`。

<div id="automatic-and-manual-deletion"></div>

## 自动删除与手动删除

本设置只影响 SandMan 的自动删除路径。如 [自动删除](AutoDelete.md) 所控制，最后一个沙盒化进程终止时仍会触发自动清理。

手动的 **删除内容** 操作使用其自身的快照行为，不使用本设置在当前状态与默认状态之间选择。显式请求删除所有快照同样会绕过本设置，并可能移除已保存的快照历史。

*AutoDeleteSnapshotTarget* 不控制创建或切换快照、选择默认快照、删除单个快照或合并快照。快照管理参见 [沙盒快照（适用于 Sandboxie Plus）](../PlusContent/BoxSnapshots.md)。

<div id="recovery-behavior"></div>

## 恢复行为

在自动删除之前，Sandboxie 的常规恢复处理可能提供恢复符合条件文件的机会。本设置不会改变恢复文件夹、文件资格条件、[自动恢复](AutoRecover.md) 或 [快速恢复](QuickRecovery.md) 的过滤；它只选择删除后使用的保留状态。

<div id="sandbox-options"></div>

## 沙盒选项

在 Sandboxie Plus 中，打开 **沙盒选项 > 文件选项 > 沙盒删除选项**。启用 **当沙盒内最后一个进程终止后自动删除更改的内容**，然后在 **自动删除后，从以下快照恢复：** 下选择目标：

- **当前快照** 写入 `AutoDeleteSnapshotTarget=Current`。
- **默认快照** 写入 `AutoDeleteSnapshotTarget=Default`。

目标控件在启用自动删除时可用，且不要求已存在快照。此处 **当前快照** 可能表示空的活动状态。

<div id="applying-changes"></div>

## 应用更改

SandMan 在自动删除开始时读取本设置。因此，已保存的更改会应用于下一次符合条件的自动删除；不需要重启 SandMan、重启沙盒化应用程序或重新创建快照。

<div id="sandboxie-plus-and-classic"></div>

## Sandboxie Plus 与 Classic

这个快照目标选项属于 SandMan/Sandboxie Plus 的快照工作流。Sandboxie Classic 使用不同的删除路径，不提供此沙盒选项行为。

<div id="failure-behavior"></div>

## 失败行为

如果选定的目标已不存在、恢复其数据失败或内容无法删除，自动删除可能报告错误。该操作不承诺事务性回滚，自动或静默清理期间的每一次失败也不保证都会产生交互式对话框。

<div id="version-history"></div>

## 版本历史

Sandboxie Plus 1.18.2 引入了显式的 `Current` 与 `Default` 选项，使目标选择在各类自动清理实现之间保持一致。

<div id="related-configuration"></div>

## 相关配置

- [自动删除](AutoDelete.md)
- [沙盒快照（适用于 Sandboxie Plus）](../PlusContent/BoxSnapshots.md)
- [快速恢复](QuickRecovery.md)
- [自动恢复](AutoRecover.md)
- [Sandboxie Ini](SandboxieIni.md)
