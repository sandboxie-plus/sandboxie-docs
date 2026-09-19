# System Call Settings

## Overview

Sandboxie mediates selected native system calls as part of its isolation and compatibility architecture. This mediation can involve both a Sandboxie handler for the call and a temporary choice of security token while the call is processed. These are separate decisions.

Sandboxie does not intercept every Windows system call, and system-call mediation is not its only isolation layer. File and registry filtering, kernel-object filtering, virtualization, network policy, and other controls operate separately. For background on Sandboxie's token architecture, see [Token and Syscall Internals](TokenMagic.md).

## SysCallLockDown

The box-wide setting is:

```ini
SysCallLockDown=y
```

`SysCallLockDown=y` places the process's intercepted system calls in lockdown mode. `UseSecurityMode=y`, which enables Security Hardened mode, also causes the process to use this lockdown behavior.

Without lockdown, Sandboxie's mediation path can temporarily use the original or full token when required to process an intercepted call. With lockdown enabled:

- an approved intercepted call may use that original/full-token execution path;
- an unapproved intercepted call does not receive that path and continues under the restricted sandbox token;
- the call can still execute, but it may fail if the restricted token lacks a required right.

`SysCallLockDown` is therefore not a simple list that blocks every unapproved system call. It controls the token-selection decision within the intercepted paths that Sandboxie mediates.

Security Hardened mode and direct use of `SysCallLockDown` require a valid [Supporter Certificate](../PlusContent/supporter-certificate.md).

## Approved system calls

Approval marks an intercepted system-call entry as eligible for original/full-token execution while lockdown is active. It does not disable Sandboxie interception, bypass an associated Sandboxie handler, or execute the call outside the sandbox. File, registry, object, and other independent filtering also remain in effect.

Approval entries belong in `GlobalSettings` or a template rather than an individual sandbox section. Keep custom approvals narrow: every approved entry restores the original/full-token path for that call under lockdown. The built-in templates contain maintained approvals for supported scenarios and should not be copied wholesale into a custom configuration.

### NT system calls

`ApproveWinNtSysCall` adds names to the NT system-call approval map. Names use the driver entry name without the `Nt` or `Zw` prefix. For example, current built-in templates contain entries in this form:

```ini
[GlobalSettings]
ApproveWinNtSysCall=OpenFile
ApproveWinNtSysCall=CreateFile
```

These examples demonstrate syntax only. They do not constitute a general recommended approval list.

### Win32k system calls

`ApproveWin32SysCall` is the corresponding approval mechanism for intercepted Win32k system calls. A template entry can, for example, use a matching pattern:

```ini
[GlobalSettings]
ApproveWin32SysCall=GdiDdDDI*
```

Win32k approval has an effect only when Sandboxie's Win32k system-call hooking path is available and installed for the process. Approval still controls the lockdown token decision; it does not bypass any Sandboxie handler installed for the matching call.

## Configuration reload

Current Sandboxie versions reload the NT and Win32k approval maps when the driver configuration is reconfigured. After editing approval entries, use **Options > Reload configuration** so the new maps are applied. A driver restart is not normally required solely for these approval-list changes.

This updates the approval maps. It does not rebuild tokens already assigned to running processes or change which system-call hooks were installed when a process started. Restart affected sandboxed processes when testing broader system-call configuration changes.

## OpenAllSysCalls

The box-wide debug setting is:

```ini
OpenAllSysCalls=y
```

Despite its name, `OpenAllSysCalls` does not simply “allow every system call” or disable the complete sandbox. `OpenAllSysCalls=y` causes NT system-call entries with an installed Sandboxie first-stage handler to bypass that handler and invoke the underlying system-call path directly. The same internal gate is present in the Win32k dispatch path, but the current Win32k table does not install first-stage handlers in that path.

The lockdown token decision is independent and occurs before this handler decision. Consequently, `OpenAllSysCalls=y` does not disable `SysCallLockDown` and does not make every call run with the original token. If the process is locked down and an intercepted call is not approved, the restricted-token behavior still applies; enabling `OpenAllSysCalls` does not grant that call original/full-token execution.

> [!WARNING]
> The project explicitly classifies `OpenAllSysCalls` as an insecure debug option. It weakens system-call-level mediation by bypassing installed Sandboxie first-stage handlers that may provide security, virtualization, filtering, or compatibility behavior for hooked entries. It is intended for debugging or highly specific compatibility investigation, not as a normal sandbox configuration.

The setting does not automatically disable unrelated layers such as file and registry filtering, kernel-object callbacks, network policy, or other independent Sandboxie controls.

## Security considerations

- Approve only the specific calls required by a confirmed compatibility problem.
- Treat built-in template approvals as maintained implementation policy, not as a general list to copy.
- Approval changes the temporary token context; it does not remove the normal handler for the call.
- `OpenAllSysCalls` removes more mediation than an approval and should not be used as a routine compatibility switch.
- A working application is not evidence that a broad approval or debug bypass preserves the intended isolation boundary.

## Version history

| Setting or change | Introduced |
| --- | --- |
| Security Hardened mode, `SysCallLockDown`, `ApproveWinNtSysCall`, and `ApproveWin32SysCall` | Sandboxie Plus 1.3.0 / Classic 5.58.0 |
| `OpenAllSysCalls` insecure debug option | Sandboxie Plus 1.15.9 / Classic 5.70.9 |

## Related pages

- [Security Hardened Mode](../PlusContent/security-mode.md)
- [Token and Syscall Internals](TokenMagic.md)
- [Sandboxie Ini](SandboxieIni.md)
