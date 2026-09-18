# BlockLocalLoop

**BlockLocalLoop** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.17.4. It restricts matched IP-loopback traffic through Sandboxie's covered networking paths and is disabled by default.

```ini
[DefaultBox]
BlockLocalLoop=y
```

This is a narrow loopback restriction, not complete local-network or host isolation. It does not block every way a sandboxed process could communicate with a service running on the same computer.

## Address scope

The user-mode Winsock enforcement recognizes:

- the complete IPv4 `127.0.0.0/8` loopback range;
- the IPv6 loopback address `::1`;
- IPv4-mapped IPv6 loopback addresses containing an address from `127.0.0.0/8`.

`BlockLocalLoop` does not determine whether a non-loopback address belongs to the same computer. The host's LAN or Wi-Fi address, private addresses such as `10.x.x.x` and `192.168.x.x`, link-local addresses, assigned non-loopback IPv6 addresses, and virtual-adapter addresses are outside its normal address scope. Broader access should be controlled with normal `NetworkAccess` rules.

The setting acts on resolved IP addresses rather than DNS names. For example, `localhost` or a custom hostname resolving to `127.0.0.0/8` or `::1` is subject to the restriction. A name resolving to a non-loopback address is not blocked merely because it identifies the local computer, and DNS resolution itself is not prevented.

The restriction is address-based rather than port-specific. It has no documented per-port exceptions or built-in exemptions for particular browsers, RPC endpoints, or system services.

## Communication behavior

When enabled, Sandboxie's user-mode Winsock path rejects standard outbound communication to matched loopback addresses. Covered paths include normal TCP connection attempts, connected UDP, UDP sends, and selected UDP receive paths. For example, calls through `connect`, `WSAConnect`, `sendto`, or `WSASendTo` are subject to the restriction.

Standard Winsock operations blocked by the user-mode path normally fail immediately with a connection-refused error. Other networking paths, including operations blocked by Windows Filtering Platform (WFP), should not be assumed to return the same exact error.

`BlockLocalLoop` does not itself prevent a sandboxed application from binding a local socket or listening on a loopback address. It restricts communication through covered loopback paths rather than preventing creation of local listeners.

There is no same-sandbox exemption. For outbound loopback traffic initiated by a sandboxed process with the setting enabled, the restriction does not distinguish whether the peer is:

- an unsandboxed host process;
- another process in the same sandbox;
- a process in another sandbox.

Consequently, client/server pairs within the same sandbox may also be affected.

The documented scope is IP networking over IPv4 and IPv6, including TCP and UDP through the covered Winsock paths. It does not apply to AF_UNIX sockets, named pipes, or other non-IP IPC mechanisms. Comprehensive raw-socket or ICMP filtering should not be assumed from the user-mode path alone.

## Network rules and WFP support

`BlockLocalLoop` is evaluated independently from normal `NetworkAccess` rules. An allow rule does not override a successful `BlockLocalLoop` match. Broader deny rules may make the setting redundant for traffic they already block.

The default enforcement layer is the user-mode Winsock path inside sandboxed processes. If WFP support is enabled globally:

```ini
[GlobalSettings]
NetworkEnableWFP=y
```

Sandboxie's driver also participates through Windows Filtering Platform. WFP can extend enforcement beyond the intercepted Winsock exports and can apply kernel authorization to additional IP traffic classes. The user-mode fallback primarily restricts traffic initiated by the sandboxed process; with WFP enabled, authorization can also apply to inbound connection and receive paths.

### Implementation notes and limitations

The reliable documented behavior is based primarily on the standard Winsock enforcement path. Kernel WFP support provides additional coverage when enabled, but current implementation details differ between address families and networking paths. Applications that bypass normal Winsock paths should not be assumed to receive identical behavior, and complete bidirectional IPv4 loopback blocking through WFP is not guaranteed.

Binding or listening itself is not prevented. Changing the global `NetworkEnableWFP` option is separate from changing `BlockLocalLoop`; see [WFP Support](../PlusContent/WFPSupport.md) for its activation requirements.

## Compatibility and purpose

The setting can reduce access by sandboxed code to host-local services that listen only on loopback, including unauthenticated localhost services, development or administration endpoints, and local helper or control services.

Software may be affected if it actually uses loopback communication, including:

- browsers connecting to a local development server;
- Electron or WebView applications using a local helper;
- OAuth or login callbacks using `127.0.0.1` or `::1`;
- IDEs, test tools, and development servers;
- local databases, HTTP or SOCKS proxies, and DNS resolvers;
- game launchers or helper processes communicating over TCP or UDP loopback.

Not every application in these categories uses loopback. Non-loopback addresses assigned to the host remain outside this setting's scope, and named pipes or other local IPC mechanisms are unrelated. Use network-access rules when broader restrictions are required.

## Scope and applying changes

`BlockLocalLoop` is a normal box setting and can be inherited through normal template or global configuration resolution. There is no documented per-program syntax.

The user-mode value is read when networking initializes in the sandboxed process. Changing the option does not reliably update every process that is already running, so restarting affected sandboxed applications is the reliable way to apply the change. A service or driver restart is not required merely for newly started processes.

## User interface and notifications

There is currently no dedicated **BlockLocalLoop** checkbox in normal Sandbox Options. Configure it through:

**Sandbox Options** > **Edit ini Section** > **Edit ini**

There is also no dedicated `BlockLocalLoop` notification or user-facing SBIE message for each blocked connection. Applications normally report their own networking failure.

## Version history

*BlockLocalLoop* was introduced in Sandboxie Plus 1.17.4. It remains disabled by default, and the current Sandbox Options interface does not provide a dedicated checkbox for it.

## Related configuration

- [Sandboxie Ini](SandboxieIni.md)
- [WFP Support](../PlusContent/WFPSupport.md)
- `NetworkAccess` for broader address, port, protocol, or program-based network rules
- `NetworkEnableWFP` for optional kernel-level network enforcement
