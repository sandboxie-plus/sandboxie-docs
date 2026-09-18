# Sandboxie Trace

Sandboxie provides several independent tracing mechanisms for troubleshooting compatibility and isolation rules. Their output is collected in a shared per-session monitor buffer and can be viewed through:

* [Trace logging](../PlusContent/TraceLog.md) in Sandboxie Plus;
* [Resource Access Monitor](ResourceAccessMonitor.md) in Sandboxie Control Classic.

Opening either viewer activates the monitor consumer. It does not automatically enable every detailed trace option described below. Some baseline resource activity is available without additional settings, while options such as `ApiTrace`, `HookTrace`, `DebugTrace`, and `ErrorTrace` add specialized or higher-volume diagnostics.

When no monitor consumer is active, the shared monitor buffer is not maintained and its messages are not retained for later display. Explicitly enabled trace options can still install hooks or perform process-side diagnostic work while the viewer is closed.

The monitor is separate from [Log Message Events](LogMessageEvents.md), which sends selected Sandboxie messages to the Windows Event Log. Crash dumps and process startup pauses are covered under [Crash and Debugger Diagnostics](CrashAndDebuggerDiagnostics.md).

## Resource-access tracing

Resource trace settings help identify file, registry, IPC, and related operations that may explain why a sandboxed application fails. Driver resource filters use these practical values where the particular setting supports them:

| Value | Meaning |
| ----- | ------- |
| `A` | Successful or allowed operations |
| `D` | Failed or denied operations |
| `I` | Ignored-device operations, where supported |
| `*` | Broad tracing |

Combinations such as `AD` are supported, and lowercase combinations such as `ad` are accepted by settings that use this filter. The letters are not implemented uniformly by every trace option.

### FileTrace

In resource mode, `FileTrace` records file, directory, volume, and device activity:

```ini
FileTrace=A
FileTrace=D
FileTrace=AD
FileTrace=I
FileTrace=*
```

`A` selects successful or allowed activity, `D` selects failed or denied activity, and `I` selects the ignored-device class. `*` requests broad file-resource tracing.

The same legacy setting name also has a separate advanced SbieDll file-API tracing use:

```ini
FileTrace=y
FileTrace=program.exe,y
```

This form adds detailed file API-call records and can be limited to an executable. Treat the resource-filter and image-qualified Boolean forms as distinct diagnostic uses of the same legacy name rather than as one combined syntax.

### KeyTrace, PipeTrace, and IpcTrace

These settings support allowed/successful and denied/failed resource filters:

```ini
KeyTrace=AD
PipeTrace=AD
IpcTrace=AD
```

* `KeyTrace` records registry-key operations.
* `PipeTrace` records named-pipe and mailslot operations.
* `IpcTrace` records access to other IPC objects and process-to-process operations.

`I` does not currently have a meaningful role for these settings.

### GuiTrace

`GuiTrace` is a legacy setting. Its direct GUI tracing implementation belongs to the old Windows XP-era Win32k hook path; modern supported Windows versions do not provide an equivalent implementation through this option. GUI- and window-class-related events can still appear through other monitor mechanisms, but enabling `GuiTrace` on Windows 10 or Windows 11 should not be expected to reproduce the historical GUI trace.

### ClsidTrace

`ClsidTrace` adds detailed COM operation records. The current runtime treats an explicit non-empty legacy value as enabled, rather than interpreting `A`, `D`, and `I` as resource filters. Use the SandMan checkbox where available, or remove the explicit entry to disable manually configured tracing.

### NetFwTrace

`NetFwTrace` is marked disabled in the current settings metadata. Limited user-mode network diagnostic remnants remain, but the old WFP/firewall logging path is not a functional, complete firewall trace. A **Network Firewall** trace checkbox may still be visible in SandMan; it should not be treated as a general WFP packet or firewall-decision logger. Remove an explicit entry rather than relying on `NetFwTrace=n` as a manual disable form.

## Troubleshooting a denied resource

A denied trace record does not by itself mean that access should be allowed. Many denied operations are expected and harmless. Test a configuration change only when the event plausibly correlates with the application failure, and prefer the narrowest resource-specific rule. Opening host resources can reduce sandbox isolation.

Use the resource type to identify the relevant configuration family:

| Trace resource | Related access settings |
| -------------- | ----------------------- |
| Files, directories, volumes, and devices | [Open File Path](OpenFilePath.md), [Closed File Path](ClosedFilePath.md), [Read File Path](ReadFilePath.md) |
| Registry keys | [Open Key Path](OpenKeyPath.md), [Closed Key Path](ClosedKeyPath.md), [Read Key Path](ReadKeyPath.md) |
| Named pipes and mailslots | [Open Pipe Path](OpenPipePath.md) |
| IPC and process-to-process objects | [Open Ipc Path](OpenIpcPath.md), [Closed Ipc Path](ClosedIpcPath.md) |
| GUI and window access | [Open Win Class](OpenWinClass.md) |
| COM classes | [Open Clsid](OpenClsid.md), [Closed Clsid Path](ClosedClsid.md) |

For example, if a denied IPC event for `\BaseNamedObjects\Xyzzy` repeatedly appears at the time of a reproducible failure and there is a clear reason to test access to that object:

```ini
[DefaultBox]
OpenIpcPath=\BaseNamedObjects\Xyzzy
```

A practical test is:

1. Reproduce the problem while Trace Logging is active.
2. Locate a denied event near the failure and identify its resource type.
3. Decide whether that specific event plausibly explains the failure.
4. If so, add the narrowest appropriate rule temporarily.
5. Reload or apply the configuration as needed, restart the affected application, and reproduce the test.
6. Compare the behavior and remove the rule if it does not solve the problem.

Do not use broad `Open*` wildcards as a generic troubleshooting method. A trace category does not mechanically determine that one particular access rule is required.

## API-call tracing

### ApiTrace

`ApiTrace` records calls that pass through Sandboxie's common SbieDll hook mechanism:

```ini
ApiTrace=y
ApiTrace=program.exe,y
```

It is image-aware, but it does not trace every Windows API used by an application. The output appears as API-call records in the monitor. Because this option can be high-volume and intrusive, enable it only while troubleshooting and restart affected processes after changing it.

### ApiTraceDll

`ApiTraceDll` extends `ApiTrace` by adding trace-only hooks for named exports in selected modules. Multiple entries are supported:

```ini
ApiTraceDll=kernel32.dll
ApiTraceDll=user32.dll
```

Use module base names rather than full paths. Module matching is case-insensitive. Not every export is guaranteed to be traceable.

### ApiSkipTrace

`ApiSkipTrace` excludes matching function-name prefixes, primarily from the additional export coverage requested with `ApiTraceDll`:

```ini
ApiSkipTrace=Nt
```

Multiple entries are supported. Prefix matching is case-sensitive. This is not a universal suppression rule for Sandboxie's normal hooks.

For installation diagnostics rather than call records, see [Hook Trace](HookTrace.md).

## Syscall and internal tracing

### CallTrace

`CallTrace` is driver syscall tracing, not generic Windows API tracing:

```ini
CallTrace=A
CallTrace=D
CallTrace=AD
CallTrace=*
```

`A` broadly records intercepted calls that reach the trace path. `D` adds calls that return a non-success NTSTATUS. These letters should not be interpreted as a universal allowed-versus-denied classification. SandMan's **Syscall Trace** checkbox writes `CallTrace=*`.

### CallTraceEx

`CallTraceEx` requests a separate advanced syscall-tracing mechanism based on Windows process instrumentation callbacks. Any configured non-empty value currently requests it. It is intended for modern Windows, is not supported across every architecture or configuration, and has no dedicated SandMan checkbox.

### SbieTrace

`SbieTrace` enables selected diagnostics for interaction between SbieDll and other Sandboxie core components. Its output appears as Debug-type records. It is not a complete internal execution trace.

### DebugTrace

`DebugTrace` captures application `OutputDebugString` output into the monitor while preserving the application's normal debug-output call. It should not be treated as lossless capture of arbitrarily long strings.

### ErrorTrace

`ErrorTrace` records nonzero Win32 last-error assignments observed through the currently hooked path. It can be extremely noisy and does not cover every Windows error or every NTSTATUS.

## DNS tracing

`DnsTrace` records the intercepted Winsock service-lookup path used by Sandboxie's DNS compatibility and filtering layer. It can show request names, IPv4 and IPv6 results, lookup errors or completion, and responses affected by `NetworkDnsFilter` when that feature is configured.

It does not trace every DNS API, capture DNS packets, or cover applications that use their own direct resolver. Queried hostnames and returned addresses may appear in the Trace Log, so review trace output before sharing it. `DnsTrace` does not enable `NetworkDnsFilter`.

The current runtime treats an explicit non-empty legacy value as enabled. Use SandMan's control where available, or remove the entry to disable it manually rather than relying on `DnsTrace=n`.

`DnsTrace` was introduced in Sandboxie Plus 1.14.0 and Sandboxie Classic 5.69.0.

## Stack traces

`MonitorStackTrace` is an effectively global monitor option and is disabled by default. When enabled before the monitor buffer is created, stack addresses are attached to records that pass through the common monitor path:

```ini
[GlobalSettings]
MonitorStackTrace=y
```

Not every diagnostic source is guaranteed to include a stack, and stacks may be incomplete or contain frames that cannot be symbolized. SandMan resolves symbols asynchronously and may use or install DbgHelp and symbol support. Stack capture and symbol resolution add diagnostic cost, and symbol downloads can involve network access.

SandMan exposes this setting through **Show Stack Trace** in the Trace Log. Changing it does not rebuild an active monitor buffer. For reliable activation or deactivation:

1. Change **Show Stack Trace**.
2. Stop Trace Logging.
3. Start Trace Logging again.

A service or driver restart is not normally required. `MonitorStackTrace` was introduced in Sandboxie Plus 1.9.6 and Sandboxie Classic 5.64.6.

## Monitor buffer size

`TraceBufferPages` controls the allocation size of the shared trace/monitor buffer. The current configured default is `256`, and the value is read when monitoring starts:

```ini
[GlobalSettings]
TraceBufferPages=2560
```

The example requests a larger buffer; it does not represent a documented byte or MiB conversion. A larger value can reduce overflow at the cost of additional memory. If the buffer cannot accept more records, events can be dropped and Sandboxie can report a monitor-buffer overflow.

Changing the setting while monitoring is active does not resize the current buffer. Stop and restart Trace Logging or the Resource Access Monitor after changing it.

## Related monitor controls

`DisableResourceMonitor=y` suppresses many normal user-mode and resource-monitor submissions for the affected sandbox or process. It does not guarantee that every explicitly enabled driver trace is suppressed.

`MonitorAdminOnly` restricts activation of the shared monitor to administrators and is effectively global for the monitor-control check. See [Monitor Admin Only](MonitorAdminOnly.md).

## SandMan configuration

Open the live viewer through **View > Trace Logging**. Per-box trace controls are under **Sandbox Options > Advanced Options > Tracing** and currently include:

* Disable Resource Monitor;
* Syscall, File, Pipe, Registry Key, IPC, GUI, COM Class, Network Firewall, and DNS tracing;
* Hook, API, Debug Output, and Error tracing.

Advanced settings without dedicated controls include `ApiTraceDll`, `ApiSkipTrace`, `CallTraceEx`, `SbieTrace`, and `TraceBufferPages`. `MonitorStackTrace` is controlled by **Show Stack Trace** in the Trace Log rather than by the per-box tracing checkbox group.

## Applying changes

Many trace settings are initialized or cached by each sandboxed process. Restart affected processes after changing them. Options that affect the shared monitor buffer, including `MonitorStackTrace` and `TraceBufferPages`, require stopping and restarting monitoring so that a new buffer is created.

Explicitly enabled trace settings may install hooks or perform process-side work even while no viewer is open. Active monitoring overhead depends on the enabled diagnostics and event volume.

## Version history

* `ApiTrace`, `ApiTraceDll`, and `ApiSkipTrace` were added to settings metadata in version 1.13.0.
* `DnsTrace` was introduced in Sandboxie Plus 1.14.0 and Sandboxie Classic 5.69.0.
* `CallTraceEx` was added in version 1.14.3.
* `HookTrace` was introduced in Sandboxie Plus 1.15.5 and Sandboxie Classic 5.70.5.

## Related pages

* [Trace logging](../PlusContent/TraceLog.md)
* [Resource Access Monitor](ResourceAccessMonitor.md)
* [Hook Trace](HookTrace.md)
* [Crash and Debugger Diagnostics](CrashAndDebuggerDiagnostics.md)
* [Sandboxie Ini](SandboxieIni.md)
