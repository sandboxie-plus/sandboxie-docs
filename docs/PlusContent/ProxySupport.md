# Proxy Support

## Overview

For matching processes, Sandboxie redirects supported Winsock TCP connection paths through a selected SOCKS5 proxy. Standard intercepted paths include `connect`, `WSAConnect`, and `ConnectEx`, although this list should not be treated as an exhaustive API contract.

The feature implements the SOCKS5 `CONNECT` command for IPv4 and IPv6 TCP destinations. It supports SOCKS5 connections without authentication and with username/password authentication.

It does not provide SOCKS4, SOCKS4a, HTTP `CONNECT`, generic HTTP or HTTPS proxying, SOCKS5 `BIND`, SOCKS5 `UDP ASSOCIATE`, or UDP proxying. UDP send and receive paths are not routed through SOCKS5. The feature is not a VPN and does not transparently cover networking mechanisms that bypass the intercepted Winsock paths.

## SandMan configuration

In Sandboxie Plus, open **Sandbox Options > Network Options > Internet Proxy**. There is no single master checkbox. Proxy rules can be added, removed, enabled or disabled, and reordered.

The rule list contains fields for the program, proxy address, port, authentication mode, login, password, and bypass addresses. The proxy-address column is currently labelled **IP**, but it also accepts a hostname.

## NetworkUseProxy syntax

The general syntax is:

```ini
NetworkUseProxy=[process,]Address=<proxy-address>;Port=<port>[;Auth=Yes|No][;Login=<user>][;Password=<password>|;EncryptedPW=<value>][;Bypass=<address-or-range>,...]
```

For example, this rule applies to every process in the sandbox:

```ini
NetworkUseProxy=*,Address=192.0.2.10;Port=1080;Auth=No
```

This rule applies only to `browser.exe` and uses username/password authentication:

```ini
NetworkUseProxy=browser.exe,Address=proxy.example;Port=1080;Auth=Yes;Login=user;EncryptedPW=<value>
```

SandMan normally creates and serializes these entries, including the stored password value. Users generally do not need to construct `EncryptedPW` manually.

The proxy address may be an IPv4 address, an IPv6 address, or a hostname. When a hostname identifies the SOCKS server, Sandboxie resolves it locally while initializing the proxy configuration. Using a hostname for the proxy server does not hide that DNS lookup.

## Application matching

A rule may apply to all processes in a sandbox by using `*`, or to a specific executable. An exact executable match takes priority over a global rule. For the same address family and specificity, the first applicable valid rule is used.

Repeated rules do not provide failover, round-robin selection, or load balancing. Use separate executable-specific rules when different applications in the same sandbox need different proxies.

## IPv4 and IPv6

Proxy selection is address-family aware:

- An IPv4 destination requires an applicable IPv4 proxy endpoint.
- An IPv6 destination requires an applicable IPv6 proxy endpoint.

An IPv4 proxy endpoint is not automatically used for IPv6 destinations, or vice versa. If a valid proxy configuration exists but no proxy endpoint is available for the destination's address family, Sandboxie fails the connection instead of connecting directly to the original destination.

A proxy hostname that resolves to both IPv4 and IPv6 addresses can provide an endpoint for each family.

## Authentication and credentials

Each proxy rule can use SOCKS5 without authentication or SOCKS5 username/password authentication. SandMan accepts the login and password and handles their serialization into the sandbox configuration.

Proxy credentials stored in Sandboxie configuration should be treated as configuration secrets and protected accordingly. The configuration is not a secure credential vault and may contain either an encoded/encrypted password representation or a plaintext fallback. For manually written entries, do not assume that arbitrary delimiter or quote characters are safely escaped, and do not rely on arbitrary credential characters being encoded as UTF-8.

## Bypass addresses

The optional `Bypass` field accepts destination IP addresses and IP ranges separated by commas:

```ini
NetworkUseProxy=*,Address=192.0.2.10;Port=1080;Auth=No;Bypass=127.0.0.1,192.168.0.0-192.168.255.255
```

Destinations matching a bypass entry are connected without using the SOCKS proxy. Localhost destinations are also not redirected through the proxy. This intentional direct-routing behavior matters when proxy-only connectivity is expected.

Bypass handling does not override independent Sandboxie network-blocking rules. A separately blocked destination remains subject to that policy.

## Failure behavior

After Sandboxie selects a valid proxy rule, failure to connect to the proxy, authentication or SOCKS negotiation failure, destination rejection, or absence of a proxy endpoint for the required address family does not cause it to retry the original destination directly. The application receives a connection failure; the exact Winsock error can vary by failure path.

However, an entirely invalid proxy configuration may result in proxying not being enabled, allowing connections to continue normally. Proxy configuration alone must therefore not be treated as an unconditional fail-closed privacy mechanism. If direct connections must be prevented, apply separate network-layer restrictions in addition to the proxy rules.

## Security and privacy limitations

SOCKS proxying is implemented through user-mode interception in SbieDll. It reduces direct TCP connections for matching applications that use the supported intercepted Winsock paths, but it is not a firewall and does not automatically create Windows Filtering Platform (WFP) rules.

Applications or components that bypass those paths, including code using other low-level networking mechanisms, may not be redirected. Proxying should also not be treated as a guarantee that application or proxy-related DNS lookups occur remotely.

For stronger control over direct traffic, combine proxy configuration with appropriate [WFP and network-access rules](WFPSupport.md). A network-layer filter observes the actual connection to the proxy endpoint, not the final destination carried inside the SOCKS session.

## Advanced and experimental settings

### NetworkProxyResolveHostnames

`NetworkProxyResolveHostnames` exists in the current setting metadata, but the standard build does not currently enable its implementation and SandMan does not expose the control. It should not be relied on for remote DNS resolution or preventing DNS leaks.

### UseProxyThreads

`UseProxyThreads=y` is an experimental compatibility mode that is disabled by default. It creates a local TCP relay for each proxied connection inside the sandboxed process: the application connects to the local relay, and a worker thread connects to the SOCKS proxy and relays the data.

This setting is intended for rare compatibility cases, not performance, privacy, or stronger network enforcement. The current runtime reads it only for Developer or Eternal certificates, and SandMan exposes its checkbox only under the same condition. Setting it manually does not enable the mode for ordinary certificates.

The relay uses a separate worker connection and should not be treated as providing the same source-address binding guarantees as the normal proxy path.

## Interaction with binding and network policy

Source-address or adapter binding is evaluated before the normal SOCKS proxy connection. An unavailable strict binding can therefore prevent connection to the proxy. Detailed binding behavior is documented under [Bind Adapter](../Content/BindAdapter.md) and [Bind Adapter IP](../Content/BindAdapterIP.md).

Without WFP enforcement, Sandboxie's user-mode destination policy evaluates the original destination before proxy redirection. With WFP enforcement, the network stack observes the actual connection to the proxy endpoint rather than the destination encapsulated in the SOCKS session. Enabling a proxy does not automatically add WFP rules that block direct connections.

## Applying configuration changes

`NetworkUseProxy` rules are initialized when a sandboxed process initializes Winsock. After changing proxy rules, restart affected sandboxed processes to ensure that the new configuration is used. Changes to `UseProxyThreads` also require restarting the affected process. A SandMan or Sandboxie service restart should not normally be necessary.

## Sandboxie Plus and Classic

The proxy runtime is implemented in shared SbieDll code. SandMan provides the current proxy configuration interface. Sandboxie Control Classic can consume compatible manually configured settings through the shared runtime where the feature is available, but it does not provide the equivalent modern proxy interface.

See [Feature Comparison](../Content/FeatureComparison.md) for the project's current feature-availability overview.

## Version history

- **1.14.0 / 5.69.0:** Added SOCKS5 proxy support and authentication.
- **1.14.5 / 5.69.5:** Added destination bypass/exclusion support.
- **1.15.9 / 5.70.9:** Changed address-family handling so a missing IPv4 or IPv6 proxy endpoint does not fall back to a direct connection for that family.
- **1.15.12 / 5.70.12:** Added proxy-server hostname support and the experimental relay-thread mode.
- **1.18.1 / 5.73.1:** Fixed additional SOCKS5 credential encoding, length validation, encrypted credential decoding, and data-transfer issues.

## Related pages

- [WFP Support](WFPSupport.md)
- [Bind Adapter](../Content/BindAdapter.md)
- [Bind Adapter IP](../Content/BindAdapterIP.md)
- [Feature Comparison](../Content/FeatureComparison.md)
