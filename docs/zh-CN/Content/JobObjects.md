# 作业对象 {#job-objects}

## 概述 {#overview}

Sandboxie 通常会把沙盒化进程分配到由 Sandboxie 管理的 Windows 作业对象中。该作业对象提供进程分组与生存期功能、部分 Windows 作业对象 GUI 限制、相关设置页面所记载的资源限制，以及可选的集体终止行为。

作业对象只是 Sandboxie 架构中的一层。令牌限制、文件系统与注册表隔离、IPC 与对象隔离、网络限制，以及其他 GUI 钩子与策略都另行实现。

## Sandboxie 的作业对象 {#sandboxies-job-object}

Sandboxie 通常为每个沙盒与 Windows 会话的组合维护一个作业对象。沙盒化进程启动时，GuiServer 会查找或创建相应的对象。

如果现有作业对象中仍有活动进程，Sandboxie 会复用它。当它不再包含活动进程后，Sandboxie 会关闭旧句柄，并在下次需要时创建一个全新的作业对象。因此，在创建作业对象时应用的设置会作用于新建的对象。

Sandboxie 在进程初始化期间分配每一个受影响的进程。其根作业对象允许脱离（breakaway），以兼容应用程序和 Windows 作业行为，但 Sandboxie 仍会在每个沙盒化进程启动时对其进行评估，并可再次请求将其关联到根作业。从作业对象脱离本身并不会把进程移出沙盒，也不会禁用 Sandboxie 的其他隔离层。

## 默认的 GUI 限制 {#default-gui-restrictions}

正常的 Sandboxie 作业对象目前应用以下 Windows 作业对象 UI 限制：

| 限制 | 通过作业对象产生的效果 |
| --- | --- |
| `JOB_OBJECT_UILIMIT_EXITWINDOWS` | 阻止作业中的进程使用受该限制控制的 Windows 关机与注销操作。 |
| `JOB_OBJECT_UILIMIT_HANDLES` | 限制对作业外部创建的 USER 句柄的访问，除非明确授予了访问权限。 |
| `JOB_OBJECT_UILIMIT_SYSTEMPARAMETERS` | 限制对系统参数的更改。 |
| `JOB_OBJECT_UILIMIT_READCLIPBOARD` | 限制通过 Windows 作业对象机制读取剪贴板。 |

Sandboxie 会在必要时显式授予所需的 USER 句柄访问权限，包括对桌面窗口的访问。这些限制是额外的 Windows 作业对象层；它们并不实现 Sandboxie 的全部 GUI 或剪贴板隔离。

以下设置会让 Sandboxie 省略这些基本的作业对象 UI 限制，但不会把进程从 Sandboxie 的根作业对象中移除：

- `OpenWndStation=y`
- `OriginalToken=y`
- `UnrestrictedToken=y`

这些设置本身不会移除进程分组，也不会禁用根作业所承载的资源限制。关于 `OpenWndStation` 在窗口站与桌面方面的内容，参见 [Sandbox Desktop and Window Station](SandboxDesktop.md)。

## `NoAddProcessToJob`

```ini
NoAddProcessToJob=y
```

`NoAddProcessToJob` 是一项沙盒级布尔设置。其默认值为未配置或 `n`。

启用后，受影响的沙盒化进程不会被分配到 Sandboxie 的根作业对象。因此：

- 根作业的 GUI 限制不适用于这些进程；
- [进程内存限制](ProcessMemoryLimit.md)、[总内存限制](TotalMemoryLimit.md)、[进程数限制](ProcessNumberLimit.md) 与 [CPU 速率限制](CpuRateLimit.md) 不会通过该根作业生效；
- 通过根作业进行的集体终止不再作为常规机制可用；
- 沙盒化应用程序可以使用自己的作业对象，而这些作业不会嵌套在 Sandboxie 的根作业之下。

此设置不会禁用 Sandboxie。文件系统、注册表、IPC、网络、令牌、GUI 以及其他独立限制仍由各自的设置与实现管辖。

`NoAddProcessToJob` 自 Sandboxie Plus 0.3.5 与 Sandboxie Classic 5.42.1 起可用。

## `AllowBoxedJobs`

```ini
AllowBoxedJobs=y
```

`AllowBoxedJobs` 是一项沙盒级布尔设置。其当前默认值为未配置或 `n`。

与 `NoAddProcessToJob` 不同，此设置不会把进程从 Sandboxie 的根作业对象中移除。在 Windows 8、Windows Server 2012 及支持嵌套作业对象的更高版本上，它允许沙盒化应用程序创建并使用真正嵌套在 Sandboxie 根作业之下的额外作业对象。

当 `AllowBoxedJobs=n` 时：

- 沙盒化应用程序使用的命名作业对象仍在 Sandboxie 的对象命名空间模型内处理；
- Sandboxie 会阻止对沙盒内作业对象的真正分配与终止控制；
- 分配请求可以由兼容性逻辑模拟，而不是创建真正的嵌套分配；
- 作业完成端口与进程创建的作业列表操作会使用相关的兼容性处理。

在受支持的 Windows 版本上使用 `AllowBoxedJobs=y` 时：

- 允许真正的嵌套作业分配；
- 在沙盒对象规则允许的范围内，可以为沙盒内的作业授予分配与终止访问权限；
- Sandboxie 的根作业仍然存在；
- 根作业配置的资源限制保持生效；
- Sandboxie 的对象命名空间隔离继续适用。

当 Sandboxie 的根作业正在使用时，`AllowBoxedJobs=y` 不允许应用程序自有的嵌套作业添加或替换作业对象 UI 限制。沙盒化应用程序设置 `JobObjectBasicUIRestrictions` 的请求出于兼容性会被忽略并报告成功，而 Sandboxie 根作业已经应用的任何 UI 限制保持不变。

Sandboxie 通过其用户模式 API 处理以及驱动层的作业对象访问检查来执行这些决定。

`AllowBoxedJobs` 自 Sandboxie Plus 0.8.5 与 Sandboxie Classic 5.50.5 起可用。

## 对比 {#comparison}

| 配置 | Sandboxie 根作业 | 根作业的 GUI 限制 | 根作业的资源限制 | 应用程序自有的作业对象 |
| --- | --- | --- | --- | --- |
| 正常/默认 | 是 | 是，除非被单独抑制 | 可用且可配置 | 默认受限或由兼容性逻辑模拟 |
| `NoAddProcessToJob=y` | 否 | 否 | 否 | 可在 Sandboxie 根作业之外使用 |
| `AllowBoxedJobs=y` | 是 | 是，除非被单独抑制 | 保持生效 | 在受支持的 Windows 版本上为真正的嵌套作业 |
| `NoSecurityIsolation=y` | 否 | 否 | 否 | 不会仅因 Sandboxie 根作业缺失而被阻止 |

简而言之：

- `NoAddProcessToJob=y` 阻止对该进程使用 Sandboxie 的根作业。
- `AllowBoxedJobs=y` 保留 Sandboxie 的根作业，并允许应用程序自有的嵌套作业。

## 资源限制 {#resource-limits}

Sandboxie 的根作业对象可以承载以下页面所记载的设置：

- [进程内存限制](ProcessMemoryLimit.md)
- [总内存限制](TotalMemoryLimit.md)
- [进程数限制](ProcessNumberLimit.md)
- [CPU 速率限制](CpuRateLimit.md)

`AllowBoxedJobs=y` 不会移除这些限制。当 `NoAddProcessToJob=y`、[`NoSecurityIsolation=y`](NoSecurityIsolation.md) 或 [`OpenWinClass=*`](OpenWinClass.md) 使 Sandboxie 避开该作业时，这些限制便无法通过 Sandboxie 的根作业生效。

`OpenWndStation=y`、`OriginalToken=y` 与 `UnrestrictedToken=y` 只能抑制上文描述的基本作业对象 UI 限制；它们本身不会移除根作业或其资源限制。

## `TerminateJobObject`

```ini
TerminateJobObject=y
```

`TerminateJobObject` 是一项沙盒级布尔设置，在 Sandboxie Plus 1.15.4 与 Sandboxie Classic 5.70.4 中引入。其默认值为未配置或 `n`，目前没有专门的 SandMan 控件。

启用后，符合条件的宿主侧**终止所有进程**（Terminate All）处理可以先尝试终止 Sandboxie 的根作业对象。Sandboxie 的进程服务随后仍会枚举并终止剩余的沙盒化进程，因此作业终止并不是唯一的清理机制。该选项并不保证每个终止请求都会使用作业，尤其是当沙盒没有可用的根作业对象时。

## 应用隔间与相关设置 {#application-compartment-and-related-settings}

在以下配置下：

```ini
NoSecurityIsolation=y
```

应用隔间进程不会被分配到 Sandboxie 的根作业对象。因此，四项根作业 GUI 限制与上文列出的资源限制都不会通过该作业生效。这并不意味着应用隔间进程不能使用它们自己的作业对象。关于该沙盒类型的更广泛行为，参见 [无安全隔离](NoSecurityIsolation.md)。

类似地，`OpenWinClass=*` 会使 Sandboxie 在受影响的配置中避开其根作业对象。根作业的 GUI 限制与资源限制因此不会通过该作业生效。其他窗口类行为记载于 [开放窗口类](OpenWinClass.md)。

## SandMan 配置 {#sandman-configuration}

当前控件位于：

**沙盒选项 > 安全选项 > 作业对象**

**添加沙盒化进程到作业对象 (推荐)**

- 已选中：`NoAddProcessToJob` 保持未配置或处于其默认值。
- 未选中：SandMan 写入 `NoAddProcessToJob=y`。

**允许使用嵌套作业对象(job object) (仅适用于 Windows 8 及更高版本)**

- 已选中：SandMan 写入 `AllowBoxedJobs=y`。
- 未选中：SandMan 移除该设置，恢复其默认值。

当当前沙盒配置无法使用 Sandboxie 的根作业时，SandMan 会禁用相关的作业对象控件，包括应用隔间与 `OpenWinClass=*` 的情形。`TerminateJobObject` 是手动 INI 选项，没有专门的复选框。这些控件不属于新建沙盒向导。

## Sandboxie Control Classic

相关的运行时组件由 Sandboxie Plus 与 Classic 共享，因此兼容的手动 INI 与模板配置可以被该共享运行时使用。

SandMan 为 `NoAddProcessToJob` 与 `AllowBoxedJobs` 提供了当前的专门控件。当前的 Sandboxie Control Classic 既没有为这些设置提供等效的专门控件，也没有为 `TerminateJobObject` 提供；Classic 用户可以在适用的情况下手动配置它们。

## 应用更改 {#applying-configuration-changes}

作业分配决策在进程初始化期间做出。更改 `NoAddProcessToJob` 或 `AllowBoxedJobs` 后，请重启受影响的沙盒化进程。

资源限制与 GUI 限制在 Sandboxie 创建其根作业对象时配置。如果该作业中仍有活动进程，Sandboxie 会复用它。为确保新配置的作业设置生效，请让沙盒变为空，以便 Sandboxie 在下一个进程启动时创建新的作业对象。通常不需要重启 Windows。

## 版本历史 {#version-history}

- Sandboxie Plus 0.3.5 / Classic 5.42.1：引入 `NoAddProcessToJob`。
- Sandboxie Plus 0.5.5 / Classic 5.46.4：兼容性改动使 Chrome 相关应用程序在 `NoAddProcessToJob=y` 时能更充分地使用其作业系统。
- Sandboxie Plus 0.8.5 / Classic 5.50.5：引入 `AllowBoxedJobs`。
- Sandboxie Plus 1.1.1 / Classic 5.56.1：`AllowBoxedJobs=y` 成为默认值。
- Sandboxie Plus 1.1.3 / Classic 5.56.3：在出现兼容性问题后，默认值恢复为 `n`。
- Sandboxie Plus 1.15.4 / Classic 5.70.4：引入 `TerminateJobObject`，以单个进程终止作为常规默认路径。

## 相关页面 {#related-pages}

- [进程内存限制](ProcessMemoryLimit.md)
- [总内存限制](TotalMemoryLimit.md)
- [进程数限制](ProcessNumberLimit.md)
- [CPU 速率限制](CpuRateLimit.md)
- [无安全隔离](NoSecurityIsolation.md)
- [开放窗口类](OpenWinClass.md)
- [Sandbox Desktop and Window Station](SandboxDesktop.md)
