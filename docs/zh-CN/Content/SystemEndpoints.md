# 系统端点 {#system-endpoints}

Sandboxie 允许与 Windows 系统服务进行部分 IPC 和 RPC 通信，同时对敏感端点施加专门的消息级过滤。本页的设置用于在兼容性需要时禁用其中某一项端点专属过滤器。

它们并不会通用地开放 LSA、SAM 或 WPAD。通用的 IPC 可达性、Windows 正常的访问检查，以及 Sandboxie 的其他无关限制，仍然各自独立。

典型配置为：

```ini
OpenLsaEndpoint=y
OpenSamEndpoint=y
OpenWPADEndpoint=y
```

这三个设置都是沙盒范围的布尔选项，默认禁用，且不按可执行文件限定。它们可以通过常规的有效 Sandboxie 配置（包括模板）继承。

## IPC 可达性与端点过滤 {#ipc-reachability-and-endpoint-filtering}

Sandboxie 把通用的 IPC 可达性与端点专属的请求过滤作为两个独立的层来处理：

```text
沙盒化进程
       |
       v
通用 IPC 路径/对象策略
       |
       +-- 被拒绝 -> 连接失败
       |
       v
端点可达
       |
       v
端点专属操作过滤器
       |
       v
请求被允许或被拒绝
```

[开放 IPC 路径](OpenIpcPath.md) 可以让某个 IPC 对象变得可达，而 [封禁 IPC 路径](ClosedIpcPath.md) 可以拒绝可达性。本页记录的 `Open...Endpoint` 设置影响的是更靠后的、专门的操作过滤器。开放 IPC 路径并不会自动移除该过滤器，端点设置也不会自动让一个被封闭的 IPC 对象变得可达。

## OpenLsaEndpoint {#openlsaendpoint}

```ini
OpenLsaEndpoint=y
```

默认值为 `n`（禁用）。

Sandboxie 在 SbieDrv 中直接处理以下固定端点：

```text
\RPC Control\LSARPC_ENDPOINT
```

默认情况下，Sandboxie 对选定的敏感 LSA RPC 操作施加拒绝列表。该过滤器涵盖修改策略或安全状态、审核配置、帐户与受信任域、帐户权限与特权、配额与系统访问状态，以及私有数据状态的操作。它并不会一概阻止 LSA 查询或枚举。

`OpenLsaEndpoint` 会禁用 Sandboxie 针对 `LSARPC_ENDPOINT` 上敏感操作的专门过滤器。它不会授予对 LSA 的不受限制的访问权限，也不会禁用 Windows 正常的访问检查。

### 安全背景 {#security-history}

LSA 端点过滤器在 Sandboxie Plus 0.5.4 / Classic 5.46.0 中引入，用于应对后来被追踪为安全议题 ID-8 / CVE-2019-13502 的问题。该过滤器仍然默认启用；`OpenLsaEndpoint=y` 是为需要执行会被该过滤器拒绝的操作的软件提供的兼容性放宽。

## OpenSamEndpoint {#opensamendpoint}

```ini
OpenSamEndpoint=y
```

默认值为 `n`（禁用）。

Sandboxie 同样在 SbieDrv 中直接处理以下固定端点：

```text
\RPC Control\samss lpc
```

常规的 SAM 请求过滤器涵盖敏感的变更类别，例如用户与帐户的创建或删除、组与别名更改、成员关系更改、密码更改、帐户属性与策略，以及安全更改。这并不意味着所有 SAM 请求都会被拒绝。

`OpenSamEndpoint` 会禁用 Sandboxie 的 SAM 端点请求过滤器。它本身不会暴露全部 SAM 数据、不会绕过 Windows 访问检查，也不提供宿主凭据。

该过滤器及其兼容性设置在 Sandboxie Plus 0.7.0 / Classic 5.48.0 中引入，起因是一起涉及提权后的沙盒化进程修改帐户或密码状态的安全问题。

### Chromium 提权服务 {#chromium-elevation-services}

当前的 Chromium 提权兼容性模板按以下模式组合这些设置：

```ini
SandboxService=<service>
RunServiceAsSystem=<service>
OpenSamEndpoint=y
```

`SandboxService` 把提权服务纳入 Sandboxie 的沙盒化服务模型，`RunServiceAsSystem` 为该服务提供所需的源身份，`OpenSamEndpoint` 则移除该兼容性流程所需的 SAM 过滤器。仅设置 `OpenSamEndpoint` 并不会实现 DPAPI 兼容性，也不会授予对宿主凭据的访问权限。参见 [沙盒化服务](SandboxedServices.md)。

## OpenWPADEndpoint {#openwpadendpoint}

```ini
OpenWPADEndpoint=y
```

默认值为 `n`（禁用）。该设置于 Sandboxie Plus 1.15.0 / Classic 5.70.0 引入。

此设置涉及与 Windows Web 代理自动发现及 `WinHttpAutoProxySvc` 关联的动态 RPC 端点。与固定的 LSA 和 SAM 端点不同，WPAD 端点是在运行时发现并注册的：

```text
SbieDll
  |
  v
请求动态 RPC 端点解析
  |
  v
SbieSvc / EpMapperServer
  |
  v
解析 WPAD 服务端点
  |
  v
向 SbieDrv 注册端点 + 过滤器
  |
  v
驱动程序应用消息过滤器
```

Sandboxie 通常会为该端点注册一个过滤器，用于处理与代理配置、策略和凭据相关的选定敏感操作。设置 `OpenWPADEndpoint=y` 后，该端点会在不附带这一专门过滤器的情况下注册。

因此，`OpenWPADEndpoint` 允许那些原本会被 Sandboxie 过滤的 WPAD 操作。它不会提供不受限制的网络、代理、WinHTTP 或 Internet 访问权限。

## 固定实现与动态实现 {#fixed-and-dynamic-implementations}

这些设置的效果在概念上相似，但使用不同的实现路径：

| 设置 | 端点处理方式 | 启用后的效果 |
| --- | --- | --- |
| `OpenLsaEndpoint` | 在 SbieDrv 中直接过滤的固定端点 | 跳过专门的 LSA 操作过滤器 |
| `OpenSamEndpoint` | 在 SbieDrv 中直接过滤的固定端点 | 跳过专门的 SAM 请求过滤器 |
| `OpenWPADEndpoint` | 由 SbieDll 与 SbieSvc 解析、再注册到 SbieDrv 的动态端点 | 在不附带专门消息过滤器的情况下注册 WPAD |

## 与 BlockPassword 的关系 {#blockpassword-relationship}

[`BlockPassword`](BlockPassword.md) 控制的是另一项遗留的 LSA 身份验证与密码相关过滤器。当前运行时仍会查询它，尽管在现代的密码更改兼容性场景中，它已被 `OpenSamEndpoint` 取代。它不是 `OpenLsaEndpoint` 或 `OpenSamEndpoint` 的别名。`OpenLsaSSPI` 尚未被确认为当前的 INI 设置。

## SandMan 配置 {#sandman-configuration}

这些控件位于 **沙盒选项 > 常规选项 > 隔离**：

| 设置 | 当前标签 |
| --- | --- |
| `OpenLsaEndpoint` | 开放 Windows 本地安全验证 (LSA) 的访问权限 |
| `OpenSamEndpoint` | 开放 Windows 安全帐户管理器 (SAM) 的访问权限 |
| `OpenWPADEndpoint` | 打开对代理配置的访问权限 |

这些标签比本页描述的精确操作过滤行为更宽泛。控件默认处于未勾选状态，启用时写入 `y`，禁用时移除该显式键。当 `NoSecurityIsolation` / 应用隔间行为生效时，这些控件会被禁用。这一界面状态不应被理解为在该模式下每条端点路径都不受限制的保证。

这些控件目前未在新沙盒向导中提供。

## 应用更改 {#applying-changes}

LSA 和 SAM 设置会在沙盒化进程的 IPC 初始化期间被缓存。更改后，请重启受影响的沙盒化进程，或重建沙盒化的进程树。

请在启动受影响的应用程序之前配置 `OpenWPADEndpoint`。更改后建议重启受影响的沙盒化进程树。动态端点是单独解析和注册的，其当前的缓存行为不应被理解为“仅重启某一个应用程序就必定重建全局端点过滤状态”的保证。

这些设置并不普遍要求重启 SandMan、SbieSvc 或驱动程序。

## 失败时的行为 {#failure-behavior}

被其常规专门过滤器选中的 LSA 和 SAM 操作会被拒绝。如果 WPAD 端点解析或注册失败，相应的 RPC 或绑定操作可能失败；目前没有确立不受限制的回退路径。通用的 IPC 策略也可能在到达端点专属过滤之前就拒绝通信。可观察到的错误取决于失败的层级，因此单一错误码无法描述所有情况。

## Sandboxie Plus 与 Classic {#sandboxie-plus-and-classic}

运行时支持由共享的 Sandboxie 组件实现。SandMan 提供上文所述的控件，兼容的手动设置也可以被共享运行时读取。这并不意味着 Sandboxie Control（Classic）提供等效的当前控件。

## 版本历史 {#version-history}

| 设置 | 引入版本 |
| --- | --- |
| `OpenLsaEndpoint` | Sandboxie Plus 0.5.4 / Classic 5.46.0 |
| `OpenSamEndpoint` | Sandboxie Plus 0.7.0 / Classic 5.48.0 |
| `OpenWPADEndpoint` | Sandboxie Plus 1.15.0 / Classic 5.70.0 |

## 相关页面 {#related-pages}

- [RPC 兼容性](RpcCompatibility.md)
- [开放 IPC 路径](OpenIpcPath.md)
- [封禁 IPC 路径](ClosedIpcPath.md)
- [阻止密码更改](BlockPassword.md)
- [沙盒化服务](SandboxedServices.md)
- [Sandboxie Ini](SandboxieIni.md)
