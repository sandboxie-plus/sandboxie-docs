# 启用对象过滤 {#enable-object-filtering}

_EnableObjectFiltering_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置，用于控制 Sandboxie 针对进程与线程句柄的内核对象管理器回调层。该层限制沙盒化进程与同一沙盒之外的目标之间的选定访问。它还支撑 [保密沙盒](ConfidentialBox.md) 所使用的另一套宿主到沙盒保护。

尽管设置名比较宽泛，当前注册的回调专门针对进程与线程句柄。文件、注册表、IPC 命名空间以及其他对象类型由 Sandboxie 的其他机制处理。

## 当前默认值与配置 {#current-default-and-configuration}

对象过滤默认启用。正常运行无需显式添加 `EnableObjectFiltering=y` 条目。

要禁用该全局回调层：

```ini
[GlobalSettings]
EnableObjectFiltering=n
```

当前运行时从 `GlobalSettings` 读取此设置；只把它放进单个沙盒的配置节，并不会控制该沙盒的回调注册。

> [!WARNING]
> 禁用该全局回调层会为所有沙盒移除一项重要的进程/线程访问控制机制。Sandboxie 针对特定系统调用的进程/线程检查在某些路径中仍然保留，但覆盖范围并不相同，不应被视为等效替代。

## 回调过滤的内容 {#what-the-callback-filters}

当前实现为以下操作注册对象管理器回调：

- 进程句柄；
- 线程句柄；
- 新建句柄；
- 句柄复制。

对于这些操作，Sandboxie 可以保持请求的访问权限不变，也可以按进程/线程访问策略削减它。在正常的拒绝路径中，请求的访问掩码会被削减为零。回调本身允许 Windows 继续处理该句柄操作，因此应用程序不应指望每个被限制的请求都返回某一个特定的 Win32 或 NT 错误。

创建或复制内核句柄的操作不会被该回调修改。这是句柄操作自身的性质，并不意味着任意用户态请求都能绕过该过滤器。

更改只影响后续的进程/线程句柄创建与复制：它不会追溯削减既有句柄中的权限，不会为先前受限的句柄追加权限，也不会使既有句柄失效。

## 进程与线程访问策略 {#process-and-thread-access-policy}

同一有效沙盒内部的进程或线程访问，通常会被该策略允许。一个沙盒中的进程以另一个沙盒中的进程或线程为目标时，会被视为沙盒外；`HideOtherBoxes` 一类的可见性控制与句柄访问过滤是相互独立的。

对于沙盒外的目标，Sandboxie 会限制那些可用于修改或控制目标的进程与线程权限。进程内存的读取访问与写入/控制访问分开处理。

该策略与 IPC 资源规则中针对进程目标的那些形式相配合：

```ini
OpenIpcPath=$:target.exe
ReadIpcPath=$:target.exe
ClosedIpcPath=$:target.exe
```

在这种用法中，匹配的 `ClosedIpcPath` 规则先于 `OpenIpcPath` 求值，随后在只读访问适用时轮到 `ReadIpcPath`。`OpenIpcPath` 可以放开原本受限的访问，`ReadIpcPath` 只作用于受支持的读取类别，`$:*` 则匹配每一个目标进程。Sandboxie 规则放行某个请求之后，Windows 正常的访问控制仍然生效。

资源规则的更广泛行为参见 [开放 IPC 路径](OpenIpcPath.md)、[读取 IPC 路径](ReadIpcPath.md) 与 [封禁 IPC 路径](ClosedIpcPath.md)。

## 回调过滤与系统调用专属过滤 {#callback-and-syscall-specific-filtering}

Sandboxie 目前有两层相关的进程/线程过滤：

1. 全局对象管理器回调层，独立于用户态 API 或引发该操作的 Sandboxie 系统调用专属检查，对受支持的句柄创建与复制进行过滤。
2. 系统调用专属的驱动程序路径，保留对打开、枚举或复制进程与线程句柄等操作的检查。

两层共用策略代码，但覆盖范围并不相同。全局回调处于活动状态时，重叠的系统调用路径通常会让位于回调。若回调未安装，当前的系统调用专属路径会在已实现之处继续施加自己的检查。

这一区别意味着 `EnableObjectFiltering=n` 与按沙盒生效的 [禁用对象过滤器](DisableObjectFilter.md) 设置并不等价。

| 配置 | 作用范围 | 对象管理器回调 | 效果 |
| --- | --- | --- | --- |
| 默认 | 全局 | 已安装 | 常规的进程/线程回调过滤 |
| `EnableObjectFiltering=n` | 全局 | 未安装 | 为所有沙盒移除回调层；系统调用专属检查可能仍然保留 |
| `DisableObjectFilter=y` | 受影响的沙盒化进程 | 仍然安装 | 放宽这些进程的出站回调过滤 |
| 带 `NoSecurityFiltering=y` 的应用隔间 | 受影响的应用隔间进程 | 仍全局安装 | 启用按进程的文件、注册表项与对象过滤禁用状态 |

## 宿主到沙盒的保护 {#host-to-sandbox-protection}

当非沙盒化的宿主进程请求指向某个沙盒化进程或线程的句柄时，该回调还会执行一项独立的检查。这条路径支撑 `DenyHostAccess`、`ProtectAdminOnly` 与 `NotifyBoxProtected` 等设置，也支撑保密沙盒额外的进程保护。

宿主到沙盒的检查与沙盒化进程的出站过滤状态相互独立。在全局回调层仍然活动时，在目标沙盒中设置 `DisableObjectFilter=y` 本身并不会禁用这项保护。该路径保留了一些运行层面的例外，供管理或运行沙盒所必需的 Sandboxie 与 Windows 组件使用。

面向用户的宿主访问策略参见 [保密沙盒](ConfidentialBox.md)。

## 应用隔间 {#application-compartment}

[应用隔间](NoSecurityIsolation.md) 模式本身并不会禁用对象管理器回调。在 `NoSecurityIsolation=y` 且保持常规过滤的情况下，应用隔间进程仍可能受这一进程/线程访问策略约束。

当同时启用 [无安全过滤](NoSecurityFiltering.md) 时，新建的应用隔间进程会获得相应的按进程文件、注册表项与对象过滤禁用状态。回调仍全局注册，其他沙盒仍正常受到过滤。

## SandMan 界面 {#sandman-interface}

全局控件位于：

**全局设置 > 高级选项 > 沙盒配置 > 激活内核模式的对象过滤器**

该复选框默认处于选中状态。选中时，SandMan 通常会移除显式的禁用覆盖，依赖运行时的默认启用状态。清除它会写入 `EnableObjectFiltering=n`。

保存这项全局功能设置可能通过驱动程序重新配置来注册或注销回调层，通常不需要重启 Windows 或常规地重启驱动程序。

如果在驱动程序启动期间需要注册回调但注册失败，驱动程序初始化会失败，Sandboxie 会记录该注册问题。后续重新配置期间的失败会被记录，并使该回调功能保持未激活状态；具体的界面呈现可能有所不同。

## 应用更改 {#applying-changes}

更改该全局设置会影响后续的进程/线程句柄创建与复制，包括已运行进程在重新配置之后发出的请求。它不会改变已经打开的句柄。

相比之下，`DisableObjectFilter` 是在每个沙盒化进程初始化时存储的。更改该设置后，请重启受影响的沙盒化进程。

## 版本历史 {#version-history}

该回调功能在 Sandboxie Plus 1.0.0 / Classic 5.55.0 中作为实验性功能引入，最初需要显式设置 `EnableObjectFiltering=y`。自 Sandboxie Plus 1.0.16 / Classic 5.55.16 起，它改为默认启用。

## 相关页面 {#related-pages}

- [禁用对象过滤器](DisableObjectFilter.md)
- [无安全过滤](NoSecurityFiltering.md)
- [无安全隔离](NoSecurityIsolation.md)
- [保密沙盒](ConfidentialBox.md)
- [开放 IPC 路径](OpenIpcPath.md)
- [读取 IPC 路径](ReadIpcPath.md)
- [封禁 IPC 路径](ClosedIpcPath.md)
- [Sandboxie Ini](SandboxieIni.md)
