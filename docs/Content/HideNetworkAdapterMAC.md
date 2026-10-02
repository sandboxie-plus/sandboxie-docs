# Hide Network Adapter MAC Address

HideNetworkAdapterMAC is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```ini
[DefaultBox]
HideNetworkAdapterMAC=y
```

When enabled, Sandboxie replaces MAC-address data in matching entries returned through its intercepted `NsiAllocateAndGetTable` path. The replacement applies to a selected NSI/NDIS table after a successful original query, not to every method of obtaining an adapter address. Other network APIs, Registry queries, and WMI classes may use different paths.

For each original address first encountered in a sandboxed process, Sandboxie uses a value from [Network Adapter MAC](NetworkAdapterMAC.md) or generates replacement bytes. Repeated encounters with that original address reuse the process-local cached value. Changing a custom value does not rewrite an existing cache entry.

The runtime fallback is disabled when no effective value is configured. The Boolean lookup can be qualified by process image and can include applicable template or global configuration. The enable value is read when the relevant `nsi.dll` initialization path runs; restarting affected sandboxed processes is the reliable way to rebuild the hook state and address cache.

In **Sandbox Options > Advanced Options > Privacy**, **Hide Network Adapter MAC Address** controls the direct box setting. An inherited effective value can differ from the checkbox state.
