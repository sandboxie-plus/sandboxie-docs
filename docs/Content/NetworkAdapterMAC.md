# Network Adapter MAC

**NetworkAdapterMAC** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since **v1.15.2 / 5.70.2**. This setting allows assigning custom MAC addresses to specific network adapters within sandboxes.

## Syntax

```ini
NetworkAdapterMAC=<Index>,<MAC Address>
```

* **Index**: Index value of the target network adapter, starts at 0
* **MAC Address**: Custom MAC address in hyphenated format (AA-BB-CC-DD-EE-FF) or plain format (AABBCCDDEEFF)

## Example Usage

```ini
[DefaultBox]
HideNetworkAdapterMAC=y
NetworkAdapterMAC=0,12-34-56-78-9A-BC
NetworkAdapterMAC=1,DE-F0-12-34-56-78
```

## Identifying Network Adapter Index Values

Sandboxie assigns index values only to adapters that have MAC addresses, in the order the system enumerates them. Virtual adapters without MAC addresses are skipped.

To identify which adapters get which Sandboxie index values, get a rough list of adapters with MAC addresses (run in Command Prompt):
```
wmic path win32_networkadapter where "MACAddress is not null" get netconnectionid,name,macaddress
```

Sandboxie assigns index values starting at 0 for the first adapter in this list, then 1, 2, 3, etc. However, Sandboxie's internal enumeration order may not match the command output order.

For accurate mapping, use the testing method:

1. Set unique MAC addresses for each index:
```ini
NetworkAdapterMAC=0,AA-00-00-00-00-00
NetworkAdapterMAC=1,AA-11-11-11-11-11
NetworkAdapterMAC=2,AA-22-22-22-22-22
NetworkAdapterMAC=3,AA-33-33-33-33-33
```
2. Run `ipconfig /all` inside the sandbox to see which adapter has which test MAC

## Important Notes

- Requires `HideNetworkAdapterMAC=y` to be enabled in the same sandbox
- Configuration available through INI only (no user interface option available)
- Invalid MAC address formats result in random MAC generation as fallback
- Each sandbox can assign different MAC addresses to the same physical adapters

## Related Settings

- [Hide Network Adapter MAC](HideNetworkAdapterMAC.md) - Required dependency for MAC address customization
- [Bind Adapter](BindAdapter.md) - Controls which network adapter programs use