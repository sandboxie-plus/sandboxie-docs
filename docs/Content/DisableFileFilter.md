# Disable File Filter

_DisableFileFilter_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.9.0 / 5.51.0. This setting disables the file system filtering mechanism, allowing sandboxed processes to bypass file access restrictions and directly interact with the host file system.

## Usage

```ini
[DefaultBox]

DisableFileFilter=y
```

## Syntax

```ini
DisableFileFilter=<y/n>
```

Where:
- `y` disables file system filtering completely
- `n` (default) maintains normal file filtering behavior

## Security Implications

> [!WARNING]
> This setting disables driver-level enforcement of file system access restrictions. Malicious software can potentially bypass these protections through various techniques including code injection, API hooking, or direct system calls, making this setting unsuitable for untrusted applications.

## Related Settings

### Master Override

`DisableFileFilter` is automatically enabled when:
- **[NoSecurityFiltering](NoSecurityFiltering.md)** is set in Application Compartment mode[^1].

### Alternative Granular Controls

- **[DisableKeyFilter](DisableKeyFilter.md)**: Disables only registry filtering.
- **[DisableObjectFilter](DisableObjectFilter.md)**: Disables only object filtering.
- **[NoSecurityFiltering](NoSecurityFiltering.md)**: Disables all filtering in Application Compartment mode.

[^1]: File filter control in `process.c`: The setting `proc->disable_file_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableFileFilter", 0, FALSE)` allows DisableFileFilter to completely bypass file system filtering either independently or as part of NoSecurityFiltering in Application Compartment mode.
