# Disable Object Filter

_DisableObjectFilter_ is an advanced sandbox setting in [Sandboxie Ini](SandboxieIni.md). For affected sandboxed processes, it relaxes the kernel Object Manager callback policy that normally restricts process and thread handle access to targets outside the same sandbox.

> [!WARNING]
> This setting can expose process and thread handle rights that Sandboxie normally restricts, increasing a sandboxed program's ability to inspect, modify, or control processes outside its sandbox. Sandboxie classifies the option as unsafe. It does not disable all Sandboxie isolation, but it should be used only when a specific compatibility requirement justifies the reduced protection.

## Configuration

```ini
[DefaultBox]
DisableObjectFilter=y
```

The syntax is:

```ini
DisableObjectFilter=y|n
```

- `y` enables the per-process filter exception.
- `n`, the default, keeps the normal callback policy.

The setting is resolved from the effective sandbox configuration and stored when each sandboxed process is initialized. Normal template and global fallback can therefore contribute to the effective value, but the current consumer does not provide executable-qualified matching for this setting.

## What it disables

When a sandboxed caller passes through the kernel callback's process/thread policy with `DisableObjectFilter=y`, Sandboxie preserves the requested access instead of applying its normal outbound restriction for that caller.

The affected callback covers the creation and duplication of process and thread handles. Despite the generic setting name, it is not a switch for every type of Windows object.

## What it does not disable

`DisableObjectFilter=y` does not:

- unregister the global Object Manager callbacks;
- disable callback filtering for other sandboxed processes whose effective configuration does not enable it;
- disable file or registry filtering;
- disable every IPC namespace or resource-access mechanism;
- disable all Sandboxie process/thread access checks;
- make the process unsandboxed.

The current driver retains syscall-specific process/thread checks. When the global callbacks are unavailable, some of those paths apply the shared access policy directly and do not uniformly consult the per-process `DisableObjectFilter` state. Consequently, this setting must not be treated as a universal switch for every current process/thread access restriction. This is an implementation boundary rather than a guarantee that the fallback will always have exactly the same structure.

## Global callback setting

Object Manager callback filtering is globally enabled by default. Users do not need to add `EnableObjectFiltering=y` for normal current behavior.

The global and per-sandbox controls are not equivalent:

| Setting | Scope | Object Manager callbacks | Result |
| --- | --- | --- | --- |
| `EnableObjectFiltering=n` | Global | Unregistered | Removes the callback layer for every sandbox; syscall-specific checks can remain |
| `DisableObjectFilter=y` | Affected sandboxed processes | Still installed | Relaxes outbound callback filtering for those processes |

See [Enable Object Filtering](EnableObjectFiltering.md) for the global default, callback scope, and syscall-filter distinction.

## Host-to-sandbox protection

The callback has a separate path for an unsandboxed host process requesting a handle to a sandboxed process or thread. This path supports [Confidential Box](ConfidentialBox.md) and settings including `DenyHostAccess` and `ProtectAdminOnly`.

Host-to-sandbox protection is evaluated separately and before the outbound `DisableObjectFilter` exception. Enabling `DisableObjectFilter` in the target sandbox therefore does not by itself allow host processes unrestricted access to that sandbox's processes while the global callback layer remains active.

## Application Compartment and NoSecurityFiltering

[Application Compartment](NoSecurityIsolation.md) mode does not automatically set `DisableObjectFilter=y` in the configuration.

For new Application Compartment processes, [No Security Filtering](NoSecurityFiltering.md) enables the corresponding file, registry-key, and object-filter disable states at runtime. This includes the same per-process object-filter state controlled directly by `DisableObjectFilter`, but it still does not unregister the global callbacks or change other sandboxes.

## IPC process rules

With normal object filtering, process-target forms such as the following can permit or deny specific access without disabling the filter for the whole sandbox:

```ini
OpenIpcPath=$:target.exe
ReadIpcPath=$:target.exe
ClosedIpcPath=$:target.exe
```

See [Open IPC Path](OpenIpcPath.md), [Read IPC Path](ReadIpcPath.md), and [Closed IPC Path](ClosedIpcPath.md). These rules can provide a narrower compatibility exception than `DisableObjectFilter=y`.

## SandMan configuration

SandMan does not provide a dedicated sandbox checkbox for `DisableObjectFilter`; it is an advanced INI/configuration option. SandMan's unsafe-configuration detection recognizes the setting, although another box-state warning can take precedence in the displayed status.

## Applying changes

The setting is stored in each sandboxed process's driver state during process initialization. Configuration reload does not rewrite that state for processes that are already running.

Restart affected sandboxed processes after changing `DisableObjectFilter`. Restarting the sandboxed process tree is appropriate when testing the change consistently. A Windows reboot is not normally required.

## Version history

The settings metadata lists `DisableObjectFilter` as added in Sandboxie Plus 0.9.2. The corresponding process-state assignment was not active in that old tag; the active per-process opt-out and Object Manager callback feature were present and publicly documented with Sandboxie Plus 1.0.0 / Classic 5.55.0.

The callback layer became enabled by default in Sandboxie Plus 1.0.16 / Classic 5.55.16, so the historical requirement to add `EnableObjectFiltering=y` no longer applies.

## Related pages

- [Enable Object Filtering](EnableObjectFiltering.md)
- [No Security Filtering](NoSecurityFiltering.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Confidential Box](ConfidentialBox.md)
- [Disable File Filter](DisableFileFilter.md)
- [Disable Key Filter](DisableKeyFilter.md)
- [Sandboxie Ini](SandboxieIni.md)
