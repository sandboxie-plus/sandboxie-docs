# DNS Filter

Sandboxie Plus can block or redirect selected hostname lookups from sandboxed programs. Rules can target particular applications and use domain patterns, while redirection rules can return configured IPv4 or IPv6 addresses.

The filter operates on supported Windows Winsock service lookups intercepted by Sandboxie. It is not a firewall and does not cover applications that resolve names through their own networking implementation, send names to a proxy for remote resolution, or connect directly to known IP addresses.

Configure rules in **Sandbox Options > Network Options > DNS Filter**. For syntax, address-family behavior, process and wildcard matching, limitations, and the separate **Block DNS, UDP port 53** option, see [Network DNS Filtering](../Content/NetworkDnsFilter.md).

DNS activity logging is a separate diagnostic feature. See [`DnsTrace`](../Content/SandboxieTrace.md) for its scope and privacy considerations.
