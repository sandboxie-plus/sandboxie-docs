# RPC 兼容性 {#rpc-compatibility}

Sandboxie 为使用 Windows 远程过程调用（RPC）的应用程序提供了兼容性处理。这些处理帮助沙盒化进程构造合适的绑定、解析动态本地端点、应用通信超时调整，以及连接到选定的宿主服务，同时不替换 Windows RPC 运行时。

这些机制并不是通用的 RPC 防火墙。通用的 IPC 可达性、Windows 访问检查、按端点过滤请求，以及沙盒化服务进程的身份，是整体模型中各自独立的部分。

## 架构概述 {#architecture-overview}

RPC 兼容性涉及 Sandboxie 的多个组件：

```text
沙盒化应用程序
        |
        v
SbieDll 的 RPC 绑定拦截
        |
        +-- 可选的绑定预设与超时判定
        |
        +-- 可选的动态端点请求
                    |
                    v
             SbieSvc 端点映射器辅助程序
                    |
                    +-- Windows 端点映射器或服务进程查找
                    |
                    v
             SbieDrv 的动态端口注册与可选过滤器
                    |
                    v
             Windows RPC 端点
```

内置模板提供了受支持的兼容性场景所需的、由项目维护的映射。LSA、SAM、WPAD 及相关服务的端点专属安全行为记录在 [系统端点](SystemEndpoints.md) 下。

## RPC 绑定预设 {#rpc-binding-presets}

`RpcPortBinding` 为 RPC 绑定提供高级兼容性预设。每个预设都会匹配调用模块以及绑定操作提供的一个标识符：

- 对于 `RpcBindingCreateW`，该标识符是绑定模板的对象 UUID。
- 对于 `RpcBindingFromStringBindingW`，配置的模式会与完整的字符串绑定进行匹配。

用于此匹配的对象 UUID 不应与用于端点查找的 RPC 接口 UUID 混淆。

简言之：**对象 UUID = 哪个对象；接口 UUID = 哪些操作；字符串绑定 = 如何到达它。**

示意形式如下：

```ini
RpcPortBinding=<module>,<object-UUID-or-string-binding-pattern>[,Resolve=<port-id>][,TimeOut=y|n]
```

当某个预设匹配时，Sandboxie 可以提供本地端点并调整通信超时。`Resolve=<port-id>` 会请求使用下文所述的映射进行端点查找。在 `RpcBindingCreateW` 路径中，端点替换只适用于尚未指定端点的本地 RPC 绑定。

如果没有预设匹配，Sandboxie 会继续走正常的绑定路径。未匹配的预设不会拒绝访问。

解析器还支持由项目维护的模板所使用的内部形式。请优先使用这些模板，不要把每一种受支持的形式或端点标识符都当作稳定的手动配置接口。

### 动态端点映射 {#dynamic-endpoint-mappings}

有两个相关设置向端点映射器辅助程序提供 `Resolve=` 所需的信息：

- `RpcPortBindingIfId` 把逻辑端口标识符映射到 RPC 接口 UUID。随后 SbieSvc 可以向 Windows 端点映射器查询匹配的当前端点。
- `RpcPortBindingSvc` 把逻辑端口标识符映射到 Windows 服务名。SbieSvc 会识别该服务的进程，并向驱动程序查询该进程当前的动态 RPC 端口。

这些设置主要是由项目维护的模板与服务解析方面的底层配套机制。接口 UUID 和服务端点细节可能随 Windows 变化，不应直接从模板中盲目复制。

## 动态端口过滤 {#dynamic-port-filtering}

`RpcPortFilter` 为 Sandboxie 全局注册到驱动程序的动态解析端口提供请求过滤。SbieSvc 读取维护的过滤条目，并把解析出的端口和过滤器标识符提交给 SbieDrv。驱动程序通过其仅限服务的路径接受该注册，检查发往已注册端口的请求，并对配置中匹配的请求返回“拒绝访问”。

过滤条目中可选的函数名仅供说明；当前的执行逻辑使用的是配置的请求标识符，而不是该标签。对于受支持的特殊端点，`Open<Name>Endpoint` 选项可以在端点注册时抑制相应的过滤器。

> [!WARNING]
> `RpcPortFilter` 使用的请求标识符是与协议和版本相关的实现细节。错误的取值可能阻断合法的 RPC 活动。请优先使用 Sandboxie 维护的模板，不要凭空编写条目，也不要把消息标识符当成稳定的 RPC 授权 API 来复制。

`RpcPortFilter` 并不过滤所有 RPC 端点，也不是通用的 RPC 防火墙。受支持的端点专属兼容性控制参见 [系统端点](SystemEndpoints.md)。

## RPC 通信超时 {#rpc-communication-timeout}

Sandboxie 通常会对绑定句柄应用 RPC 通信超时调整。`RpcMgmtSetComTimeout` 的当前运行时默认值在未配置该项时为启用。

要显式禁用默认调整：

```ini
[DefaultBox]
RpcMgmtSetComTimeout=n
```

此设置会改变兼容性和计时行为。它不会授予端点访问权限、阻断端点，也不提供防火墙功能。

在 SandMan 中，该控件位于 **沙盒选项 > 其它杂项 > 兼容性**，标签为：

> 默认禁用 RpcMgmtSetComTimeout (或许可以解决兼容性问题)

复选框的状态与设置有反向关系：

- 选中时写入 `RpcMgmtSetComTimeout=n`；
- 清除时保持正常的启用行为。

### 调用模块覆盖 {#calling-module-override}

`UseRpcMgmtSetComTimeout` 是一种高级的、按调用模块限定的覆盖，用于当前绑定尚未提供其超时判定的情况。例如，维护的模板可以为源自特定 DLL 的调用选择不同的超时行为。

`UseRpcMgmtSetComTimeout` 允许对源自特定模块（例如某个 DLL）的调用采用不同的超时行为。Sandboxie 会先检查此设置，然后再查找匹配的 `RpcPortBinding` 预设。

如果匹配的预设包含 `TimeOut=`，该值会覆盖按模块的判定。否则，即使有绑定预设匹配，按模块的判定仍然生效。如果两者都没有提供覆盖，Sandboxie 会使用进程的 `RpcMgmtSetComTimeout` 默认值。

## 沙盒化 RpcSs 的启动 {#sandboxed-rpcss-startup}

当进程需要沙盒化的端点映射器时，Sandboxie 通常会启动与其沙盒关联的 RpcSs。该 RpcSs 进而可以通过特殊的服务器启动流程启动沙盒化的 DcomLaunch 进程。这些是与沙盒关联的 Sandboxie 服务可执行文件，而不是非沙盒化的宿主服务实例。

`NoSandboxieRpcSs` 会让特殊的服务器启动辅助程序在处理相关端点请求时，在启动沙盒化 RpcSs 或 DcomLaunch 之前就返回。它不会禁用 Windows RPC、不会阻断所有 RPC 通信，也不会禁用 `RpcPortBinding`。此选项没有记录受支持的通用用户工作流，因此应将其视为内部的兼容性行为，而不是常规配置控件。

用于启动沙盒化 RpcSs 的身份由另一项设置控制。参见 [沙盒化服务](SandboxedServices.md#runrpcssassystem)。

## 应用更改 {#applying-changes}

RPC 超时默认值会在每个沙盒化进程中初始化，而按模块的绑定判定则在创建绑定之时做出。动态端点也会按需解析和注册。更改这些设置后，请重启受影响的沙盒化进程，或重建沙盒化的进程树，以免沿用已有的绑定和缓存的端点信息。

更改 RpcSs 的启动身份需要重启沙盒化 RpcSs 进程。仅因这些配置更改，通常不需要重启 SandMan、SbieSvc 或驱动程序。

## 版本历史 {#version-history}

| 设置或机制 | 引入版本 |
| --- | --- |
| `RpcMgmtSetComTimeout` | Sandboxie Plus 0.6.7 |
| `UseRpcMgmtSetComTimeout` | Sandboxie Plus 0.7.1 |
| `RpcPortBinding`、`RpcPortBindingIfId` 和 `RpcPortBindingSvc` | Sandboxie Plus 0.7.3 |
| `NoSandboxieRpcSs` | Sandboxie Plus 1.5.0 |
| `RpcPortFilter` | Sandboxie Plus 1.14.2 |

## 相关页面 {#related-pages}

- [系统端点](SystemEndpoints.md)
- [沙盒化服务](SandboxedServices.md)
- [开放 IPC 路径](OpenIpcPath.md)
- [封禁 IPC 路径](ClosedIpcPath.md)
- [Sandboxie Ini](SandboxieIni.md)
