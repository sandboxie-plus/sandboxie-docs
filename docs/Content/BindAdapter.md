# Bind Adapter

**BindAdapter** and **BindAdapterIP** are sandbox settings in [Sandboxie Ini](SandboxieIni.md) available since **v1.15.12 / 5.70.12** and **v1.15.10 / 5.70.10** respectively. These settings control which network adapter or IP address sandboxed programs use for network communications.

## Syntax

### BindAdapter
```ini
BindAdapter=[<Program>,]<AdapterName>
```

### BindAdapterIP
```ini
BindAdapterIP=[<Program>,]<IP Address>
```

* **Program**: (Optional) Specific program executable name to apply binding to. If omitted, applies to all programs in the sandbox.
* **AdapterName**: The friendly name of a network adapter (e.g., "Ethernet", "Wi-Fi", "VPN Connection")
* **IP Address**: A specific IPv4 or IPv6 address that must be bound to one of the host's network adapters

## Purpose

These settings restrict sandboxed network communications to specific network resources:

- **BindAdapter** forces programs to use a particular network adapter by name
- **BindAdapterIP** forces programs to use a specific IP address for all network operations

## Example Usage

### Basic Adapter Binding

Bind all sandboxed programs to the Wi-Fi adapter:

```ini
[DefaultBox]
BindAdapter=Wi-Fi
```

### IP Address Binding

Force programs to use a specific IPv4 address:

```ini
[DefaultBox]
BindAdapterIP=192.168.100.123
```

Force programs to use a specific IPv6 address:

```ini
[DefaultBox]
BindAdapterIP=fe80::8570:c50:a571:bf22
```

### Per-Process Configuration

Apply binding to specific programs only:

```ini
[DefaultBox]
BindAdapterIP=firefox.exe,192.168.1.100
BindAdapterIP=chrome.exe,10.0.0.50
```

```ini
[DefaultBox]  
BindAdapter=torrent.exe,VPN Connection
```

### Multiple Configurations

You can configure multiple per-process bindings:

```ini
[DefaultBox]
BindAdapterIP=program1.exe,192.168.1.10
BindAdapterIP=program2.exe,192.168.1.20
BindAdapter=program3.exe,Ethernet 2
```

## Important Notes

> **Configuration Precedence:** BindAdapter takes absolute precedence over BindAdapterIP. If both are configured for the same process, BindAdapter is used and BindAdapterIP entries are completely ignored.
>
> **Priority System:** Multiple entries follow a "most specific wins" policy:
> - Exact program name match (e.g., `BindAdapter=chrome.exe,Ethernet`) has highest priority
> - Negation match (e.g., `BindAdapter=!firefox.exe,Wi-Fi`) has medium priority  
> - Global match (e.g., `BindAdapter=Ethernet`) has lowest priority
> - Only the most specific matching entry is used; others are ignored
>
> **Single IP Limitation:** Only one IP address per family is active. IPv4 and IPv6 entries are processed independently, each following the "most specific wins" policy. Multiple entries of the same address family compete with each other (first-found wins when specificity is equal). You cannot bind to multiple IPv4 or multiple IPv6 addresses simultaneously, but you can have one IPv4 and one IPv6 address active at the same time.
>
> **Failure Behavior:** BindAdapter and BindAdapterIP handle unavailable resources differently:
> - **BindAdapter**: If the adapter name is not found, falls back to localhost (127.0.0.1 and ::1) with no error reported
> - **BindAdapterIP**: If the IP address is not bound to any host NIC, all network connections will fail silently
>
> **UI Limitation:** Per-process binding configurations can only be set by manually editing the Sandboxie.ini file. The user interface only supports global (all programs) binding configurations.

## User Interface

In **Sandboxie Plus**, you can configure these settings through:

**Sandbox Options** > **Network Options** > **Other Options**

The interface provides:
- A dropdown menu to select from available network adapters for **BindAdapter**
- Text fields for IPv4 and IPv6 addresses for **BindAdapterIP**

![Bind Adapter Configuration](../Media/BindAdapter.png)

## Related Settings

- [Network Dns Filter](NetworkDnsFilter.md) - Filter DNS requests from sandboxed programs