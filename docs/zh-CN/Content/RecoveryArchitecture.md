# 文件恢复架构 {#file-recovery-architecture}

文件恢复会把选定的内容从沙盒移动到宿主可访问的目标位置。配置可恢复位置并不会授予沙盒化程序访问该宿主位置的权限；恢复操作在用户选择要恢复的内容之后，于沙盒外执行。

<div id="recovery-is-split-across-components"></div>

## 恢复分散在多个组件中

| 组件 | 作用 |
| --- | --- |
| 自动检测 | 使用 `AutoRecover=y` 时，SbieDll 会监视沙盒化进程中符合条件的文件活动，并报告恢复候选对象。 |
| 快速恢复 | SandMan 在打开恢复窗口时单独扫描已配置的位置。它不要求 `AutoRecover=y`。 |
| 呈现 | SandMan 按其偏好显示恢复对话框或通知。 |
| 目标位置 | 用户选择对应的宿主文件夹或其他文件夹。 |
| 恢复操作 | SandMan 把选定的文件从沙盒存储移动到宿主目标位置。 |

<div id="recoverable-locations"></div>

## 可恢复位置

可重复的 [`RecoverFolder`](RecoverFolder.md) 条目为自动检测和快速恢复共同指明位置或模式。字面的文件夹会提供一个递归的快速恢复扫描根。通配符条目则用于过滤候选路径；它不是递归扫描该模式所代表的每个路径的指令。有效条目可能来自沙盒配置和已启用的模板。`%Personal%` 这类个人文件夹引用可以展开为可用的路径。

<div id="automatic-and-immediate-recovery"></div>

## 自动恢复与即时恢复

[`AutoRecover=y`](AutoRecover.md) 使用有效的 `RecoverFolder` 与 [`AutoRecoverIgnore`](AutoRecoverIgnore.md) 条目来初始化进程侧检测。候选对象必须匹配某个可恢复位置，且不匹配任何忽略条目。Sandboxie 会在相关文件活动之后报告符合条件的、非空的沙盒内文件；这并不承诺在文件创建的确切时刻弹出提示。检测本身不会移动文件。

SandMan 接收恢复事件，可以打开对话框或呈现通知。其通知偏好与临时抑制会影响用户看到的内容。无论快速恢复的忽略选项如何，自动检测都会应用 `AutoRecoverIgnore`。

当 `AutoRecover` 设置缺失时，SbieDll 中对应的回退行为处于禁用状态。新建的沙盒可能会显式启用它：当前 SandMan 的新建沙盒向导默认勾选即时恢复，而 Classic 的新建沙盒默认值会写入 `AutoRecover=y`。因此，由产品创建的沙盒与没有有效 `AutoRecover` 值的沙盒行为未必相同。

<div id="quick-recovery"></div>

## 快速恢复

打开 [快速恢复](QuickRecovery.md) 时，SandMan 会读取有效的恢复位置并递归扫描字面根。通配符条目会过滤扫描中发现的候选对象。该窗口也可以显示所有沙盒内文件，而不只是已配置的恢复位置。

启用 [`UseAutoRecoverIgnoreForQuick`](UseAutoRecoverIgnoreForQuick.md) 时，SandMan 可以把 `AutoRecoverIgnore` 应用到快速恢复列表。窗口的 **显示所有文件** 或 **显示被忽略的文件** 视图可以显示原本隐藏的文件。这种快速恢复专用的过滤不会取代自动检测器自身的忽略检查。

设置元数据把 `UseAutoRecoverIgnoreForQuick` 的默认值描述为 `n`，但当前的 SandMan 使用方把缺失值视为已启用。显式的 `n` 会关闭其常规的快速恢复列表过滤。这是 SandMan 使用方的默认值，而不是 SbieDll 范围内的运行时默认值。

<div id="destinations-and-moving-files"></div>

## 目标位置与移动文件

**恢复到对应的目录** 选择沙盒外的对应位置；**恢复到任意文件夹** 允许用户选择另一个目标位置。SandMan 在用户设置（`SbieCtrl_RecoverTarget`）中保留可复用的目标历史，并保留自己的上次目标偏好。这些不是 `RecoverFolder` 的沙盒规则。

SandMan 会准备目标位置，并对选定的沙盒文件使用宿主侧移动（`QFile::rename`）。如果目标已存在，它会在覆盖前询问；批准覆盖可能会在移动之前移除已有的目标。移动失败会被报告，未恢复的沙盒源文件仍然保留。恢复不保证是原子的，也不保证回滚先前已批准的覆盖。

移动文件之前，SandMan 可能运行已安装的 FileChecker 附加组件或已配置的 [`OnFileRecovery`](SandManTriggers.md) 命令。检查器失败可能会中止该次恢复，除非用户显式忽略该警告。检查器与用户批准并不能证明恢复的内容可以安全地打开或运行。

<div id="applying-changes"></div>

## 应用更改

自动检测及其文件夹/忽略列表会在每个沙盒化进程中初始化。当你需要自动检测器使用新值时，请在更改 `AutoRecover`、`RecoverFolder` 或 `AutoRecoverIgnore` 之后重启受影响的沙盒化进程。SandMan 在创建恢复窗口时读取恢复位置，而快速恢复列表的忽略设置会在扫描与刷新期间重新加载。在该窗口之外更改 `RecoverFolder` 后，请重新打开恢复窗口。这些 SandMan 侧的更改不需要为快速恢复重启沙盒化进程。

<div id="classic-and-sandman"></div>

## Classic 与 SandMan

较早的 [恢复设置](RecoverySettings.md)、[快速恢复](QuickRecovery.md) 与 [即时恢复](ImmediateRecovery.md) 页面保留了有用的 Sandboxie Control / Classic 工作流程与截图。当前的 Sandboxie Plus 控件位于 **沙盒选项 > 文件恢复**，其中有单独的 **快速恢复** 与 **即时恢复** 节。SandMan 的呈现偏好位于 **全局设置 > 常规选项**：**恢复选项** 包含恢复窗口偏好，**消息通知** 包含 **将可恢复的文件以通知形式显示**。

<div id="version-history"></div>

## 版本历史

通配符恢复模式与 `UseAutoRecoverIgnoreForQuick` 是在 Sandboxie Plus 1.18.0 / Classic 5.73.0 中添加的。这并不代表较早的恢复设置的引入日期。

<div id="related-pages"></div>

## 相关页面

- [恢复文件夹](RecoverFolder.md)
- [自动恢复](AutoRecover.md)
- [自动恢复忽略](AutoRecoverIgnore.md)
- [对快速恢复使用自动恢复忽略](UseAutoRecoverIgnoreForQuick.md)
- [快速恢复](QuickRecovery.md)
- [即时恢复](ImmediateRecovery.md)
