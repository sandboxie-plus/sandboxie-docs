# 代理支持

## 概述

对于匹配的过程，Sandboxie 会把受支持的 Winsock TCP 连接路径重定向到选定的 SOCKS5 代理。标准拦截路径包括 `connect`、`WSAConnect` 和 `ConnectEx`，但不应把该列表视为详尽的 API 契约。

该功能为 IPv4 和 IPv6 TCP 目标实现 SOCKS5 `CONNECT` 命令。它支持无认证的 SOCKS5 连接以及用户名/密码认证的 SOCKS5 连接。

它不提供 SOCKS4、SOCKS4a、HTTP `CONNECT`、通用 HTTP 或 HTTPS 代理、SOCKS5 `BIND`、SOCKS5 `UDP ASSOCIATE` 或 UDP 代理。UDP 收发路径不经由 SOCKS5 路由。该功能不是 VPN，也不会透明地覆盖绕过被拦截 Winsock 路径的网络机制。

## SandMan 配置

在 Sandboxie Plus 中，打开**「沙盒选项 → 网络选项 → 互联网代理」**。没有单一的总开关。代理规则可以添加、移除、启用或停用以及重排序。

规则列表包含程序、代理地址、端口、认证方式、登录名、密码和绕过地址等字段。代理地址列目前标注为 **IP**，但它同样接受主机名。

## NetworkUseProxy 语法

通用语法为：

```ini
NetworkUseProxy=[process,]Address=<proxy-address>;Port=<port>[;Auth=Yes|No][;Login=<user>][;Password=<password>|;EncryptedPW=<value>][;Bypass=<address-or-range>,...]
```

例如，该规则适用于沙盒中的所有进程：

```ini
NetworkUseProxy=*,Address=192.0.2.10;Port=1080;Auth=No
```

该规则仅适用于 `browser.exe` 并使用用户名/密码认证：

```ini
NetworkUseProxy=browser.exe,Address=proxy.example;Port=1080;Auth=Yes;Login=user;EncryptedPW=<value>
```

SandMan 通常会创建并序列化这些条目，包括存储的密码值。用户一般不需要手动构造 `EncryptedPW`。

代理地址可以是 IPv4 地址、IPv6 地址或主机名。当主机名标识 SOCKS 服务器时，Sandboxie 会在初始化代理配置时于本地解析它。对代理服务器使用主机名并不能隐藏这次 DNS 查询。

## 应用匹配

规则可以通过 `*` 适用于沙盒中的所有进程，或适用于特定可执行文件。精确的可执行文件匹配优先于全局规则。对于相同的地址族和特异性，使用第一条适用的有效规则。

重复的规则不提供故障转移、轮询选择或负载均衡。当同一沙盒中不同应用需要不同代理时，请使用分开的、针对特定可执行文件的规则。

## IPv4 与 IPv6

代理选择具有地址族感知能力：

- IPv4 目标需要一个适用的 IPv4 代理端点。
- IPv6 目标需要一个适用的 IPv6 代理端点。

IPv4 代理端点不会自动用于 IPv6 目标，反之亦然。如果存在有效的代理配置但没有目标地址族对应的代理端点，Sandboxie 会让连接失败，而不是直接连接到原始目标。

解析到 IPv4 和 IPv6 地址的代理主机名可以为每个地址族分别提供端点。

## 认证与凭据

每条代理规则可以使用无认证的 SOCKS5 或用户名/密码认证的 SOCKS5。SandMan 接受登录名和密码，并处理它们到沙盒配置的序列化。

存储在 Sandboxie 配置中的代理凭据应被当作配置机密妥善保护。该配置不是安全的凭据保险库，可能包含编码/加密的密码表示或明文回退。对于手动编写的条目，不要假定任意分隔符或引号字符会被安全转义，也不要依赖任意凭据字符会被编码为 UTF-8。

## 绕过地址

可选的 `Bypass` 字段接受以逗号分隔的目标 IP 地址和 IP 范围：

```ini
NetworkUseProxy=*,Address=192.0.2.10;Port=1080;Auth=No;Bypass=127.0.0.1,192.168.0.0-192.168.255.255
```

匹配绕过条目的目标会在不使用 SOCKS 代理的情况下连接。本地主机目标也不会被重定向到代理。这种有意为之的直连行为在预期"仅通过代理联网"时很重要。

绕过处理不会覆盖独立的 Sandboxie 网络阻断规则。被单独阻断的目标仍然受该策略约束。

## 失败行为

在 Sandboxie 选定有效代理规则之后，连接代理失败、认证或 SOCKS 协商失败、目标被拒绝，或者所需地址族没有代理端点，都不会让它直接重试原始目标。应用会收到连接失败；具体的 Winsock 错误因失败路径而异。

但是，完全无效的代理配置可能导致代理功能未被启用，连接照常进行。因此不应把代理配置本身视为无条件的失败即关闭（fail-closed）隐私机制。如果必须阻止直连，请在代理规则之外另行施加网络层限制。

## 安全与隐私限制

SOCKS 代理通过 SbieDll 中的用户态拦截实现。它减少了使用受支持拦截 Winsock 路径的匹配应用的直接 TCP 连接，但它不是防火墙，也不会自动创建 Windows 筛选平台（WFP）规则。

绕过这些路径的应用或组件——包括使用其他底层网络机制的代码——可能不会被重定向。代理也不应被视为应用或代理相关 DNS 查询会在远端发生的保证。

要对直接流量有更强的控制，请把代理配置与相应的 [WFP 和网络访问规则](WFPSupport.md)结合使用。网络层过滤器观察到的是到代理端点的实际连接，而不是 SOCKS 会话内承载的最终目标。

## 高级与实验性设置

### NetworkProxyResolveHostnames

`NetworkProxyResolveHostnames` 存在于当前设置元数据中，但标准构建目前未启用其实现，SandMan 也没有暴露该控件。不应依赖它来做远端 DNS 解析或防止 DNS 泄漏。

### UseProxyThreads

`UseProxyThreads=y` 是一个默认停用的实验性兼容模式。它为沙盒进程内每个被代理的连接创建本地 TCP 中继：应用连接到本地中继，由工作线程连接到 SOCKS 代理并中继数据。

该设置面向罕见的兼容性场景，而非性能、隐私或更强的网络强制。当前运行时仅对 Developer 或 Eternal 证书读取它，SandMan 也只在相同条件下暴露其复选框。手动设置它不会为普通证书启用该模式。

中继使用独立的工作连接，不应被视为提供与常规代理路径相同的源地址绑定保证。

## 与绑定和网络策略的交互

源地址或适配器绑定在常规 SOCKS 代理连接之前进行评估。因此不可用的严格绑定可能导致无法连接到代理。详细的绑定行为在[绑定适配器](../Content/BindAdapter.md)和[绑定适配器 IP](../Content/BindAdapterIP.md)下有文档说明。

没有 WFP 强制时，Sandboxie 的用户态目标策略会在代理重定向之前评估原始目标。启用 WFP 强制时，网络栈观察到的是到代理端点的实际连接，而不是 SOCKS 会话中封装的目标。启用代理不会自动添加阻止直连的 WFP 规则。

## 应用配置更改

`NetworkUseProxy` 规则在沙盒进程初始化 Winsock 时被初始化。更改代理规则后，请重启受影响的沙盒进程以确保使用新配置。更改 `UseProxyThreads` 同样需要重启受影响的进程。通常不应需要重启 SandMan 或 Sandboxie 服务。

## Sandboxie Plus 与经典版

代理运行时实现在共享的 SbieDll 代码中。SandMan 提供当前的代理配置界面。在功能可用的地方，Sandboxie Control 经典版可通过共享运行时消费兼容的手工配置设置，但不提供等效的现代代理界面。

项目当前的可用性总览参见[功能对比](../Content/FeatureComparison.md)。

## 版本历史

- **1.14.0 / 5.69.0：** 添加 SOCKS5 代理支持和认证。
- **1.14.5 / 5.69.5：** 添加目标绕过/排除支持。
- **1.15.9 / 5.70.9：** 更改地址族处理，使缺失 IPv4 或 IPv6 代理端点时不再对该地址族回退到直连。
- **1.15.12 / 5.70.12：** 添加代理服务器主机名支持和实验性的中继线程模式。
- **1.18.1 / 5.73.1：** 修复额外的 SOCKS5 凭据编码、长度校验、加密凭据解码和数据传输问题。

## 相关页面

- [WFP 支持](WFPSupport.md)
- [绑定适配器](../Content/BindAdapter.md)
- [绑定适配器 IP](../Content/BindAdapterIP.md)
- [功能对比](../Content/FeatureComparison.md)
