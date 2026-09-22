# Enable Object Filtering

_EnableObjectFiltering_ is a global setting in [Sandboxie Ini](SandboxieIni.md) that controls Sandboxie's kernel Object Manager callback layer for process and thread handles. This layer restricts selected access between sandboxed processes and targets outside the same sandbox. It also supports the separate host-to-sandbox protection used by [Confidential Box](ConfidentialBox.md).

Despite the generic setting name, the current callback registration is specifically for process and thread handles. File, registry, IPC namespace, and other object types are handled by separate Sandboxie mechanisms.

## Current default and configuration

Object filtering is enabled by default. Users do not need to add an explicit `EnableObjectFiltering=y` entry for normal operation.

To disable the global callback layer:

```ini
[GlobalSettings]
EnableObjectFiltering=n
```

The current runtime reads this setting from `GlobalSettings`; placing it only in an individual sandbox section does not control callback registration for that sandbox.

> [!WARNING]
> Disabling the global callback layer removes an important process/thread access-control mechanism for every sandbox. Sandboxie's syscall-specific process/thread checks remain in some paths, but they do not provide identical coverage and should not be treated as an equivalent replacement.

## What the callback filters

The current implementation registers Object Manager callbacks for:

- process handles;
- thread handles;
- new handle creation;
- handle duplication.

For these operations, Sandboxie can leave the requested access unchanged or reduce it according to the process/thread access policy. In the normal denied path, the requested access mask is reduced to zero. The callback itself permits Windows to continue processing the handle operation, so applications should not rely on one particular Win32 or NT error for every restricted request.

Operations that create or duplicate a kernel handle are not modified by this callback. This is a property of the handle operation and does not imply that arbitrary user-mode requests can bypass the filter.

Changes affect future process/thread handle creation and duplication. They do not retroactively reduce rights in an existing handle, add rights to a previously restricted handle, or invalidate an existing handle.

## Process and thread access policy

Process or thread access within the same effective sandbox is normally allowed by this policy. A process in one sandbox targeting a process or thread in another sandbox is treated as outside the sandbox; visibility controls such as `HideOtherBoxes` are separate from handle-access filtering.

For outside targets, Sandboxie restricts process and thread rights that can be used to modify or control the target. Process-memory read access is handled separately from write/control access.

The policy integrates with process-target forms of the IPC resource rules:

```ini
OpenIpcPath=$:target.exe
ReadIpcPath=$:target.exe
ClosedIpcPath=$:target.exe
```

For this use, a matching `ClosedIpcPath` rule is evaluated before `OpenIpcPath`, followed by `ReadIpcPath` where read-only access is applicable. `OpenIpcPath` can permit otherwise restricted access, `ReadIpcPath` applies only to the supported read category, and `$:*` matches every target process. Normal Windows access control still applies after a Sandboxie rule permits a request.

See [Open IPC Path](OpenIpcPath.md), [Read IPC Path](ReadIpcPath.md), and [Closed IPC Path](ClosedIpcPath.md) for the broader resource-rule behavior.

## Callback and syscall-specific filtering

Sandboxie currently has two related process/thread filtering layers:

1. The global Object Manager callback layer filters supported handle creation and duplication independently of the user-mode API or Sandboxie's syscall-specific check that led to the operation.
2. Syscall-specific driver paths retain checks for operations such as opening, enumerating, or duplicating process and thread handles.

The layers share policy code but do not have identical coverage. When the global callbacks are active, overlapping syscall paths normally defer to the callback. If the callbacks are not installed, current syscall-specific paths continue to apply their own checks where implemented.

This distinction means that `EnableObjectFiltering=n` is not equivalent to the per-sandbox [Disable Object Filter](DisableObjectFilter.md) setting.

| Configuration | Scope | Object Manager callbacks | Effect |
| --- | --- | --- | --- |
| Default | Global | Installed | Normal process/thread callback filtering |
| `EnableObjectFiltering=n` | Global | Not installed | Removes the callback layer for every sandbox; syscall-specific checks can remain |
| `DisableObjectFilter=y` | Affected sandboxed processes | Still installed | Relaxes outbound callback filtering for those processes |
| Application Compartment with `NoSecurityFiltering=y` | Affected compartment processes | Still globally installed | Enables the per-process file, registry-key, and object-filter disable states |

## Host-to-sandbox protection

The callback also implements a separate check when an unsandboxed host process requests a handle to a sandboxed process or thread. This path supports settings such as `DenyHostAccess`, `ProtectAdminOnly`, and `NotifyBoxProtected`, as well as the additional process protection of a Confidential Box.

The host-to-sandbox check is separate from a sandboxed process's outbound filter state. Setting `DisableObjectFilter=y` in the target sandbox does not by itself disable this protection while the global callback layer remains active. The path retains operational exceptions for Sandboxie and Windows components required to manage or run the sandbox.

See [Confidential Box](ConfidentialBox.md) for the user-facing host-access policy.

## Application Compartment

[Application Compartment](NoSecurityIsolation.md) mode does not by itself disable the Object Manager callbacks. With `NoSecurityIsolation=y` and normal filtering, compartment processes can still be subject to this process/thread access policy.

When [No Security Filtering](NoSecurityFiltering.md) is also enabled, new compartment processes receive the corresponding per-process file, registry-key, and object-filter disable states. The callbacks remain registered globally, and other sandboxes remain normally filtered.

## SandMan interface

The global control is located at:

**Global Settings > Advanced Config > Sandboxie Config > Activate Kernel Mode Object Filtering**

The checkbox is selected by default. When selected, SandMan normally removes an explicit disabling override and relies on the enabled runtime default. Clearing it writes `EnableObjectFiltering=n`.

Saving this global feature setting can register or unregister the callback layer through driver reconfiguration. A Windows reboot or normal driver restart is not ordinarily required.

If callback registration is required during driver startup but fails, driver initialization fails and Sandboxie logs the registration problem. A failure during later reconfiguration is logged and leaves the callback feature inactive; the exact UI presentation can vary.

## Applying changes

Changing the global setting affects future process/thread handle creation and duplication, including requests made by already-running processes after reconfiguration. It does not alter handles that are already open.

By contrast, `DisableObjectFilter` is stored when each sandboxed process is initialized. Restart affected sandboxed processes after changing that setting.

## Version history

The callback feature was introduced as experimental in Sandboxie Plus 1.0.0 / Classic 5.55.0 and initially required an explicit `EnableObjectFiltering=y` setting. It became enabled by default in Sandboxie Plus 1.0.16 / Classic 5.55.16.

## Related pages

- [Disable Object Filter](DisableObjectFilter.md)
- [No Security Filtering](NoSecurityFiltering.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Confidential Box](ConfidentialBox.md)
- [Open IPC Path](OpenIpcPath.md)
- [Read IPC Path](ReadIpcPath.md)
- [Closed IPC Path](ClosedIpcPath.md)
- [Sandboxie Ini](SandboxieIni.md)
