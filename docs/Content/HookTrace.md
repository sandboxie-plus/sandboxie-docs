# Hook Trace

`HookTrace` records diagnostic information about function hooks installed through SbieDll's common hook-installation path. It is useful when investigating hook compatibility or process-initialization problems.

```ini
[DefaultBox]

HookTrace=y
```

The output appears in the Hook category of the shared monitor used by [Sandboxie Trace](SandboxieTrace.md) and the Sandboxie Plus [Trace Log](../PlusContent/TraceLog.md). Typical entries include:

```text
Hooking: module!function
FAILED Hooking: module!function
Skipped Hooking: module!function
Hooking (trace): module!function
```

Additional platform- or implementation-specific annotations may appear. The displayed text is diagnostic output rather than a stable, exhaustive format.

Current output can include these annotations:

* `(Chrome Hook Hooked)` indicates that Sandboxie's Chrome-specific hook handling was used successfully for that hook.
* `(Chrome Hook Unresolved)` indicates that the Chrome-specific target could not be resolved through that path. This annotation alone does not establish that the application will fail.
* `FFS Target not found, hooked x86 code instead` is an ARM64EC-specific fallback. The expected Fast Forward Sequence target was unavailable, so Sandboxie hooked the x86-side code instead.

`HookTrace` covers hooks installed through this common SbieDll path; it does not report every hooking mechanism used anywhere in Sandboxie. Process startup can generate a large amount of output, so enable it only while troubleshooting.

## Application hooking records

When `HookTrace` is active, certain calls through Sandboxie's intercepted `WriteProcessMemory` path can produce records beginning with:

```text
Application Hooking:
```

These records can appear when a sandboxed application calls that path and the destination address can be associated with an exported function in another module. The current record includes the resolved module and export, an offset, and a hexadecimal representation of the bytes being written. This can help diagnose application-level code patching or hooking that may interact with Sandboxie's own hooks.

The record does not mean that every `WriteProcessMemory` call is logged, that Sandboxie detects all application hooking, or that the activity is malicious.

The setting is initialized per process. Restart affected sandboxed processes after enabling, disabling, or changing it.

`HookTrace` was introduced in Sandboxie Plus 1.15.5 and Sandboxie Classic 5.70.5.

## Related settings

* [Function Skip Hook](FuncSkipHook.md) selectively suppresses hooks by function name.
* [Skip Hook](SkipHook.md) controls named Sandboxie hook groups for matching processes.

## Related pages

* [Sandboxie Trace](SandboxieTrace.md)
* [Trace logging](../PlusContent/TraceLog.md)
