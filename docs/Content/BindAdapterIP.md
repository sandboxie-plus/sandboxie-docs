# Bind Adapter IP

*BindAdapterIP* selects a literal local IPv4 or IPv6 address for supported Winsock operations in matching sandboxed processes. It was introduced in Sandboxie Plus 1.15.10 / Classic 5.70.10.

The address must be assigned to an operational host network interface. If that address disappears, the rule does not automatically migrate to a new DHCP, VPN, or adapter address. Use [*BindAdapter*](BindAdapter.md) instead when Sandboxie should follow the current usable addresses of a named adapter.

## Syntax

```ini
BindAdapterIP=[process,]ip_address
```

Omit `process` to apply the rule to every process in the sandbox, or specify an executable name for a program-specific rule. One IPv4 and one IPv6 address can be selected for a process; each address family is evaluated independently.

Examples:

```ini
BindAdapterIP=192.0.2.25
BindAdapterIP=browser.exe,2001:db8::25
```

The addresses above are reserved for documentation and will not be usable as local bindings. Replace them with addresses actually assigned to active interfaces on the host.

Rules are read from the sandbox's effective configuration, including inherited template settings. The Sandboxie Plus interface manages box-wide IPv4 and IPv6 values; executable-specific rules require manual [Sandboxie Ini](SandboxieIni.md) configuration.

## Behavior and precedence

For matching processes, SbieDll applies the configured address through its user-mode Winsock interception layer. This covers supported connection and datagram paths, but it is not a firewall and does not guarantee coverage for networking code that bypasses those paths.

An applicable *BindAdapter* rule has configuration precedence over *BindAdapterIP*. A literal IP rule is not used as a fallback when the configured named adapter is unavailable.

*StrictBindIP* is enabled by default. On normal intercepted paths it prevents an unavailable address or an unconfigured address family from falling back to an unbound connection. With `StrictBindIP=n`, Windows may select another local address or interface when binding cannot be applied. See [Bind Adapter](BindAdapter.md#strictbindip) for syntax, affected operation classes, and limitations.

Because *BindAdapterIP* identifies a literal address, DHCP renewal, VPN reconnection, or another host network change can make it unavailable. Sandboxie revalidates whether the address remains assigned to an operational interface, but it does not rewrite the rule to use a replacement address. Restart affected sandboxed processes after changing the configured rule. A SandMan or Sandboxie service restart is not normally required.

## Sandboxie Plus interface

Open **Sandbox Options** > **Network Options** > **Other Options**. In the **Bind to Adapter IP** group, select **None (Don't bind to adapter)** and enter an address in the **IPv4:** or **IPv6:** field.

The shared SbieDll runtime is also used by Sandboxie Classic, which can consume compatible manual configuration where the feature is available but does not provide the equivalent modern interface.

## Security limitation

*BindAdapterIP* controls the source address on supported user-mode socket paths. It does not create WFP rules or provide absolute interface confinement. Use separate network policy when direct traffic through another interface must be prevented; see [Windows Filtering Platform](../PlusContent/WFPSupport.md).

## Related settings

- [Bind Adapter](BindAdapter.md) — named-adapter binding, *StrictBindIP*, proxy interaction, and detailed limitations
- [Proxy Support](../PlusContent/ProxySupport.md) — SOCKS5 proxy behavior and binding interaction
