# Hook and Loader Compatibility

These advanced settings change selected Sandboxie hook or Windows loader initialization paths. They are intended for targeted compatibility troubleshooting, not as general switches to disable sandboxing. Skipping an interception path can also change the mediation or compatibility behavior that depends on it.

## Hooking layers

Sandboxie does not use one universal hook. The driver maintains information about selected native system calls; an injected low-level path can prepare syscall stubs in a newly started process. SbieDll separately installs Nt and Win32 API hooks, and its loader callbacks initialize hooks and workarounds for particular loaded modules. A setting that skips one of these paths does not necessarily skip the others.

## NoSysCallHooks

```ini
[DefaultBox]
NoSysCallHooks=y
```

`NoSysCallHooks` is a box-wide Boolean option, disabled by default. When enabled, Sandboxie skips the low-level syscall-stub initialization for newly started processes in that box. It also skips selected SbieDll secure hooks for `NtOpenProcess`, `NtOpenThread`, and `NtDuplicateObject`, and the related WoW64 syscall fix-up. Application Compartment mode independently skips the low-level path and those selected secure hooks.

This does **not** disable every Sandboxie hook or the rest of process injection. Other SbieDll hooks and independent driver controls still have their own initialization paths. Use this option only for a diagnosed compatibility problem; it is not a way to turn off all API interception while keeping otherwise unchanged sandbox behavior.

## DisableWinNtHook

`DisableWinNtHook` is a repeatable pattern setting for the driver's NT syscall map. The map loader reads entries from `[SysCallPresets]`, so the setting is global rather than selected separately for each box or executable. The underlying configuration lookup has fallback behavior for `[GlobalSettings]`, but these sources should not be described as two freely merged lists. Shipped presets already provide entries. Write the syscall entry name without its `Nt` or `Zw` prefix. A current preset illustrates the syntax:

```ini
[SysCallPresets]
DisableWinNtHook=MapViewOfSection
```

The driver scans `Zw` exports, removes the `Zw` prefix, and marks matching map entries disabled. Entries so marked are omitted when Sandboxie copies syscall information for its low-level hook path. The parser accepts multiple entries and its pattern matcher supports `*` and `?`; matching uses the export-name spelling, including case. A name or pattern matching no known entry has no effect. This is not an image-aware rule: program selectors, process groups, and negated selectors are not parsed here.

This setting does not generically disable Win32 API hooks, nor does it guarantee that every higher-level API using a named syscall becomes unhooked. `DisableWin32Hook` is a separate Win32k map control discussed in [Win32k Hooks](Win32kHooks.md).

### How the two syscall settings differ

`NoSysCallHooks=y` skips a broader low-level syscall-stub initialization path for processes in a box. `DisableWinNtHook` instead selects named entries in a driver-wide NT syscall map used by that path. The first is a box-level Boolean; the second is a repeatable map pattern. Neither setting disables all Sandboxie hooks.

## NoParallelLoading

```ini
[DefaultBox]
NoParallelLoading=y
```

`NoParallelLoading` is a box-wide Boolean option, disabled by default. During SbieDll loader initialization in a newly started sandboxed process, it sets that process's `LoaderThreads` parameter to `0`. This targets Windows loader parallel-loading behavior for debugging loader compatibility issues. It does not disable application multithreading or serialize all process activity.

## DllSkipHook

`DllSkipHook` is a repeatable DLL-name setting in the effective box configuration. For example, the current Proxifier compatibility template contains:

```ini
DllSkipHook=ws2_32.dll
```

At SbieDll loader initialization, each value is compared case-insensitively with the exact DLL basenames in Sandboxie's known module-initializer table. A match skips that module's Sandboxie-specific initialization callback when the DLL is loaded. It does **not** prevent Windows from loading the DLL. Other, separate tracing or hook paths are not universally disabled by this setting.

An unknown name, a full path, or a wildcard pattern does not match that table and has no effect. There is no executable-selector, process-group, or negation parser for these values. Unlike [Skip Hook](SkipHook.md) and [Function Skip Hook](FuncSkipHook.md), this option selects known module callbacks rather than individual hook identifiers or exported functions.

`NoParallelLoading` and `DllSkipHook` address different problems: the former changes loader concurrency for a process, while the latter skips a selected Sandboxie callback for a known module. Neither is a general DLL-blocking or sandbox-disable mechanism.

## Templates and presets

Sandboxie's current `[SysCallPresets]` contains several `DisableWinNtHook` entries maintained for its syscall map. The Proxifier template provides the `DllSkipHook=ws2_32.dll` compatibility example above. These are current maintained presets, not a recommendation to copy every entry or a promise that template contents will remain unchanged. `DllSkipHook` can also come from applicable enabled templates in the effective sandbox configuration.

## Applying changes

`NoSysCallHooks`, `NoParallelLoading`, and `DllSkipHook` are read during process or SbieDll initialization. Start new sandboxed processes after changing them; existing processes do not rebuild their installed hooks or loader state. The driver can refresh `DisableWinNtHook` map flags when its configuration is reloaded, but already initialized process stubs are not retroactively rebuilt. Reload the configuration and restart affected sandboxed processes when testing a map change. A driver restart or Windows reboot is not normally required for that update.

The current SandMan options source has no dedicated controls for these four settings. Configure them in [Sandboxie Ini](SandboxieIni.md) or through an applicable preset or template.

## Version history

The changelog records `NoSysCallHooks` in Sandboxie Plus 0.4.5 / Classic 5.44.1, `DllSkipHook` in Plus 0.9.1 / Classic 5.51.1, `DisableWinNtHook` in Plus 1.3.0 / Classic 5.58.0, and `NoParallelLoading` in Plus 1.7.0 / Classic 5.62.0. It also records support for changing `DisableWinNtHook` without a driver reload in Plus 1.15.9 / Classic 5.70.9.

## Related settings

- [System Call Settings](SyscallSettings.md) explains syscall mediation, approvals, and lockdown separately from hook-map exclusions.
- [Win32k Hooks](Win32kHooks.md) covers the distinct Win32k hook path.
- [Advanced Loader and SxS Compatibility](AdvancedLoaderCompatibility.md) covers other loader and process-start workarounds.
