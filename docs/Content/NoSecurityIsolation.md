# No Security Isolation

_NoSecurityIsolation_ is a sandbox setting available since v1.0.0 / 5.55.0 that transforms Sandboxie from a secure isolation environment into an **Application Compartment** mode, prioritizing compatibility over security.

## Usage

```ini
[DefaultBox]

NoSecurityIsolation=y
```

## Syntax

```ini
NoSecurityIsolation=<y/n>
```

Where:

- `y` enables compartment mode,
- `n` (default) maintains security isolation.

## How It Works

When enabled, the driver sets `bAppCompartment = TRUE`, fundamentally changing Sandboxie's operation by:

- **Bypassing token filtering**: Both primary and impersonation tokens remain unmodified[^1][^2][^3]
- **Excluding Job Objects**: Processes avoid Windows Job Object restrictions[^4]  
- **Relaxing path controls**: Default security-oriented path blocking is disabled[^5]

## Feature Matrix

| Feature | Standard Sandbox | Application Compartment |
|---------|-----------------|-------------------------|
| **File System Virtualization** | ✓ | ✓ |
| **Registry Virtualization** | ✓ | ✓ |
| **Object Namespace Isolation** | ✓ | ✓ |
| **Process Monitoring** | ✓ | ✓ |
| **Token-Based Security** | ✓ | ✗ |
| **Privilege Restrictions** | ✓ | ✗ |
| **Job Object Assignments** | ✓ | ✗ |
| **Security Path Blocking** | ✓ | ✗ |

## Path Control Changes

In Application Compartment mode, three key path behaviors are automatically disabled[^5]:

- **`AlwaysCloseForBoxed`**: Boxed processes can access normally blocked paths[^6].
- **`DontOpenForBoxed`**: Open path rules apply equally to all processes[^7].
- **`ProtectHostImages`**: Host binary protection is relaxed[^8].

## Compatibility & Integration

### Automatic Activation

- **Unsupported Windows builds**: Automatically enabled with warning MSG_1207[^11].
- **Sandboxie Plus box types**: Pre-configured in `Application Compartment` and `Application Compartment with Data Protection`.

### Enhanced Compatibility

- Processes interact freely with the host system.
- Reduced conflicts with privilege-dependent applications.
- Better support for complex software and development tools.

## Security Implications

> [!IMPORTANT]
> Application Compartment mode significantly reduces security isolation:
>
> - Processes run with original security context and privileges.
> - No token-based protection or privilege dropping.
> - Sandbox provides virtualization but not security boundary.

## Related Settings

### Complementary

- **[NoSecurityFiltering](NoSecurityFiltering.md)**: Further disables filtering[^9].
- **OriginalToken**: Auto-enabled in compartment mode.
- **Template Paths**: `TemplateAppCPaths` are applied[^10].

### Job Object Limits (Disabled)

These settings become ineffective due to Job Object exclusion:

- `ProcessNumberLimit`
- `ProcessMemoryLimit`
- `TotalMemoryLimit`

## Use Cases & Troubleshooting

**When to Enable:**

- Software testing and development environments.
- Legacy applications requiring full system privileges.
- Token restriction compatibility issues.
- Virtualization-only scenarios (file/registry separation).

**Common Triggers:**

- Applications failing to start due to token restrictions.
- Administrative privilege requirements.
- Complex software compatibility issues.

## Related

- **Sandboxie Plus**: Sandbox Options > Security Options > Security Isolation
- [Box Types](../PlusContent/box-preset-comparison.md)
- [DropChildProcessToken](DropChildProcessToken.md)

[^1]: **Token Bypass**: `Token_ReplacePrimary` returns `TRUE` when `proc->bAppCompartment` is set, bypassing all token filtering operations.

[^2]: **Primary Tokens**: Left unmodified in `token.c` when Application Compartment mode is active.

[^3]: **Impersonation Tokens**: `Thread_CheckTokenForImpersonation` returns `STATUS_SUCCESS` without restrictions when `proc->bAppCompartment` is enabled.

[^4]: **Job Object Exclusion**: Condition `new_proc->bAppCompartment` in `process.c` excludes processes from Windows Job Objects.

[^5]: **Path Handling**: Three behaviors disabled in `process.c`: `always_close_for_boxed`, `dont_open_for_boxed`, and `protect_host_images`.

[^6]: **AlwaysCloseForBoxed**: `proc->always_close_for_boxed = !proc->bAppCompartment && Conf_Get_Boolean(...)` ensures boxed processes aren't blocked from normally closed paths.

[^7]: **DontOpenForBoxed**: `proc->dont_open_for_boxed = !proc->bAppCompartment && Conf_Get_Boolean(...)` allows equal path rule application.

[^8]: **ProtectHostImages**: `proc->protect_host_images = !proc->bAppCompartment && Conf_Get_Boolean(...)` disables host binary protection.

[^9]: **Security Filtering**: `no_filtering = proc->bAppCompartment && Conf_Get_Boolean(..., L"NoSecurityFiltering", ...)` enables complete filtering bypass.

[^10]: **Template Paths**: `Process_GetPaths(proc, list, L"TemplateAppCPaths", setting_name, FALSE)` applies compartment-specific template paths.

[^11]: **Auto Fallback**: `!Dyndata_Active && !proc->bAppCompartment` triggers automatic compartment mode with `Log_Msg1(MSG_1207, info)`.

