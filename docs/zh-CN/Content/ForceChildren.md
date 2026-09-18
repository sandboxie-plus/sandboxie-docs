# 强制子进程

`ForceChildren` 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置（v1.14.5 / 5.69.5 引入），强制父进程的特定子进程在指定沙盒中启动。当你想让已知父进程启动的任何进程都被自动沙盒化时，这很有用。

## 语法

一般形式：

```ini
[DefaultBox]

ForceChildren=<程序>
```

其中 `<程序>` 可以是：

- 带通配符的映像路径，例如 `C:\Users\*\App\*.exe` —— 通配符模式会与规范路径进行不区分大小写的匹配。
- 不带反斜杠的映像名称，例如 `dopus.exe` —— 按映像名称使用驱动程序映像匹配规则进行匹配。

注意：

- `ForceChildren` 中的路径在匹配前会经过规范化处理（移除重复反斜杠并转换重解析点）。[^1]
- 使用通配符模式时，会创建一个模式匹配器，并与转换后的路径进行不区分大小写的匹配。[^2]

## 行为和匹配规则

- 创建新进程时会评估 `ForceChildren` 条目。如果父进程匹配任何已启用沙盒的 `ForceChildren` 规则，子进程将被强制进入该沙盒。[^3]

- 匹配尝试（大致按优先级顺序）：

    - 父进程的映像名称与 `ForceChildren` 条目中作为映像名称或映像模式的条目比较。[^4]
    - 父进程的规范化映像路径和/或工作目录与 `ForceChildren` 条目中的通配符路径模式（含 `*` 的条目）比较。[^5]

- 含通配符的规则使用模式引擎；不含通配符的规则使用支持 NLS 的字符串比较和映像匹配辅助例程，以进行正确的语言感知检查。[^2][^4]

- 沙盒的 `ForceChildren` 匹配取决于该沙盒对当前用户/会话已启用且已启用强制规则。`DisableForceRules` 之类的设置会阻止应用该沙盒的强制规则。[^6]

- 某些系统进程和 Sandboxie 内部组件可豁免强制。Sandboxie 主目录永远不会被强制。[^7]

## 示例

1. 强制特定父二进制文件的子进程（映像名称）：

    ```ini
    [MyBox]
    
    ForceChildren=parentapp.exe
    ```

2. 使用通配符模式匹配父映像路径：

    ```ini
    [MyBox]
    
    ForceChildren=C:\Users\*\Downloads\*\app.exe
    ```

## 命令行开关

详情参见 [启动命令行](StartCommandLine.md#force_children-or-fcp)。

### 相关开关：

- `/force_children` —— 从命令行启用/影响强制子进程行为。
- `/fcp` —— `/force_children` 的简写（在支持处）。

## 与警报和其他强制设置的交互

- 当驱动程序确定新启动的进程应使用哪个沙盒（如果有）时，`ForceChildren` 条目会与 `ForceFolder` 和 `ForceProcess` 条目一起评估。

- 如果匹配规则启用了警报（例如，当强制规则受策略限制时），驱动程序可能显示警报而不是强制该进程。驱动程序跟踪一个"警报"状态，可以阻止强制，并可选地记录或通知用户。[^8]

- `ForceChildren` 设置补充了 `ForceProcess`（无论父进程如何，直接按名称强制命名进程）和 `ForceFolder`（按文件夹路径强制进程）。当你想强制由特定父进程派生的进程时，请使用 `ForceChildren`。

## 实现说明（驱动程序行为）

- 驱动程序在进程创建时为每个已启用沙盒构建内存中的强制规则列表。每条 `ForceChildren` 条目被转换为内部 `FORCE_ENTRY` 元素，存储规范路径或（存在通配符时）编译的 PATTERN。[^2]

- 按映像名称匹配时，驱动程序使用辅助函数 `Process_MatchImage`，它实现了语言感知且特定于映像名称的匹配逻辑。[^4]

- 代码确保在使用前移除重复反斜杠并解析重解析点；尽可能执行到 NT 风格路径的转换。如果无法转换，则使用原始路径进行匹配。[^1][^5]

## 另请参阅

- [强制进程](ForceProcess.md) —— 按名称或路径强制进程。
- [强制文件夹](ForceFolder.md) —— 按文件夹路径或模式强制进程。
- [禁用强制规则](DisableForceRules.md) —— 禁用沙盒所有强制规则的逐沙盒设置。

## 图形界面（Sandboxie Manager / 沙盒管理器）

### 在哪里找到它：

- 打开 Sandboxie Manager（沙盒管理器）。
- 打开沙盒的选项：右键点击沙盒并选择"沙盒选项"。
- 在选项窗口中，找到列出强制条目的程序控制 / 强制程序区域。

### 如何添加强制子进程条目：

1. 在选项窗口的程序控制 / 强制程序区域，你会看到强制条目列表以及"强制程序"、"强制子进程"和"强制文件夹"按钮。
2. 点击"强制子进程"，通过选择可执行文件（或使用打开文件对话框的浏览变体）添加条目。
3. 该项目以类型标签"子进程"出现在列表中。勾选的条目保存到 `ForceChildren`；未勾选的条目保存到 `ForceChildrenDisabled`。
4. 要移除条目，选中它并点击"移除"。

### 说明和参考：

- UI 树控件是 `OptionsWindow.ui` 中的 `ui.treeForced`。选项窗口在 `OptionsForce.cpp`（LoadForced/SaveForced/AddForcedEntry）中加载/保存这些列表。
- 同页显示的"禁用此沙盒的强制程序和强制文件夹"复选框是 `ui.chkDisableForced`，对应 `DisableForceRules` 设置。

## 脚注

[^1]: 驱动程序在存储条目之前移除重复反斜杠并转换重解析点。参见 `Process_AddForceFolders` 如何把 `expnd` 规范化为 `buf` 并调用 `File_TranslateReparsePoints`。

[^2]: 通配符条目使用 `Pattern_Create` 创建 PATTERN 对象，并用 `Pattern_Match` 与小写的规范路径匹配。

[^3]: `Process_FcpInsert`、`Process_FcpCheck` 及相关例程实现基于父进程的强制映射，使新创建的子进程可以添加到以 PID 为键的映射中，并在子进程创建期间进行检查。

[^4]: 映像名称匹配委托给 `Process_MatchImage`（当条目不含反斜杠时由驱动程序使用）。

[^5]: 驱动程序使用 `Process_TranslateDosToNt` 把 DOS 风格路径转换为 NT 风格路径，它包装 `File_TranslateDosToNt`，如果转换因语法错误失败则回退为复制原始路径。

[^6]: 构建强制数据列表时，只考虑对当前 SID/会话已启用且未设置 `DisableForceRules` 的沙盒。

[^7]: Sandboxie 主目录下的路径被排除在强制之外；代码显式检查并跳过 `Driver_HomePathNt` 下的匹配。

[^8]: 当警报规则匹配时，驱动程序可能设置警报状态（`IsAlert`）并推迟强制。警报可能产生记录的消息，并且根据设置，可以阻止进程在沙盒下启动。
