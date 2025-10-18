# Disable Key Filter

_DisableKeyFilter_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.9.0 / 5.51.0. This setting disables the registry filtering mechanism, allowing sandboxed processes to bypass registry access restrictions and directly modify the host system registry.

## Usage

```ini
[DefaultBox]

DisableKeyFilter=y
```

## Syntax

```ini
DisableKeyFilter=<y/n>
```

Where:

- `y` disables registry filtering completely.
- `n` (default) maintains normal registry filtering behavior.

## Security Implications

> [!WARNING]
> This setting disables driver-level enforcement of registry access restrictions. Malicious software can potentially bypass these protections through various techniques including code injection, API hooking, or direct system calls, making this setting unsuitable for untrusted applications.

## Related Settings

### Master Override

`DisableKeyFilter` is automatically enabled when:
- **[NoSecurityFiltering](NoSecurityFiltering.md)** is set in Application Compartment mode[^1].

### Alternative Granular Controls

- **[DisableFileFilter](DisableFileFilter.md)**: Disables only file system filtering.
- **[DisableObjectFilter](DisableObjectFilter.md)**: Disables only object filtering.
- **[NoSecurityFiltering](NoSecurityFiltering.md)**: Disables all filtering in Application Compartment mode.

[^1]: Registry filter control in `process.c`: The setting `proc->disable_key_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableKeyFilter", 0, FALSE)` allows DisableKeyFilter to completely bypass registry filtering either independently or as part of NoSecurityFiltering in Application Compartment mode.
