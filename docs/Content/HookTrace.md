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

`HookTrace` covers hooks installed through this common SbieDll path; it does not report every hooking mechanism used anywhere in Sandboxie. Process startup can generate a large amount of output, so enable it only while troubleshooting.

The setting is initialized per process. Restart affected sandboxed processes after enabling, disabling, or changing it.

`HookTrace` was introduced in Sandboxie Plus 1.15.5 and Sandboxie Classic 5.70.5.

## Related pages

* [Sandboxie Trace](SandboxieTrace.md)
* [Trace logging](../PlusContent/TraceLog.md)
