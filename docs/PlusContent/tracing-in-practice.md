# Tracing in practice

This page is the hands-on companion to [Trace logging](TraceLog.md). That page documents the trace mechanism (buffer, stack traces, performance); this one describes how to actually get a useful log and read it, based on the current driver behaviour. It also separates the trace settings that are active today from ones that only survive as legacy metadata.

Everything here applies to the current release (1.18.x). If you arrived from older documentation or an old forum answer, note the current-versus-legacy table below — several widely quoted trace option names no longer do anything.

## The three prerequisites

Resource tracing only records what you asked it to record. All three of these must be in place, and the first one is where most people get stuck:

1. **Enable the monitor.** In SandMan, choose **View > Trace Logging** (Sandbox Options > Global Settings > Advanced Options, when using the standalone trace monitor). Note that this switch lives in the *View* menu — it is not a button inside the Trace Log panel, and toggling the panel alone does not enable it.

2. **Set per-box trace masks.** A box only records the access types its trace settings ask for (the driver reads these when the process starts). For a first diagnostic pass on file and registry access:

    ```ini
    [MyBox]
    FileTrace=ad
    KeyTrace=ad
    IpcTrace=ad
    ```

    Without these lines the Trace Log stays completely empty, no matter how the global switch is set. The same settings are available in SandMan under **Sandbox Options > Advanced Options > Tracing**.

3. **Reproduce while tracing.** Only accesses that happen while the monitor is active are recorded; the log is a live stream, not a historical archive.

## Current trace settings versus legacy names

The trace options that the current driver actually consumes are:

| Setting | Records |
| --- | --- |
| `FileTrace` | file accesses |
| `KeyTrace` | registry accesses |
| `IpcTrace` | IPC object accesses (named objects, sections, RPC) |
| `PipeTrace` | named pipe accesses |
| `CallTrace` | system-call level records |
| `GuiTrace` | GUI-related records |

Each value is a combination of characters:

| Character | Records |
| --- | --- |
| `a` | accesses that are allowed |
| `d` | accesses that are denied |
| `i` | accesses to ignore |
| `*` | all of the above |

`FileTrace=ad` therefore logs both successful and blocked file accesses — the usual starting point.

!!! warning

    Older documentation and wiki pages also mention `ApiTrace`, `HookTrace`, `ErrorTrace` and `DebugTrace`. These names still appear in the settings metadata file, but the current driver contains no code path that reads them: setting them has **no effect**. If a guide tells you to enable `ApiTrace` to see what a program does, it is describing an older Sandboxie.

## Confirming that tracing actually works

Before analysing a log, confirm the pipeline end to end:

1. Open **View > Trace Logging**.
2. Launch a short-lived program in a traced box — for example `notepad` started in the box.
3. Watch the Trace Log panel. If records appear, the monitor is live and the masks are in effect.
4. If the panel stays empty, the usual causes are: the global switch is off (step 1 above), the box has no trace masks, or the accesses you expect happened *before* tracing was enabled.

This quick check separates "the monitor is not running" from "nothing interesting happened", which are otherwise easy to confuse.

## The two export formats

The trace view has two display modes, and they export different things:

- **Monitor mode** (the default tree view) shows aggregated counts per resource. Exporting from this mode writes the aggregate table — handy for a quick overview, but it has no per-record details.
- **Trace log mode** (switch the monitor-mode toggle off in the toolbar) shows individual records. Exporting from this mode writes a tab-separated file with one record per line: timestamp, process, PID, TID, type, status, name and message. This is the format to use for analysis and for sharing in an issue.

Use the **Save to file** button (the floppy-disk icon) in the trace view toolbar after switching to Trace log mode.

## One behaviour that surprises most people

**Accesses denied by a Closed* rule are not recorded.** The monitor writes a denied record only when the path matched *no* explicit path rule at all — a normal `ClosedFilePath` hit counts as the rule working as designed and leaves no trace entry.

The practical consequence: a tool that collects "denied" entries from the trace and proposes opening rules for them collects exactly the wrong cases, and the privacy/security boxes (`ClosedFilePath`, `ClosedKeyPath`, and the lock-down set of privacy-mode boxes) produce no denied records at all.

## Diagnosing a program that fails in a stricter box

The working direction is the inverse of what the trace seems to suggest:

1. Let the program run to completion in a box where it **works**, with `FileTrace=ad` (and the other masks as needed) set on that box.
2. Export the trace log (Trace log mode).
3. Compare the recorded accesses against the blocking rules of the box where the program **fails** (`ClosedFilePath`, `ClosedKeyPath`, `ClosedIpcPath`, `BlockNetworkFiles`). The accesses that match a blocking rule of the target box are the candidates.
4. Add access rules for those resources only, and retest in the target box.

Step 3 is mechanical — a small script can do it — but the judgement stays with you: decide which resources to open, and prefer the narrowest rule that works (read-only rules where the program only reads).

## Performance

Tracing is not free: every recorded access costs a little, and stack-trace capture considerably more. See [Performance impact](TraceLog.md#performance-impact) for the details, and keep the masks as narrow as the investigation requires — a full `*` across every category is rarely the right starting point.

## Related pages

- [Trace logging](TraceLog.md) — the mechanism, buffer and stack-trace options
- [Sandboxie Trace](../Content/SandboxieTrace.md) — the underlying `Trace*` settings
- [Sandboxie Ini](../Content/SandboxieIni.md) — configuration file reference
- [Application Compartment](compartment-mode.md) — the relaxed box type often used for games
