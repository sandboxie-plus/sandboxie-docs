# 绑定适配器

**绑定适配器** 和 **绑定适配器 IP** 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置，分别自 **v1.15.12 / 5.70.12** 和 **v1.15.10 / 5.70.10** 起可用。这些设置控制沙盒化程序使用哪个网络适配器或 IP 地址进行网络通信。

## 语法

### BindAdapter
```ini
BindAdapter=[<程序>,]<适配器名称>
```

### BindAdapterIP
```ini
BindAdapterIP=[<程序>,]<IP 地址>
```

* **程序**：（可选）要应用绑定的特定程序可执行文件名称。省略时，适用于沙盒中的所有程序。
* **适配器名称**：网络适配器的友好名称（例如"以太网"、"Wi-Fi"、"VPN 连接"）
* **IP 地址**：必须绑定到宿主机某个网络适配器上的特定 IPv4 或 IPv6 地址

## 目的

这些设置把沙盒化的网络通信限制到特定的网络资源：

- **绑定适配器** 按名称强制程序使用特定网络适配器
- **绑定适配器 IP** 强制程序对所有网络操作使用特定 IP 地址

## 用法示例

### 基本适配器绑定

把所有沙盒化程序绑定到 Wi-Fi 适配器：

```ini
[DefaultBox]
BindAdapter=Wi-Fi
```

### IP 地址绑定

强制程序使用特定 IPv4 地址：

```ini
[DefaultBox]
BindAdapterIP=192.168.100.123
```

强制程序使用特定 IPv6 地址：

```ini
[DefaultBox]
BindAdapterIP=fe80::8570:c50:a571:bf22
```

### 按进程配置

只对特定程序应用绑定：

```ini
[DefaultBox]
BindAdapterIP=firefox.exe,192.168.1.100
BindAdapterIP=chrome.exe,10.0.0.50
```

```ini
[DefaultBox]  
BindAdapter=torrent.exe,VPN Connection
```

### 多个配置

你可以配置多个按进程的绑定：

```ini
[DefaultBox]
BindAdapterIP=program1.exe,192.168.1.10
BindAdapterIP=program2.exe,192.168.1.20
BindAdapter=program3.exe,Ethernet 2
```

## 重要说明

> **配置优先级：** 绑定适配器绝对优先于绑定适配器 IP。如果为同一进程配置了两者，使用绑定适配器，绑定适配器 IP 条目被完全忽略。
>
> **优先级系统：** 多个条目遵循"最具体者胜出"策略：
> 
> - 精确程序名称匹配（例如 `BindAdapter=chrome.exe,Ethernet`）优先级最高
> - 否定匹配（例如 `BindAdapter=!firefox.exe,Wi-Fi`）优先级中等  
> - 全局匹配（例如 `BindAdapter=Ethernet`）优先级最低
> - 只使用最具体的匹配条目；其他条目被忽略
>
> **单一 IP 限制：** 每个地址族只有一个 IP 处于活动状态。IPv4 和 IPv6 条目独立处理，各自遵循"最具体者胜出"策略。同一地址族的多个条目相互竞争（特异性相同时先找到者胜出）。你不能同时绑定到多个 IPv4 或多个 IPv6 地址，但可以同时让一个 IPv4 和一个 IPv6 地址处于活动状态。
>
> **失败行为：** 绑定适配器和绑定适配器 IP 处理不可用资源的方式不同：
> 
> - **绑定适配器**：如果找不到适配器名称，回退到 localhost（127.0.0.1 和 ::1），不报告错误
> - **绑定适配器 IP**：如果 IP 地址未绑定到任何宿主网卡，所有网络连接都会静默失败
>
> **界面限制：** 按进程的绑定配置只能通过手动编辑 Sandboxie.ini 文件来设置。用户界面只支持全局（所有程序）绑定配置。

## 用户界面

在 **Sandboxie Plus** 中，你可以通过以下路径配置这些设置：

**沙盒选项** > **网络选项** > **其他选项**

该界面提供：

- 一个下拉菜单，用于为 **绑定适配器** 选择可用网络适配器
- 用于 **绑定适配器 IP** 的 IPv4 和 IPv6 地址文本字段

![绑定适配器配置](../Media/BindAdapter.png)

## 相关设置

- [网络 DNS 过滤器](NetworkDnsFilter.md) - 过滤沙盒化程序的 DNS 请求
