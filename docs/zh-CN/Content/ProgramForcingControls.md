# 程序强制控制

自动强制决定：当某程序本会在沙盒之外启动时，一次 **新进程启动** 应如何处理。驱动在 `Process_GetForcedStartBox()` 中完成核心选择。已配置的强制规则、全局程序警报与临时的 **暂停强制沙盒化程序规则** 状态各有用途；它们都不是覆盖 Sandboxie 全部隔离的总开关。

## 一次启动是如何被求值的

Sandboxie 先判断进程是否已关联到某个沙盒路径，然后针对为当前用户和会话启用的沙盒，求值已配置的强制规则。每个沙盒都可以贡献 [强制文件夹](ForceFolder.md)、[强制进程](ForceProcess.md) 与 [强制子进程](ForceChildren.md) 规则；不存在单一的全局目标沙盒。[禁用强制规则](DisableForceRules.md) 会把某个沙盒排除在为这些规则构建的强制数据之外。

对于常规配置规则，现有详细顺序是：可执行文件所在目录的 `ForceFolder` → `ForceProcess` / 已配置的 `ForceChildren` → 工作目录的 `ForceFolder` → 文档参数的 `ForceFolder`。各链接的设置页面涵盖了匹配语法与例外。

如果常规强制没有选中沙盒，驱动会检查全局的 `AlertFolder`，然后再检查 `AlertProcess` 条目。普通的警报列表匹配只会报告或拒绝一次未沙盒化的启动，它 **不会** 选择沙盒。其他独立路径，包括网络标记（Mark-of-the-Web）强制，可能在稍后被求值。一次成功的常规强制选择不会同时走这条普通警报列表分支。

| 机制 | 作用范围 | 持久性 | 对新启动的影响 |
| --- | --- | --- | --- |
| `DisableForceRules=y` | 单个沙盒 | 配置 | 使该沙盒不参与常规强制数据。 |
| **暂停强制沙盒化程序规则** | Windows 会话 | 临时的计时状态 | 生效期间跳过匹配的常规强制规则的分派。 |
| `AlertFolder` / `AlertProcess` | 全局 | 配置 | 匹配沙盒之外的启动，用于通知或拒绝；不选择沙盒。 |
| `StartRunAlertDenied=y` | 全局 | 配置 | 使常规警报列表的匹配项拒绝启动。 |
| `AllowForceSystem=y` | 全局 | 配置 | 从主强制/警报求值中移除基于身份的默认排除；仍需规则匹配。 |

这些机制不能相互替代。SandMan 还可能把未勾选的单条强制条目保留为禁用的界面项；它们既不是生效的强制规则，也不等同于 `DisableForceRules` 或会话暂停。

<div id="global-program-alerts-and-blocking"></div>

## 全局程序警报与阻止

`AlertFolder` 与 `AlertProcess` 是 `[GlobalSettings]` 下的全局列表，不是逐沙盒的目标规则：

```ini
[GlobalSettings]
AlertFolder=C:\Example
AlertProcess=example.exe
```

[警报文件夹](AlertFolder.md) 在进程启动时检验可执行文件自身的路径/目录。与 `ForceFolder` 不同，它不会为警报匹配去检查工作目录或文档参数。普通的文件夹条目会递归匹配该文件夹下的内容；通配符条目使用模式匹配。[警报进程](AlertProcess.md) 把普通条目当作映像名匹配；包含 `*` 的条目会作为大小写不敏感的模式，去匹配规范化后的可执行文件路径。这两个列表都不监视启动之后的任意文件访问或活动。

默认情况下 `StartRunAlertDenied=n`：常规警报列表的匹配可以产生 [SBIE1301](SBIE1301.md)，而不会因此机制阻止启动。设 `StartRunAlertDenied=y` 后，常规警报列表的匹配会改为拒绝启动。`AlertStartRunAccessDenied` 默认是 `y`，它控制的是该拒绝是否报告 [SBIE1308](SBIE1308.md)，并不控制拒绝本身。这套全局警报策略与沙盒的 **启动/运行访问** 限制是分开的。

SandMan 在 **全局设置 > 程序控制 > 程序警报** 下提供这些列表，配套 **添加程序** 与 **添加文件夹**。**阻止下列程序在此系统中启动** 对应 `StartRunAlertDenied`；**程序启动失败时，提示问题代码 SBIE1308** 对应这条全局路径上的 `AlertStartRunAccessDenied`。

## 临时暂停与持久的逐沙盒禁用

SandMan 的 **暂停强制沙盒化程序规则** 菜单动作在开始暂停时会询问时长。工具栏与热键动作不会询问。驱动为该 Windows 会话保存暂停时间戳；它不会在沙盒上设置 `DisableForceRules=y`，也不会挂起已在运行的进程。暂停生效期间，匹配的 `ForceFolder`、`ForceProcess` 或 `ForceChildren` 规则在新启动时会被跳过。

被跳过的强制匹配会保留其“已暂停的强制”状态：`StartRunAlertDenied` **不会** 把该匹配变成被阻止的启动。若 `NotifyForceProcessDisabled=y`，则可能改为产生 SBIE1301。若没有任何强制规则匹配，普通的 `AlertFolder` / `AlertProcess` 检查仍会执行，并可能在 `StartRunAlertDenied=y` 下阻止启动。暂停强制不会禁用全局警报/阻止列表。

[强制禁用等待秒数](ForceDisableSeconds.md) 控制暂停时长。菜单提示最初提供配置值，缺少该设置时为 60 秒；工具栏与热键动作使用配置值，或驱动的 10 秒回退值。已配置的全局 `ForceDisableSeconds=0` 会使定时暂停失效；零不表示无限期暂停，也不表示永久禁用强制。API 只在时长为正数时才保存所给时长，因此在菜单中输入零不一定写入零值的 INI 设置。即使把正的时长保存为配置，暂停状态仍然是临时的。

[仅限管理员强制禁用](ForceDisableAdminOnly.md) 默认是 `n`。设全局 `ForceDisableAdminOnly=y` 后，暂停 API 仅限于管理员账户；它并不总是要求已提升的管理员令牌。SandMan 对该项标注为 **仅管理员用户可「停用强制沙盒化程序规则」**。底层驱动还会校验控制调用方是否可信。

<div id="system-service-identities"></div>

## 系统服务身份

`AllowForceSystem` 是一个高级的手工全局布尔值，默认是 `n`。默认防护会跳过主强制规则、警报规则与网络标记求值，条件是目标进程以 `S-1-5-18`（LocalSystem）、`S-1-5-19`（LocalService）或 `S-1-5-20`（NetworkService）身份运行。以这些身份运行、且父进程被识别为 DcomLaunch 的进程，是对该防护的显式兼容例外；这不能推广到所有以 SYSTEM 为父进程的场景。

```ini
[GlobalSettings]
AllowForceSystem=y
```

启用后，这些身份可以参与常规求值；它不会自动强制每个服务，也不会改变这道门之外的其他处理。该设置自 Sandboxie Plus 1.16.0 / Classic 5.71.0 起引入。未找到针对它的专门 SandMan 控件。

## 通知、生命周期与限制

在同一个全局 **程序警报** 区域中，**当强制沙盒化进程被禁止时，提示问题代码 SBIE1301** 对应 `NotifyForceProcessDisabled`，**当进程被强制进入沙盒时，提示问题代码 SBIE1321** 对应 `NotifyForceProcessEnabled`。两者默认均为 `n`。前者在临时暂停期间报告被跳过的强制匹配；后者报告成功的强制分派。两个通知设置都不会启用、禁用或暂停强制。参见 [通知设置](NotificationSettings.md)。

强制与警报配置在应用或重新加载配置之后，影响后续的进程启动决策。会话暂停是驱动的实时状态，按其时长过期。这些控件不会追溯性地移动、终止或挂起进程；不会禁用文件或注册表隔离或 Sandboxie 本身；不会取代沙盒的启动/运行限制；也不会授予提升。通常不必仅为这些控件重启 Windows。
