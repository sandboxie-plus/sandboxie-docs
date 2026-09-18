# CPU Affinity Mask

_CpuAffinityMask_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.13.5. It restricts sandboxed processes to selected logical processors by applying a processor affinity mask as each process initializes.

## Usage

```ini
[DefaultBox]
CpuAffinityMask=0x00000003
```

The value must be hexadecimal and begin with `0x` or `0X`. Each set bit allows the corresponding logical processor. In this example, bits 0 and 1 are set, so sandboxed processes may run on logical processors 0 and 1. Logical processors do not necessarily correspond one-to-one with physical CPU cores.

## Current Limitations

The current Sandboxie implementation supports logical processor indices 0 through 31 only. Bits for logical processors 32 and higher cannot be configured with this setting, including on 64-bit Windows.

Sandboxie exposes one affinity mask but no processor-group selector, `GROUP_AFFINITY` setting, or CPU Sets setting. On systems that use multiple Windows processor groups, the mask is therefore subject to Windows' single-group affinity semantics and cannot explicitly select processors in another group.

If Windows rejects the requested affinity mask, Sandboxie currently does not terminate the process because of that failure. If _CpuAffinityMask_ is not configured, Sandboxie does not apply this setting's processor-affinity restriction.

_CpuAffinityMask_ controls where sandboxed processes may execute. To limit their aggregate processor scheduling capacity, see [CPU Rate Limit](CpuRateLimit.md). The two settings can be used together.
