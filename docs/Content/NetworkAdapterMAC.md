# Network Adapter MAC

**NetworkAdapterMAC** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since **v1.15.2 / 5.70.2**. It supplies custom address bytes for the selected NSI/NDIS table path when [Hide Network Adapter MAC](HideNetworkAdapterMAC.md) is enabled. It does not change the physical adapter's address or every API that can report an adapter identity.

## Syntax and examples

```ini
NetworkAdapterMAC=<ordinal>,<MAC address>
```

Use a conventional six-byte hexadecimal MAC address, with or without hyphens:

```ini
[DefaultBox]
HideNetworkAdapterMAC=y
NetworkAdapterMAC=0,12-34-56-78-9A-BC
NetworkAdapterMAC=1,DE-F0-12-34-56-78
```

The parser accepts hexadecimal digits and ignores hyphens. If no applicable valid custom value is available, Sandboxie generates replacement bytes on the intercepted path. The setting does not enforce a locally administered or unicast address bit pattern; choose custom values appropriate for the software being tested.

The parser does not require a six-byte result. `NetworkAdapterMAC=0,AA` replaces only the first byte and preserves the remaining original bytes; `NetworkAdapterMAC=0,--` can succeed without replacing any bytes. Only parser failure triggers the random fallback. Use exactly six bytes for a full conventional MAC replacement.
## What the ordinal means

The ordinal starts at `0` for the first previously uncached original address processed in a sandboxed process, then advances for each new original address. A repeated original address reuses its cached replacement and does not consume a new ordinal. This number is **not** the Windows interface index, `ifIndex`, or a stable adapter ID. Which adapter receives `0` or `1` can vary with query order and between processes; the order shown by `wmic` or `ipconfig` does not establish Sandboxie's ordinal mapping.

The replacement cache is local to the sandboxed process and keyed by the original address. Changing a custom value does not rewrite an existing mapping; restart the affected process to rebuild the map. The Boolean enable decision is read when the relevant `nsi.dll` initialization path runs, so restarting is also the reliable way to apply a changed enable value.

For compatibility testing, distinct valid values such as `AA-00-00-00-00-00` and `AA-11-11-11-11-11` can help observe the order in an application known to use this intercepted path. Such observations apply to that process and query order; they do not turn the ordinal into a permanent adapter index.

## Configuration availability

SandMan has a **Hide Network Adapter MAC Address** checkbox under **Sandbox Options > Advanced Options > Privacy**, but no dedicated editor for custom `NetworkAdapterMAC` entries was identified. Custom values can be configured in the INI. The checkbox shows a direct box value, while an effective enable value can also come from applicable template or global configuration.

## Related settings

- [Hide Network Adapter MAC](HideNetworkAdapterMAC.md) enables this NSI/NDIS address-substitution path.
- [Bind Adapter](BindAdapter.md) controls a separate network binding behavior.
