# Fake Process Mitigations

`FakeProcessMitigations` is an experimental compatibility setting available since
Sandboxie Plus 1.19.1. It changes what an affected sandboxed process is told about
two Windows process mitigation policies. It is disabled by default.

**This setting does not enable those Windows protections.** An application may
rely on restrictions that are reported as enabled but are not actually enforced.
Use it only when needed for compatibility, preferably for a specific executable.

## Usage

```ini
[DefaultBox]
FakeProcessMitigations=app.exe,y
```

This enables the setting for `app.exe` in `DefaultBox`. Restart affected
processes after changing it. Remove the entry or set it to `n` to disable it:

```ini
FakeProcessMitigations=app.exe,n
```

## Syntax

```ini
FakeProcessMitigations=[<process>,]y|n
```

Omitting the process selector applies the setting to processes in the sandbox:

```ini
FakeProcessMitigations=y
```

The setting selects processes by image, not by command-line arguments.

## Reported Policies

When enabled, Sandboxie hooks `GetProcessMitigationPolicy` if the API is
available. The real API is called first. Only a successful query using the
current-process pseudo-handle and a sufficiently sized output buffer is changed:

| Policy | Reported values |
| --- | --- |
| `ProcessDynamicCodePolicy` | `ProhibitDynamicCode=1`, `AllowThreadOptOut=0`, and `AllowRemoteDowngrade=0`. Other bits are unchanged. |
| `ProcessExtensionPointDisablePolicy` | `DisableExtensionPoints=1`. Other bits are unchanged. |

Failed queries, other policies, and queries using a real process handle are not
modified, even if that handle refers to the calling process. Native or direct
queries that bypass this API hook are not changed. The setting does not change
Windows mitigation enforcement and does not guarantee that an application will
start or work correctly.
