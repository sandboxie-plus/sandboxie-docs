# 网络 DNS 过滤

**NetworkDnsFilter** 是 [沙盘配置文件（Sandboxie.ini）](SandboxieIni.md) 中的一个沙盘配置项，自 **v1.14.0 / 5.69.0** 版本起提供，且需要[支持者证书](https://sandboxie-plus.com/supporter-certificate/)才能启用。
它允许用户按进程粒度对特定域名的 DNS 查询进行阻止或重定向，从而控制沙盘内的网络流量。

## 语法

```
NetworkDnsFilter=[进程,]域名[:IP地址]
```

* **进程**（可选）：要应用规则的可执行程序名。如果省略，则该规则对所有沙盘应用生效。
* **域名**：要过滤的完整域名（FQDN），不支持通配符。
* **IP地址**（可选）：将该域名重定向到的 IP 地址。如果留空，则表示阻止该域名的访问。

### 示例：

```ini
NetworkDnsFilter=program.exe,example.com:1.1.1.1
```

此示例中：

* `program.exe` 是要应用该规则的进程。
* `example.com` 是要过滤的域名。
* `1.1.1.1` 是将 `example.com` 请求重定向到的 IP 地址。

## 使用示例

### 1. 重定向所有对某域名的请求

此规则会将所有沙盘应用对 `example.com` 的 DNS 请求重定向到 `1.1.1.1`：

```ini
[DefaultBox]
NetworkDnsFilter=example.com:1.1.1.1
```

### 2. 仅对特定应用重定向域名请求

此规则仅对沙盘中的 program.exe 应用，将对 `example.com` 的请求重定向到 `1.1.1.1`：

```ini
[DefaultBox]
NetworkDnsFilter=program.exe,example.com:1.1.1.1
```

### 3. 阻止所有对某域名的请求

此规则会阻止所有沙盘应用对 `example.com` 的 DNS 请求（即不进行域名解析）：

```ini
[DefaultBox]
NetworkDnsFilter=example.com
```

### 4. 仅对特定应用阻止域名请求

此规则仅阻止沙盘中的 `program.exe` 对 `example.com` 进行 DNS 请求：

```ini
[DefaultBox]
NetworkDnsFilter=program.exe,example.com
```

## 注意事项

* **不支持通配符**：必须指定完整域名，不支持诸如 `*.example.com` 的通配符写法。
* **依赖系统 DNS**：为确保 DNS 过滤有效，建议同时使用 `Template=BlockDNS` 模板。这样可以确保应用程序通过系统发起 DNS 查询。
* **第三方软件干扰**：某些第三方应用可能会干扰或绕过 DNS 过滤机制。

* **已知限制**：

    * 当应用程序内部配置了安全 DNS（如 DNS-over-HTTPS）时，DNS 过滤将无效。
    * 当应用程序启用了 “通过 SOCKS 4/5 代理 DNS 查询” 等类似设置时，DNS 过滤也将无效。

* **已知 Bug**：

    * 当主机名未找到时，重定向会失败。详细信息请参阅 [此问题](https://github.com/sandboxie-plus/Sandboxie/issues/4359)。

## 相关配置界面

此配置项对应于 **Sandboxie Plus** 图形界面中的以下路径：

**沙盘选项** > **网络选项** > **DNS 过滤器**。
