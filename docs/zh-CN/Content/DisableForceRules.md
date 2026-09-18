# 禁用强制规则

`DisableForceRules` 是逐沙盒设置（v1.9.1 / 5.64.1 引入），禁用该沙盒的所有"强制"规则。设置后，驱动程序将跳过处理该沙盒中定义的 `ForceFolder`、`ForceProcess` 和 `ForceChildren` 条目，从而有效阻止基于这些规则的自动沙盒强制。

当你希望一个沙盒存在但不参与自动强制决策时（例如，只把该沙盒用于手动运行或特殊操作），此设置尤其有用。

## 语法

把它放在 Sandboxie 配置的沙盒节下：

```ini
[DefaultBox]

DisableForceRules=<y|n>
```

有效值：

- `y` — 启用：该沙盒的强制规则被忽略。
- `n` — 禁用（默认）：构建强制列表时会评估该沙盒的强制规则。

## 行为

- 当驱动程序枚举配置节以构建内存中的强制规则时，它会调用 `Conf_IsBoxEnabled`，然后检查 `DisableForceRules`。如果某个沙盒设置了 `DisableForceRules`，该沙盒会被跳过强制规则处理，它的任何 `ForceFolder`、`ForceProcess` 或 `ForceChildren` 条目都不会被使用。[^1]

- 影响沙盒是否被考虑的其他设置包括该沙盒对当前 SID/会话的启用状态——创建强制列表时不考虑对当前用户/会话未启用的沙盒。[^2]

- `DisableForceRules` 不会移除该沙盒，也不改变其他非强制行为；它只阻止驱动程序把该沙盒的强制条目添加到运行时强制列表。

## 示例

为名为 `NoAutoForce` 的沙盒禁用强制规则：

```ini
[NoAutoForce]

DisableForceRules=y
```

保持强制规则启用（默认）：

```ini
[MyBox]

DisableForceRules=n
```

## 图形界面（Sandboxie Manager / 沙盒管理器）

从 Sandboxie Manager（沙盒管理器）界面的以下任一位置切换"禁用强制规则"：

- 上下文菜单 -> 沙盒预设 -> 禁用强制规则
	- 在沙盒列表中右键点击沙盒，打开"沙盒预设"子菜单，切换"禁用强制规则"项。
- 沙盒选项 -> 强制选项卡
	- 右键点击沙盒，选择"沙盒选项"，在"程序控制"选项卡下切换到"强制程序"，勾选/取消勾选"禁用此沙盒的强制程序和强制文件夹"复选框，然后保存。

这些界面控件直接映射到 `DisableForceRules` 沙盒设置，并立即为所选沙盒更新它。[^4][^5]

## 实现说明（驱动程序行为）

- 驱动程序调用 `Process_CreateForceData` 为每个已启用沙盒构建内存中的 `FORCE_BOX` 条目列表。创建期间它遍历配置节，并跳过任何 `Conf_Get_Boolean(section, L"DisableForceRules", 0, FALSE)` 返回真的沙盒。[^1]

- 在 `Process_CreateForceData` 中跳过沙盒，意味着它的任何 `ForceFolder`、`ForceProcess` 或 `ForceChildren` 列表都不会被添加到 `Process_GetForcedStartBox` 及相关检查使用的运行时 `boxes` 列表。

## 另请参阅

- [强制进程](ForceProcess.md) —— 按名称或路径强制进程。
- [强制文件夹](ForceFolder.md) —— 按文件夹路径或模式强制进程。
- [强制子进程](ForceChildren.md) —— 基于父进程的强制规则（匹配父进程的子进程被强制）。

## 脚注

[^1]: 参见 `Process_CreateForceData` 如何遍历所有配置节，并用 `if (Conf_Get_Boolean(section, L"DisableForceRules", 0, FALSE)) continue;` 跳过启用该设置的沙盒。

[^2]: 在为沙盒构建任何强制列表之前，使用 Conf_IsBoxEnabled 决定该沙盒是否对当前 SID/会话处于活动状态。

[^3]: 决定进程是否可以被强制时，驱动程序检查 `AllowForceSystem` 等全局/会话级标志和基于会话的强制禁用标志；`DisableForceRules` 只影响强制列表中逐沙盒的包含。

[^4]: 预设菜单切换在沙盒管理器的 `SbieView.cpp`（`m_pMenuPresetsForce`）中实现，并调用 `SetBoolSafe("DisableForceRules", ...)` 更改设置。

[^5]: 沙盒选项对话框在 `OptionsForce.cpp` 中读写复选框 `ui.chkDisableForced`，并在保存选项时持久化 `DisableForceRules` 设置。
