# Disable Object Filter

_DisableObjectFilter_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.0 / 5.55.0. This setting disables the object filtering mechanism, allowing sandboxed processes to bypass object access restrictions and directly interact with processes, threads, and other system objects outside the sandbox.

## Prerequisites

> [!NOTE]
> Object filtering requires global activation via `EnableObjectFiltering=y` in the [GlobalSettings] section. When globally enabled, individual sandboxes can disable it using `DisableObjectFilter=y`.

## Usage

```ini
[DefaultBox]

DisableObjectFilter=y
```

## Syntax

```ini
DisableObjectFilter=<y/n>
```

Where:
- `y` disables object filtering for this sandbox
- `n` (default) maintains object filtering when globally enabled

## Security Implications

> [!WARNING]
> This setting disables driver-level enforcement of object access restrictions. Malicious software can potentially bypass these protections through various techniques including code injection, API hooking, or direct system calls, making this setting unsuitable for untrusted applications.

## Related Settings

### Master Override

`DisableObjectFilter` is automatically enabled when:

- **[NoSecurityFiltering](NoSecurityFiltering.md)** is set in Application Compartment mode[^1].

### Alternative Granular Controls

- **[DisableFileFilter](DisableFileFilter.md)**: Disables only file system filtering.
- **[DisableKeyFilter](DisableKeyFilter.md)**: Disables only registry filtering.
- **[NoSecurityFiltering](NoSecurityFiltering.md)**: Disables all filtering in Application Compartment mode.

[^1]: Object filter control in `process.c`: The setting `proc->disable_object_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableObjectFilter", 0, FALSE)` allows DisableObjectFilter to completely bypass object filtering either independently or as part of NoSecurityFiltering in Application Compartment mode.
