# 阻止本地回环 {#blocklocalloop}

**BlockLocalLoop** 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.17.4 起可用。它会限制 Sandboxie 所覆盖的网络路径上的匹配 IP 回环流量，默认禁用。

```ini
[DefaultBox]
BlockLocalLoop=y
```

这是一种范围很窄的回环限制，并不等于完整的本地网络隔离或宿主隔离。它不会阻断沙盒化进程与同一台计算机上运行的服务通信的所有途径。

## 地址范围 {#address-scope}

用户态的 Winsock 强制执行能识别：

- 完整的 IPv4 `127.0.0.0/8` 回环地址段；
- IPv6 回环地址 `::1`；
- 含 `127.0.0.0/8` 中某个地址的、IPv4 映射的 IPv6 回环地址。

`BlockLocalLoop` 并不判断某个非回环地址是否属于同一台计算机。宿主的局域网或 Wi-Fi 地址、`10.x.x.x` 与 `192.168.x.x` 一类的专用地址、链路本地地址、已分配的非回环 IPv6 地址以及虚拟适配器地址，都在其常规地址范围之外。更广泛的访问应通过常规的 `NetworkAccess` 规则控制。

该设置作用于解析后的 IP 地址，而不是 DNS 名称。例如，`localhost` 或某个解析到 `127.0.0.0/8` 或 `::1` 的自定义主机名都受该限制约束。解析到非回环地址的名称，不会仅仅因为它指向本机就被阻止，DNS 解析本身也不被阻止。

该限制基于地址而非端口。它没有已记录在案的按端口例外，也没有针对特定浏览器、RPC 端点或系统服务的内置豁免。

## 通信行为 {#communication-behavior}

启用后，Sandboxie 的用户态 Winsock 路径会拒绝向匹配的回环地址发起的标准出站通信。覆盖的路径包括常规的 TCP 连接尝试、已连接的 UDP、UDP 发送以及选定的 UDP 接收路径。例如，通过 `connect`、`WSAConnect`、`sendto` 或 `WSASendTo` 发出的调用都受该限制约束。

被用户态路径阻断的标准 Winsock 操作通常立即以连接被拒绝的错误失败。对于其他网络路径，包括被 Windows 过滤平台（WFP）阻断的操作，不应假定会返回完全相同的错误。

`BlockLocalLoop` 本身并不阻止沙盒化应用程序绑定本地套接字或在回环地址上监听。它限制的是通过所覆盖回环路径进行的通信，而不是阻止创建本地监听器。

不存在同一沙盒内的豁免。对于启用该设置的沙盒化进程发起的出站回环流量，该限制不区分对端是：

- 非沙盒化的宿主进程；
- 同一沙盒中的另一个进程；
- 另一个沙盒中的进程。

因此，同一沙盒内的客户端/服务器组合也可能受到影响。

已记录的作用范围是 IPv4 与 IPv6 上的 IP 网络通信，包括经由所覆盖 Winsock 路径的 TCP 与 UDP。它不适用于 AF_UNIX 套接字、命名管道或其他非 IP 的 IPC 机制。不应仅凭用户态路径就假定具备完整的原始套接字或 ICMP 过滤。

## 网络规则与 WFP 支持 {#network-rules-and-wfp-support}

`BlockLocalLoop` 与常规的 `NetworkAccess` 规则独立求值。放行规则不能覆盖一次成功的 `BlockLocalLoop` 匹配。对于更宽泛的拒绝规则已经阻断的流量，该设置可能是多余的。

默认的强制执行层是沙盒化进程内部的用户态 Winsock 路径。如果全局启用了 WFP 支持：

```ini
[GlobalSettings]
NetworkEnableWFP=y
```

Sandboxie 的驱动程序也会通过 Windows 过滤平台参与执行。WFP 可以把强制执行扩展到被拦截的 Winsock 导出之外，并可对额外的 IP 流量类别施加内核级授权。用户态回退路径主要限制沙盒化进程发起的流量；启用 WFP 后，授权还可以作用于入站连接与接收路径。

### 实现说明与限制 {#implementation-notes-and-limitations}

可靠且有记录的行为主要基于标准的 Winsock 强制执行路径。内核 WFP 支持在启用后提供额外覆盖，但当前的实现细节在不同地址族与不同网络路径之间存在差异。不应假定绕过常规 Winsock 路径的应用程序会得到完全一致的行为，也不保证能通过 WFP 实现完整的双向 IPv4 回环阻断。

绑定或监听本身不被阻止。更改全局的 `NetworkEnableWFP` 选项与更改 `BlockLocalLoop` 是两件独立的事；其启用条件参见 [WFP（Windows 过滤平台）支持](../PlusContent/WFPSupport.md)。

## 兼容性与用途 {#compatibility-and-purpose}

该设置可以减少沙盒内代码对仅在回环上监听的宿主本地服务的访问，包括无需身份验证的 localhost 服务、开发或管理端点，以及本地辅助服务或控制服务。

如果软件确实使用回环通信，就可能受到影响，例如：

- 连接到本地开发服务器的浏览器；
- 使用本地辅助程序的 Electron 或 WebView 应用程序；
- 使用 `127.0.0.1` 或 `::1` 的 OAuth 或登录回调；
- IDE、测试工具与开发服务器；
- 本地数据库、HTTP 或 SOCKS 代理以及 DNS 解析器；
- 通过 TCP 或 UDP 回环通信的游戏启动器或辅助进程。

这些类别并非每个应用程序都使用回环。分配给宿主的非回环地址仍在该设置范围之外，命名管道或其他本地 IPC 机制也不相关。需要更广泛的限制时，请使用网络访问规则。

## 作用范围与应用更改 {#scope-and-applying-changes}

`BlockLocalLoop` 是一项常规的沙盒设置，可以通过常规的模板或全局配置解析继承。它没有已记录在案的按程序语法。

用户态取值在沙盒化进程初始化网络时读取。更改该选项并不能可靠地更新每一个已在运行的进程，因此重启受影响的沙盒化应用程序才是可靠的应用方式。仅就新启动的进程而言，不需要重启服务或驱动程序。

## 用户界面与通知 {#user-interface-and-notifications}

常规的沙盒选项目前没有专门的 **BlockLocalLoop** 复选框。请通过以下位置配置：

**沙盒选项** > **配置文本** > **编辑配置**

对于每一次被阻断的连接，也没有专门的 `BlockLocalLoop` 通知或面向用户的 SBIE 消息。应用程序通常会自行报告其网络失败。

## 版本历史 {#version-history}

*BlockLocalLoop* 在 Sandboxie Plus 1.17.4 中引入。它仍然默认禁用，当前的沙盒选项界面也没有为它提供专用复选框。

## 相关配置 {#related-configuration}

- [Sandboxie Ini](SandboxieIni.md)
- [WFP（Windows 过滤平台）支持](../PlusContent/WFPSupport.md)
- `NetworkAccess`，用于更广泛的地址、端口、协议或基于程序的网络规则
- `NetworkEnableWFP`，用于可选的内核级网络强制执行
