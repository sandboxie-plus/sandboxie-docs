# Crash and Debugger Diagnostics

Sandboxie's crash-dump and debugger-wait options are separate from [Trace Log monitoring](SandboxieTrace.md). Minidump settings create files after qualifying unhandled crashes, while debugger-wait settings pause matching processes early during Sandboxie DLL initialization so that a debugger can attach.

## Minidump crash diagnostics

### EnableMiniDump

`EnableMiniDump` is image-aware and disabled by default:

```ini
EnableMiniDump=y
EnableMiniDump=program.exe,y
```

For matching sandboxed processes, Sandboxie installs a process-local unhandled-exception dump handler that uses Windows DbgHelp `MiniDumpWriteDump` support. A dump is produced only for crashes that reach this top-level unhandled-exception path. The setting does not guarantee a dump for every crash or termination method, and it does not automatically cover unboxed SandMan, SbieSvc, SbieDrv, or every Sandboxie component.

Dump files are written inside the sandbox as:

```text
<sandbox root>\<image-name>.<unique counter>.dmp
```

The suffix is a runtime-generated unique value. The crashing sandboxed process writes the file using its current permissions.

Restart matching processes after changing `EnableMiniDump`. `EnableMiniDump` and `MiniDumpFlags` were introduced in Sandboxie Plus 1.0.5 and Sandboxie Classic 5.55.5.

### MiniDumpFlags

`MiniDumpFlags` controls the type of dump requested:

```ini
MiniDumpFlags=Extended
MiniDumpFlags=0xAABBCCDD
```

If the setting is absent, or contains unrecognized ordinary text, Sandboxie uses its built-in default flags. `Extended` requests a much more comprehensive dump. Advanced users can supply a hexadecimal Windows `MINIDUMP_TYPE` bitmask.

Extended or full-memory-style dumps can be large and may contain sensitive memory, including application data, document contents, credentials, or other secrets resident in the process. Review dumps before sharing them and do not use `Extended` as a routine default without a troubleshooting need.

## Waiting for a debugger

### WaitForDebugger

Use `WaitForDebugger` to select an executable by exact image name:

```ini
WaitForDebugger=program.exe
```

Multiple entries are supported. Matching is case-insensitive and does not use wildcard syntax. A matching process pauses very early during Sandboxie DLL initialization until a debugger attaches.

There is no timeout. If no debugger attaches, the process can remain paused indefinitely.

### WaitForDebuggerAll

```ini
WaitForDebuggerAll=y
```

This makes every affected sandboxed process wait for a debugger. It is disabled by default and should be used only for deliberate developer or troubleshooting work: accidental enablement can prevent sandboxed applications from starting normally.

### WaitForDebuggerCmdLine

```ini
WaitForDebuggerCmdLine=some argument
```

Multiple entries are supported. Each entry is matched as a case-insensitive substring of the process command line. Despite historical metadata describing this value as a pattern, it does not implement wildcard or regular-expression syntax.

`WaitForDebugger`, `WaitForDebuggerAll`, and `WaitForDebuggerCmdLine` are alternative selectors. A match from any one of them can trigger the wait.

### WaitForDebuggerSilent

After a debugger attaches, current behavior depends on `WaitForDebuggerSilent`:

* When silent mode is enabled, the process continues without Sandboxie deliberately raising a breakpoint.
* When silent mode is disabled, Sandboxie raises a debug breakpoint so the attached debugger stops there.

If `WaitForDebuggerSilent` is absent, the current runtime uses silent continuation. To request a breakpoint after attachment, configure:

```ini
WaitForDebuggerSilent=n
```

There is no SandMan **Resume** action. Attaching a debugger releases the initial wait; when breakpoint mode is used, continue execution from the debugger.

## SandMan configuration

SandMan's **Sandbox Options > Advanced Options > Debug > Debug Options** generic settings editor exposes at least `EnableMiniDump` and `WaitForDebugger`. It does not provide dedicated checkboxes for `MiniDumpFlags`, `WaitForDebuggerAll`, `WaitForDebuggerCmdLine`, or `WaitForDebuggerSilent`.

No equivalent dedicated Sandboxie Control Classic settings panel was identified for these options. The compatible manual INI settings are consumed by the shared runtime.

## Applying changes

These options are evaluated during process initialization. Restart matching sandboxed processes after changing them; recreating the affected sandbox process tree is the most reliable approach. A SandMan, service, or driver restart is not normally required.

## Related pages

* [How To Use WinDbg](HowToUseWinDbg.md)
* [Sandboxie Trace](SandboxieTrace.md)
* [Sandboxie Ini](SandboxieIni.md)
