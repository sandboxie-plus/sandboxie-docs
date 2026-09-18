# 网络 DNS 过滤

**网络 DNS 过滤** 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 **v1.14.0 / 5.69.0** 起可用，需要 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)。它允许用户按进程阻止或重定向特定域名的 DNS 查询，从而控制沙盒内的网络流量。

## 语法

```
NetworkDnsFilter=[进程,]域名[:IP 地址]
```

* **进程**（可选）：规则适用的可执行文件名称。省略时，规则适用于所有沙盒化应用程序。
* **域名**：要过滤的完全限定域名（FQDN）。不支持通配符。
* **IP 地址**（可选）：要把域名重定向到的 IP 地址。留空则阻止该域名。

### 示例：

```ini
NetworkDnsFilter=program.exe,example.com:1.1.1.1
```

在此示例中：

* `program.exe` 是规则适用的进程。
* `example.com` 是要过滤的域名。
* `1.1.1.1` 是 `example.com` 的请求将被重定向到的 IP 地址。

## 用法示例

### 1. 重定向对某个域名的所有请求

此规则把任何沙盒化应用程序对 `example.com` 发出的所有 DNS 请求重定向到 `1.1.1.1`：

```ini
[DefaultBox]
NetworkDnsFilter=example.com:1.1.1.1
```

### 2. 只重定向特定应用程序对域名的请求

此规则把对 `example.com` 的 DNS 请求重定向到 `1.1.1.1`，但只针对沙盒化应用程序 `program.exe`：

```ini
[DefaultBox]
NetworkDnsFilter=program.exe,example.com:1.1.1.1
```

### 3. 阻止对域名的所有请求

此规则阻止任何沙盒化应用程序对 `example.com` 的所有 DNS 请求：

```ini
[DefaultBox]
NetworkDnsFilter=example.com
```

### 4. 只阻止特定应用程序对域名的请求

此规则只阻止沙盒化 `program.exe` 对 `example.com` 的 DNS 请求：

```ini
[DefaultBox]
NetworkDnsFilter=program.exe,example.com
```

## 重要说明

* **不支持通配符**：你必须指定完整的域名；不支持通配符（例如 `*.example.com`）。
* **系统 DNS 要求**：为进行正确的 DNS 过滤，你可能需要使用 `Template=BlockDNS` 模板。这确保应用程序通过系统发出 DNS 查询。
* **第三方干扰**：某些第三方应用程序可能干扰或覆盖 DNS 过滤。

* **限制**：在以下情况 DNS 过滤不起作用：

    * 应用程序内配置了安全 DNS（例如 DNS-over-HTTPS）。
    * 应用程序内配置了"使用 SOCKS 4/5 代理 DNS"或类似设置。

* **缺陷**：

    * 主机找不到时重定向失败。[详情参见此问题](https://github.com/sandboxie-plus/Sandboxie/issues/4359)。

## 相关配置

此设置对应 **Sandboxie Plus** 中以下路径的图形界面选项：

**沙盒选项** > **网络选项** > **DNS 过滤器**。
