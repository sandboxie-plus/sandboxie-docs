# 绑定适配器

**BindAdapter**(绑定适配器) 和 **BindAdapterIP**(绑定适配器IP) 是[Sandboxie Ini](SandboxieIni.md) 自 **v1.15.12 / 5.70.12** 和 **v1.15.10 / 5.70.10** 版本以来可用的沙箱设置。这些设置控制沙箱内的程序用于网络通信的网络适配器或 IP 地址。

## 语法

### BindAdapter
```ini
BindAdapter=[<程序名>,]<适配器名>
```

### BindAdapterIP
```ini
BindAdapterIP=[<程序名>,]<IP 地址>
```

* **程序名**: （可选）要应用绑定的程序名称。如果省略，则适用于沙箱中的所有程序。
* **适配器名**: 网络适配器的友好名称（例如，“Ethernet”、“Wi-Fi”、“VPN Connection”）
* **IP 地址**: 必须绑定到一个主机网络适配器的特定 IPv4 或 IPv6 地址

## 目的

这些设置将沙箱内网络通信限制为特定的网络资源：

- **BindAdapter** 强制程序按名称使用特定的网络适配器
- **BindAdapterIP** 强制程序在所有网络操作中使用特定的 IP 地址

## 示例用法

### 基本适配器绑定

将所有沙箱程序绑定到 Wi-Fi 适配器：

```ini
[DefaultBox]
BindAdapter=Wi-Fi
```

### IP 地址绑定

强制程序使用特定的 IPv4 地址：

```ini
[DefaultBox]
BindAdapterIP=192.168.100.123
```

强制程序使用特定的 IPv6 地址：

```ini
[DefaultBox]
BindAdapterIP=fe80::8570:c50:a571:bf22
```

### 单进程配置

仅对特定程序应用绑定：

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

您可以配置多个单进程绑定：

```ini
[DefaultBox]
BindAdapterIP=program1.exe,192.168.1.10
BindAdapterIP=program2.exe,192.168.1.20
BindAdapter=program3.exe,Ethernet 2
```

## 重要说明

> **配置优先级:** BindAdapter 对 BindAdapterIP 具有绝对优先权。如果对同一进程配置了两者，则使用 BindAdapter，BindAdapterIP 条目将被完全忽略。
>
> **优先级系统:** 多个条目遵循“最具体者获胜”的政策：
> - 精确程序名称匹配（例如，`BindAdapter=chrome.exe,Ethernet`）具有最高优先级
> - 否定匹配（例如，`BindAdapter=!firefox.exe,Wi-Fi`）具有中等优先级  
> - 全局匹配（例如，`BindAdapter=Ethernet`）具有最低优先级
> - 仅使用最具体的匹配条目；其他条目被忽略
>
> **单一 IP 限制:** 每个地址族只能激活一个 IP 地址。IPv4 和 IPv6 条目独立处理，每个条目遵循“最具体者获胜”的政策。相同地址族的多个条目相互竞争（当特异性相等时，先找到的胜出）。您不能同时绑定多个 IPv4 或多个 IPv6 地址，但可以同时激活一个 IPv4 和一个 IPv6 地址。
>
> **失败行为:** BindAdapter 和 BindAdapterIP 对不可用资源的处理方式不同：
> - **BindAdapter**: 如果未找到适配器名称，则回退到本地主机（127.0.0.1 和 ::1），且不报告错误
> - **BindAdapterIP**: 如果 IP 地址未绑定到任何主机 NIC，则所有网络连接将静默失败
>
> **用户界面限制:** 每个进程的绑定配置只能通过手动编辑 Sandboxie.ini 文件进行设置。用户界面仅支持全局（所有程序）绑定配置。

## 用户界面

在 **Sandboxie Plus** 中，您可以通过以下方式配置这些设置：

**沙箱选项** > **网络选项** > **其他选项**

该界面提供：
- 一个下拉菜单，用于从可用网络适配器中选择 **BindAdapter**
- IPv4 和 IPv6 地址的文本字段，用于 **BindAdapterIP**

![Bind Adapter Configuration](../Media/BindAdapter.png)

## 相关设置

- [网络 DNS 过滤器](NetworkDnsFilter.md) - 过滤沙箱程序的 DNS 请求