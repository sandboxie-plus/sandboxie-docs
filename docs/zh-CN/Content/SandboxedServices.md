# 沙盒化服务 {#sandboxed-services}

Sandboxie 可以拦截并模拟选定的 Windows 服务控制管理器（SCM）操作，使某些服务作为与沙盒关联的进程运行。这是 SbieDll 的 API 拦截、沙盒化服务的配置与状态、SbieSvc 执行的权限操作，以及在需要执行宿主服务操作时访问真实 Windows SCM 这几部分的组合。

它并不是对 Windows SCM 的完整克隆或完全虚拟化。Sandboxie 有选择地拦截并模拟 SCM 操作，把沙盒化服务的配置与状态保存在沙盒内，并使用 SbieSvc 执行权限操作或与真实 SCM 通信。

## SandboxService {#sandboxservice}

`SandboxService` 用于选择应使用 Sandboxie 沙盒化服务模型的服务：

```ini
SandboxService=ServiceName
```

支持多个条目：

```ini
SandboxService=ServiceOne
SandboxService=ServiceTwo
```

默认值为空列表。服务名按精确、不区分大小写的方式匹配。不支持通配符、取反和按可执行文件限定的形式。

`SandboxService` 本身不会选择 SYSTEM 身份。它只影响匹配的服务是否按沙盒化服务处理。

## 服务被视为沙盒化的条件 {#what-makes-a-service-sandboxed}

在其他内部路径之外，Sandboxie 可以在以下情况下把服务归类为沙盒化：

- 它是在沙盒内创建的，并出现在沙盒化服务状态中；
- 它的名称匹配某个 `SandboxService` 条目；
- Sandboxie 对该服务有内置处理。

这些内置情形属于实现细节，不应被视为 `SandboxService` 所支持服务的通用清单。

## 启动沙盒化服务 {#starting-a-sandboxed-service}

当被拦截的 `StartService` 请求指向一个被归类为沙盒内的服务时，Sandboxie 不会简单地要求宿主 SCM 启动已有的宿主实例。大致流程如下：

```text
沙盒化的 StartService 请求
       |
       v
Sandboxie 将该服务归类为沙盒内服务
       |
       v
虚拟状态 -> START_PENDING
       |
       v
SbieSvc 通过 Sandboxie 启动服务可执行文件
       |
       v
服务进程与沙盒建立关联
       |
       v
沙盒化服务状态 -> RUNNING
```

该图概括的是 Sandboxie 的状态处理，而不是规定确切的 Windows SCM 时序。

已经在运行的宿主服务不会被自动移入沙盒、被终止或被收编为沙盒化实例。某个服务是否支持独立的沙盒化实例，取决于该服务本身。如果服务缺失，或无法通过沙盒化服务路径启动，操作会失败，而不会有意回退去启动真实的宿主服务。

## 沙盒化 SCM 模型 {#sandboxed-scm-model}

SbieDll 拦截服务的打开、创建、启动、查询和调度器路径。在沙盒内创建的服务配置可以通过虚拟化的注册表状态保存，Sandboxie 会在需要时维护合成的句柄或服务状态。当某项操作是针对宿主服务的，SbieSvc 会执行权限操作并与真实 SCM 通信。

这种分工让沙盒化进程可以使用熟悉的 SCM API，但并不意味着每一种 SCM 行为都被完全虚拟化。

## RunServiceAsSystem {#runserviceassystem}

`RunServiceAsSystem` 为指定的沙盒化服务选择 SYSTEM 源身份：

```ini
RunServiceAsSystem=ServiceName
```

支持多个条目。默认值为空列表。匹配方式为精确且不区分大小写；不支持通配符、取反和按可执行文件限定的形式。

`RunServiceAsSystem` 改变的是启动匹配的沙盒化服务时使用的源身份。它本身不会把宿主服务移入沙盒。该服务必须另行被归类为沙盒化，例如通过 `SandboxService`。

## RunServicesAsSystem {#runservicesassystem}

宽泛形式如下：

```ini
RunServicesAsSystem=y
```

其默认值为 `n`（禁用）。启用后，服务启动路径可以宽泛地为沙盒化服务选择 SYSTEM 身份，具体受当前的特例逻辑约束。

历史元数据中提到 RpcSs 和 DcomLaunch 的表述，并不完整描述当前的可执行文件行为。该设置既不限于这两个名称，也不是“无论特例如何、每个沙盒化服务都会使用 SYSTEM”的无条件保证。

### 选择性形式与宽泛形式 {#selective-and-broad-forms}

`RunServiceAsSystem=<name>` 只针对指定的服务。`RunServicesAsSystem=y` 启用更宽泛的 SYSTEM 源选择，因此未被选择性设置点名的服务，在当前逻辑允许的情况下仍可走宽泛路径。添加选择性条目不会取消针对其他服务的全局设置。

当只有特定服务需要 SYSTEM 源身份时，选择性形式更有用。

## RunRpcssAsSystem {#runrpcssassystem}

`RunRpcssAsSystem` 控制 SbieSvc 启动与沙盒关联的 RpcSs 进程时使用的源身份：

```ini
RunRpcssAsSystem=y
```

默认值为 `n`。显式设为 `y` 会让 SbieSvc 为沙盒化 RpcSs 的启动复制其 SYSTEM 源令牌。生成的 `SandboxieRpcSs` 进程仍与沙盒关联；该设置不会启动或收编非沙盒化的宿主 RpcSs 服务。

> [!WARNING]
> 以 SYSTEM 源令牌启动沙盒化 RpcSs，会放大该进程仍可访问的资源被滥用时的后果。仅在确有需要时使用此兼容性选项。它本身并不会把 RpcSs 移出沙盒。

### 应用隔间与 OriginalToken {#application-compartment-and-originaltoken}

当前的服务启动逻辑在以下两个条件同时成立时，可以自动选择相同的 SYSTEM 源路径：

1. 调用方处于应用隔间模式，或配置了 `OriginalToken=y`；且
2. 启用了 `MsiInstallerExemptions=y` 或 `RunServicesAsSystem=y` 之一。

因此，仅处于应用隔间并不会自动让沙盒化 RpcSs 使用 SYSTEM 源令牌。

沙盒化的 DcomLaunch 通过沙盒化 RpcSs/服务器流程启动。上述显式的令牌源决定是针对 RpcSs 启动做出的；不应将其推广为一条独立的、完全相同的 DcomLaunch 令牌选择规则。

### SandMan 控件 {#sandman-control}

该控件位于 **沙盒选项 > 安全选项 > 高级安全**，标签为：

> 以 SYSTEM 进程启动沙盒内的 RpcSs（不推荐）

SandMan 会从显式的 `RunRpcssAsSystem` 值加载此复选框。在应用隔间模式下，如果宽泛的 `RunServicesAsSystem` 行为或 `MsiInstallerExemptions` 已经触发上文所述的自动运行时条件，该直接控件会被禁用。

有关绑定解析、端点过滤、超时行为和沙盒化 RpcSs 启动架构，参见 [RPC 兼容性](RpcCompatibility.md)。

## “以 SYSTEM 身份”的含义 {#what-as-system-means}

对于这条服务启动路径，Sandboxie 从以 LocalSystem 身份运行的 SbieSvc 获取源令牌，复制主令牌、调整其会话，并用它启动沙盒化的服务进程。在适用的情况下，Sandboxie 默认还会执行服务侧的权限剥离。

因此，“以 SYSTEM 运行”描述的是启动沙盒化服务时使用的源身份。它并不意味着一个在沙盒之外运行的、不受限制的 LocalSystem 进程。

在常规隔离沙盒中：

- 进程仍与沙盒关联；
- 常规的 Sandboxie 令牌与隔离流程仍然可以生效；
- 文件、注册表、IPC 及其他隔离机制仍然独立。

`NoSecurityIsolation` / 应用隔间会改变后续的令牌与隔离行为，因此本页的设置并不保证在任何沙盒模式下都得到完全相同的最终令牌。

## 相关的特殊情形 {#related-special-cases}

[MSI 安装程序豁免](MsiInstallerExemptions.md) 可以改变 MSIServer 的处理方式，CryptSvc 也有当前的特例行为。这些机制与服务身份相关，但并不是本页所记录设置的通用替代品。

## Chromium 提权模板 {#chromium-elevation-template}

当前的 `Chromium_Elevation` 模板使用以下模式：

```ini
OpenSamEndpoint=y

SandboxService=MicrosoftEdgeElevationService
RunServiceAsSystem=MicrosoftEdgeElevationService

SandboxService=MicrosoftEdgeDevElevationService
RunServiceAsSystem=MicrosoftEdgeDevElevationService

SandboxService=MicrosoftCopilotElevationService
RunServiceAsSystem=MicrosoftCopilotElevationService

SandboxService=GoogleChromeElevationService
RunServiceAsSystem=GoogleChromeElevationService

SandboxService=GoogleChromeDevElevationService
RunServiceAsSystem=GoogleChromeDevElevationService

SandboxService=BraveElevationService
RunServiceAsSystem=BraveElevationService
```

该模板提供兼容性流程中三个彼此独立的部分：

`SandboxService`
: 把指定的提权服务交由 Sandboxie 的沙盒化服务模型处理。

`RunServiceAsSystem`
: 仅为该指定的提权服务使用 SYSTEM 源身份。

`OpenSamEndpoint`
: 移除该兼容性流程所需的 SAM 消息过滤器。参见 [系统端点](SystemEndpoints.md)。

模板已从宽泛的 `RunServicesAsSystem=y` 行为改为选择性的 `RunServiceAsSystem=...` 条目。这样把 SYSTEM 源选择限制在指定的提权服务上，而不是把宽泛设置应用到其他沙盒化服务。

该模板由 Sandboxie 维护，通常无需手动复制。

## 与 DPAPI 的关系 {#dpapi-relationship}

Sandboxie 有独立的 DPAPI 兼容性与代理处理。近期的 Chromium 提权工作调整了涉及以 SYSTEM 运行服务的 DPAPI 场景所使用的身份。

`OpenSamEndpoint` 并不实现 DPAPI，也不解密凭据。兼容性仍取决于有效的 Windows 身份、Windows DPAPI 规则、Chromium 的行为与策略、应用绑定加密或相关机制，以及提权服务的可用性与配置。本页的设置不保证能够访问宿主凭据。

## 失败时的行为 {#failure-behavior}

沙盒化服务路径没有“沙盒内启动失败后再启动真实宿主服务”的通用回退：

- 不存在或不可用的服务会启动失败；
- 驱动服务以及不支持的非 Win32 服务类型会被沙盒化服务路径拒绝；
- 已经在运行的宿主实例不会被自动收编；
- 无法获取或复制 SYSTEM 源令牌，或无法创建沙盒化进程时，服务启动会失败；
- 未发现有意回退到另一个限制更少的宿主令牌的行为。

具体的 Windows 错误可能取决于失败发生的环节。

## 应用更改 {#applying-changes}

`SandboxService` 会在服务分类和启动操作期间被评估。新值可以影响后续的启动，但不会移动已经在运行的服务实例。

`RunServiceAsSystem` 和 `RunServicesAsSystem` 在服务进程启动时才会起作用。更改任一设置都不会追溯替换已经分配的服务令牌。

更改服务身份设置后，请重启受影响的沙盒化服务或进程。需要进行干净的配置测试时，请重建沙盒化的进程树。通常不需要重启 SandMan、SbieSvc 或驱动程序。

## SandMan 配置 {#sandman-configuration}

宽泛设置暴露在 **沙盒选项 > 安全选项 > 高级安全** 下，标签为：

> 不使用系统令牌启动沙盒化的服务 (推荐)

该复选框的语义与 `RunServicesAsSystem` 相反：

- 选中时，宽泛的 `RunServicesAsSystem=y` 行为被禁用；
- 清除时，SandMan 可以写入 `RunServicesAsSystem=y`。

`SandboxService` 和 `RunServiceAsSystem` 目前没有专门的 SandMan 控件；它们是手动设置或模板设置。新沙盒向导不会暴露这些控件。

## Sandboxie Plus 与 Classic {#sandboxie-plus-and-classic}

运行时由共享的 Sandboxie 组件实现。SandMan 提供当前的 `RunServicesAsSystem` 控件，而 `SandboxService` 和 `RunServiceAsSystem` 仍属手动或模板设置。这并不意味着 Sandboxie Control（Classic）中有等效的当前控件。

## 版本历史 {#version-history}

| 设置或变更 | 引入版本 |
| --- | --- |
| `RunServicesAsSystem` | Sandboxie Plus 0.5.4 / Classic 5.46.0 |
| `RunServiceAsSystem` | Sandboxie Plus 0.5.4b / Classic 5.46.1 |
| `SandboxService` | Sandboxie Plus 0.5.5 / Classic 5.46.4 |
| `RunRpcssAsSystem` | Sandboxie Plus 0.9.7 |
| Chromium 提权与 DPAPI 兼容性工作 | Sandboxie Plus 1.18.0 / Classic 5.73.0 时期 |
| 选择性 Chromium 提权模板 | Sandboxie Plus 1.18.1 / Classic 5.73.1 |

这些服务设置早于它们当前在 Chromium 提权中的用途。

## 相关页面 {#related-pages}

- [RPC 兼容性](RpcCompatibility.md)
- [系统端点](SystemEndpoints.md)
- [服务程序](ServicePrograms.md)
- [启动服务](StartService.md) — 一项生命周期/启动设置，并不等同于 `SandboxService`
- [MSI 安装程序豁免](MsiInstallerExemptions.md)
- [Sandboxie Ini](SandboxieIni.md)
