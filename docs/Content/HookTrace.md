# HookTrace

_HookTrace_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.5 / 5.70.5. It enables detailed logging of all function hooking activities performed by the  [SbieDll](SBIEDLLAPI.md) component.

## Usage

```
[DefaultBox]

HookTrace=y
```

## Overview

Function hooking is a core mechanism used by Sandboxie to intercept and redirect system calls from sandboxed processes. The `HookTrace` setting provides detailed visibility into this process, logging every hook attempt, success, failure, and related metadata. This is primarily useful for troubleshooting sandboxing issues and understanding how Sandboxie instruments applications.

## How It Works

When `HookTrace` is enabled:

1. **Hook Detection**: SbieDll logs all attempts to hook functions in loaded modules[^1].
2. **Status Tracking**: Each hook operation is classified with status flags indicating success, failure reasons, or special conditions[^2].
3. **Module Resolution**: The system identifies the source module for each hooked function using address lookup[^3].
4. **Monitor Output**: Hook information is sent to the monitoring system using the MONITOR_HOOK flag[^4].

## Output Format

Hook trace entries appear in the format:

```
Hooking: module!function
FAILED Hooking: module!function
Skipped Hooking: module!function  
Hooking (trace): module!function
```

Additional status information may be appended:

- `(Chrome Hook Hooked)` - Chrome-specific hook was successfully applied[^5].
- `(Chrome Hook Unresolved)` - Chrome-specific hook failed to resolve[^6].
- `FFS Target not found, hooked x86 code instead` - ARM64 fallback was used[^7].

## Hook Status Types

The tracing system categorizes hook operations with several status flags:

- **HOOK_STAT_CHROME**: Chrome browser-specific hook handling[^8].
- **HOOK_STAT_CHROME_FAIL**: Chrome hook resolution failed[^9].
- **HOOK_STAT_NO_FFS**: ARM64 architecture-specific Fast Forward Sequence not found[^10].
- **HOOK_STAT_SKIPPED**: Hook was intentionally skipped based on configuration[^11].
- **HOOK_STAT_TRACE**: Hook is for API tracing purposes only[^12].
- **HOOK_STAT_SYSCALL**: ARM64 system call hooking (ARM64 EC only)[^13].

## Application Hook Detection

When `HookTrace` is enabled, the system also monitors applications that attempt to modify other processes' memory, which may indicate application-level hooking attempts. This provides additional insight into potential conflicts with Sandboxie's own hooking mechanisms[^14].

## Performance Considerations

- **Increased Logging**: Enabling HookTrace generates significant log output, particularly during process startup when many modules are loaded and hooked.
- **Debug Purposes Only**: This setting is primarily intended for debugging and troubleshooting, not for production use.
- **Storage Impact**: The verbose output can quickly consume log storage space.

## Related Settings

- [ApiTrace](SandboxieTrace.md) - Traces actual API calls after hooks are established.
- [DebugTrace](SandboxieTrace.md) - General debug output from Sandboxie components.
- [FuncSkipHook](SandboxieTrace.md) - Controls which functions should not be hooked.
- [SkipHook](SandboxieTrace.md) - Module-specific hook skipping configuration.


[^1]: Hook initialization occurs in `SbieDll_HookInit()` where `Dll_HookTrace = SbieApi_QueryConfBool(NULL, L"HookTrace", FALSE)`
[^2]: Hook status tracking is implemented using multiple flags defined as `HOOK_STAT_*` constants, including `HOOK_STAT_CHROME`, `HOOK_STAT_CHROME_FAIL`, `HOOK_STAT_NO_FFS`, `HOOK_STAT_SKIPPED`, `HOOK_STAT_TRACE`, and `HOOK_STAT_SYSCALL`
[^3]: Module resolution is performed by `Trace_FindModuleByAddress((void*)module)` to identify the source module of each hooked function
[^4]: Hook trace output is sent to the monitoring system via `SbieApi_MonitorPutMsg(MONITOR_HOOK | MONITOR_TRACE | ((HookStats & HOOK_STAT_SKIPPED) ? MONITOR_OPEN : 0), dbg)`
[^5]: Chrome hook success is indicated by `HookStats & HOOK_STAT_CHROME` and logged as "Chrome Hook Hooked"
[^6]: Chrome hook failure is indicated by `HookStats & HOOK_STAT_CHROME_FAIL` and logged as "Chrome Hook Unresolved"
[^7]: ARM64 fallback is indicated by `HookStats & HOOK_STAT_NO_FFS` and logged as "FFS Target not found, hooked x86 code instead"
[^8]: `HOOK_STAT_CHROME` flag value `0x00000001` indicates successful Chrome-specific hook handling
[^9]: `HOOK_STAT_CHROME_FAIL` flag value `0x00000002` indicates failed Chrome hook resolution
[^10]: `HOOK_STAT_NO_FFS` flag value `0x00000004` indicates ARM64 Fast Forward Sequence target not found
[^11]: `HOOK_STAT_SKIPPED` flag value `0x00000008` indicates the hook was intentionally skipped
[^12]: `HOOK_STAT_TRACE` flag value `0x00000100` indicates the hook is for API tracing purposes
[^13]: `HOOK_STAT_SYSCALL` flag value `0x00000200` is used for ARM64 system call hooking in ARM64 EC mode only
[^14]: Application hook detection is implemented in `file_misc.c` where `Dll_HookTrace` enables monitoring of `WriteProcessMemory` calls that may indicate application-level hooking attempts