# Network DNS Filtering

**NetworkDnsFilter** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since **v1.14.0 / 5.69.0** and requires a [supporter certificate](https://sandboxie-plus.com/supporter-certificate/). It allows users to block or redirect DNS queries for specific domains on a per-process basis, offering control over network traffic within sandboxes.

## Syntax

```
NetworkDnsFilter=[process,]domain[:ip_address]
```

* **process** (optional): The name of the executable to which the rule applies. If omitted, the rule applies to all sandboxed applications.
* **domain**: The fully qualified domain name (FQDN) to filter. Wildcards are not supported.
* **ip\_address** (optional): The IP address to redirect the domain to. If left empty, the domain is blocked.

### Example:

```ini
NetworkDnsFilter=program.exe,example.com:1.1.1.1
```

In this example:

* `program.exe` is the process to which the rule applies.
* `example.com` is the domain to filter.
* `1.1.1.1` is the IP address to which `example.com` requests will be redirected.

## Usage Examples

### 1. Redirect all requests made to a domain

This rule redirects all DNS requests made to `example.com` to `1.1.1.1` for any sandboxed application:

```ini
[DefaultBox]
NetworkDnsFilter=example.com:1.1.1.1
```

### 2. Redirect requests to a domain only for a specific application

This rule redirects DNS requests to `example.com` to `1.1.1.1`, but only for the sandboxed application `program.exe`:

```ini
[DefaultBox]
NetworkDnsFilter=program.exe,example.com:1.1.1.1
```

### 3. Block all requests to a domain

This rule blocks all DNS requests to `example.com` for any sandboxed application:

```ini
[DefaultBox]
NetworkDnsFilter=example.com
```

### 4. Block requests to a domain only for a specific application

This rule blocks DNS requests to `example.com` only for the sandboxed `program.exe`:

```ini
[DefaultBox]
NetworkDnsFilter=program.exe,example.com
```

## Important Notes

* **Wildcard support is not available**: You must specify complete domain names; wildcards (e.g., `*.example.com`) are not supported.
* **System DNS requirement**: For proper DNS filtering, you may need to use the `Template=BlockDNS` template. This ensures that applications make DNS queries through the system.
* **Third-party interference**: Some third-party applications may interfere with or override DNS filtering.

* **Limitations**: DNS filtering will not work when

    * A secure DNS (e.g., DNS-over-HTTPS) is configured within an application.
    * The "Proxy DNS when using SOCKS 4/5" or a similar setting is configured within an application.

* **Bugs**:

    * Redirection fails when host not found. [Refer to this issue](https://github.com/sandboxie-plus/Sandboxie/issues/4359) for details.

## Related Configuration

This setting corresponds to the GUI option in **Sandboxie Plus** under the following path:

**Sandbox Options** > **Network Options** > **DNS Filter**.
