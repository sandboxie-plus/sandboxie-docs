# 网络访问

`NetworkAccess` 为 Sandboxie 的网络规则引擎定义程序、地址、端口与协议规则。用户态的 Winsock 路径与（启用时的）[Windows 筛选平台 (WFP) 路径](../PlusContent/WFPSupport.md) 使用同一套规则解析与比较逻辑，但两者的强制执行覆盖范围不同。

## 语法与示例

```ini
NetworkAccess=[process,]Allow|Block[;Port=...][;Address=...][;Protocol=...]
```

例如：

```ini
[DefaultBox]
NetworkAccess=*,Block;Port=80,443
NetworkAccess=chrome.exe,Allow;Port=443;Address=192.0.2.10;Protocol=TCP
NetworkAccess=<Browsers>,Allow;Port=80,443;Protocol=TCP
```

可选的进程选择器可以标识一个可执行文件、一个匹配的可执行文件模式，或一个[进程组](ProcessGroup.md)。Sandboxie 常规的[程序名匹配](ProgramNamePrefix.md)也支持取反选择器。在下文描述的规则比较中，不带进程选择器的规则比带显式 `*` 选择器的匹配规则适用范围更广。

若没有任何 `NetworkAccess` 规则匹配，规则引擎会放行该流量。要构建默认拒绝的规则集，先添加一条适用面很广的阻止规则，再在需要处添加更窄的放行规则：

```ini
NetworkAccess=*,Block
NetworkAccess=chrome.exe,Allow;Port=443
```

该规则引擎默认值与 [WFP 支持](../PlusContent/WFPSupport.md#allownetworkaccess)中描述的 `AllowNetworkAccess` 门是分开的。

## 匹配规则是如何选出的

对于候选程序与端点，Sandboxie 严格按下列顺序比较前四个条件。后续候选若在第一个不同的条件上更优，就取代当前的胜出者：

| 顺序 | 条件 | 更具体或更优先的匹配 |
| --- | --- | --- |
| 1 | 进程选择器 | 匹配的正向选择器，其次是匹配的取反选择器，再次是显式 `*`，最后是无选择器 |
| 2 | 组合端点 | 同时约束地址与端口的规则，优先于只约束其中一项或都不约束的规则 |
| 3 | 端口 | 精确端口，其次是范围，最后是不约束 |
| 4 | 地址 | 精确地址，其次是范围，最后是不约束 |

匹配的正向选择器包括可执行文件名称、通配符映像模式或 `ProcessGroup`；最上面这一类并不限于精确的可执行文件名。下面前三个示例是正向选择器，其余各行分别展示取反选择器、显式 `*` 与无选择器：

```ini
NetworkAccess=chrome.exe,Allow;Port=443
NetworkAccess=chr*.exe,Allow;Port=443
NetworkAccess=<Browsers>,Allow;Port=443
NetworkAccess=!chrome.exe,Block
NetworkAccess=*,Block
NetworkAccess=Block
```

进程匹配最先比较，因此更强的进程选择器可以压过地址或端口约束更精确的规则。在进程匹配等价时，同时指定 `Address` 与 `Port` 的规则优先于只指定其中一项的规则。完成该组合比较之后，才先检查端口的具体性，再检查地址的具体性。

前四个条件打平之后，当前比较器对动作与协议的处理并不对称。`Block` 候选会立即取代 `Allow` 胜出者。否则比较会继续进行到协议具体性，其中已指定的协议优先于 `Any`。因此当两条在其他方面打平的规则分别偏向 `Block` 与更具体的协议时，规则顺序可能影响结果。

若比较器找不到取代当前胜出者的理由，既有的胜出者保持不动。兼容的规则也可能在内部被合并。`NetworkAccess` 不是“最后一条规则获胜”的引擎。

## 地址、端口与协议

`Address` 接受单个 IPv4 或 IPv6 地址、地址范围，以及以逗号分隔的多项。例如：

```ini
Address=192.0.2.10
Address=192.0.2.10-192.0.2.50
Address=2001:db8::10
```

`Port` 接受单个数字端口、范围，以及以逗号分隔的集合：

```ini
Port=80,443,49152-65535
```

当前规则语言识别 `Protocol=Any`、`TCP`、`UDP` 与 `ICMP`；未指定协议的规则默认为 `Any`。它没有定义 `ICMPv6` 关键字。支持的地址语法使用地址与范围，不支持 CIDR 记法；`http` 这类端口名不是数字端口值。

## 强制执行路径

在没有 WFP 强制执行时，SbieDll 通过被拦截的用户态 Winsock 路径应用 `NetworkAccess`，其中包括 `connect`、`WSAConnect`、`sendto` 与 `WSASendTo` 等重要出站 TCP 与 UDP 操作。相关的接收钩子也参与该实现。这主要是出站规则的强制执行，并不覆盖每一条 Windows 网络路径。绕过或移除用户态钩子的代码可以绕过这一层。

设 `NetworkEnableWFP=y` 后，Sandboxie 使用内核 WFP 回调，在出站连接与入站接收/接受授权层，为受跟踪的沙盒进程评估共享规则。全局开关、进程映射与生命周期参见 [WFP 支持](../PlusContent/WFPSupport.md)。

尽管解析器与 SandMan 编辑器都识别 `ICMP`，用户态钩子聚焦于 Winsock TCP 连接与 UDP 收发。ICMP 覆盖范围取决于强制执行路径与流量类型；无论是本设置还是 WFP，都不应被理解为对每条原始或 ICMPv6 路径的保证。

`AllowNetworkAccess=n` 是一个独立的映像感知访问门。在 WFP 下，它可以在常规 `NetworkAccess` 规则求值之前选择整体阻断互联网访问。`NetworkAccess=...,Allow` 规则不一定能覆盖该门。[提示互联网访问](PromptForInternetAccess.md)产生的运行时批准可以影响某个进程实例的该门；它们不是持久的 `NetworkAccess` 规则。[阻止本地回环](BlockLocalLoop.md)在 WFP 下同样单独求值。

## SandMan 与版本背景

规则编辑器位于 **沙盒选项 > 网络选项 > 网络防火墙**。其字段对应程序、动作、协议、IP/地址与端口。**测试规则** 控件为输入的程序、地址、端口与协议提供部分预览；它们不会发起网络连接。该预览不处理通配符或进程组选择器，会跳过模板规则，并可能把已禁用的规则计入。因此其高亮结果可能不同于运行时实际应用的规则。

`NetworkAccess` 在 Sandboxie Plus 0.9.0 引入。规则覆盖与更新行为取决于强制执行路径，因此更改策略后请重启受影响的沙盒应用程序，以确保进程本地状态被一致地重建。WFP 规则也可以通过 Sandboxie 的配置更新路径，为已在跟踪的既有进程刷新。

## 相关页面

- [WFP 支持](../PlusContent/WFPSupport.md)
- [阻止本地回环](BlockLocalLoop.md)
- [提示互联网访问](PromptForInternetAccess.md)
- [进程组](ProcessGroup.md)
