# Job Objects

## Overview

Sandboxie normally assigns sandboxed processes to a Windows Job Object managed by Sandboxie. This Job Object provides process grouping and lifecycle functions, selected Windows Job Object GUI restrictions, the resource limits documented on the related setting pages, and optional collective termination behavior.

The Job Object is only one layer of Sandboxie's architecture. Token restrictions, file-system and registry isolation, IPC and object isolation, network restrictions, and other GUI hooks and policies are implemented separately.

## Sandboxie's Job Object

Sandboxie normally maintains a Job Object for each combination of sandbox and Windows session. GuiServer finds or creates the appropriate object when a sandboxed process starts.

If the existing Job Object still contains active processes, Sandboxie reuses it. After it has no active processes, Sandboxie closes the old handle and creates a fresh Job Object when one is next required. Settings applied when the Job Object is created therefore take effect on the newly created object.

Sandboxie assigns each affected process during process initialization. Its root Job Object allows breakaway for compatibility with applications and Windows Job behavior, but Sandboxie still evaluates each sandboxed process as it starts and can request its association with the root Job again. Breakaway from a Job Object does not by itself move a process outside the sandbox or disable Sandboxie's other isolation layers.

## Default GUI restrictions

The normal Sandboxie Job Object currently applies these Windows Job Object UI restrictions:

| Restriction | Effect through the Job Object |
| --- | --- |
| `JOB_OBJECT_UILIMIT_EXITWINDOWS` | Prevents processes in the Job from using the Windows shutdown and logoff operations controlled by this restriction. |
| `JOB_OBJECT_UILIMIT_HANDLES` | Restricts access to USER handles created outside the Job, except where access is explicitly granted. |
| `JOB_OBJECT_UILIMIT_SYSTEMPARAMETERS` | Restricts changes to system parameters. |
| `JOB_OBJECT_UILIMIT_READCLIPBOARD` | Restricts clipboard reads through the Windows Job Object mechanism. |

Sandboxie explicitly grants required USER-handle access where necessary, including access to the desktop window. These restrictions are an additional Windows Job Object layer; they do not implement all of Sandboxie's GUI or clipboard isolation.

The following settings cause Sandboxie to omit these basic Job Object UI restrictions without removing the process from Sandboxie's root Job Object:

- `OpenWndStation=y`
- `OriginalToken=y`
- `UnrestrictedToken=y`

These settings do not by themselves remove process grouping or disable resource limits carried by the root Job. For the Window Station and Desktop aspects of `OpenWndStation`, see [Sandbox Desktop and Window Station](SandboxDesktop.md).

## `NoAddProcessToJob`

```ini
NoAddProcessToJob=y
```

`NoAddProcessToJob` is a box-wide Boolean setting. Its default is absent or `n`.

When enabled, affected sandboxed processes are not assigned to Sandboxie's root Job Object. Consequently:

- the root Job's GUI restrictions do not apply to those processes;
- [Process Memory Limit](ProcessMemoryLimit.md), [Total Memory Limit](TotalMemoryLimit.md), [Process Number Limit](ProcessNumberLimit.md), and [CPU Rate Limit](CpuRateLimit.md) do not apply through that root Job;
- collective termination through the root Job is not available as the normal mechanism;
- sandboxed applications can use their own Job Objects without those Jobs being nested beneath Sandboxie's root Job.

This setting does not disable Sandboxie. File-system, registry, IPC, network, token, GUI, and other independent restrictions remain governed by their own settings and implementation.

`NoAddProcessToJob` has been available since Sandboxie Plus 0.3.5 and Sandboxie Classic 5.42.1.

## `AllowBoxedJobs`

```ini
AllowBoxedJobs=y
```

`AllowBoxedJobs` is a box-wide Boolean setting. Its current default is absent or `n`.

Unlike `NoAddProcessToJob`, this setting does not remove a process from Sandboxie's root Job Object. On Windows 8, Windows Server 2012, and later versions that support nested Job Objects, it permits sandboxed applications to create and use real additional Job Objects nested beneath Sandboxie's root Job.

With `AllowBoxedJobs=n`:

- named Job Objects used by sandboxed applications are still handled inside Sandboxie's object-namespace model;
- Sandboxie prevents real assign and terminate control over boxed Job Objects;
- assignment requests can be compatibility-simulated instead of creating a real nested assignment;
- related compatibility handling is used for Job completion-port and process-creation Job-list operations.

With `AllowBoxedJobs=y` on a supported Windows version:

- real nested Job assignment is allowed;
- assign and terminate access can be granted for boxed Jobs where permitted by the sandbox object rules;
- Sandboxie's root Job remains present;
- the root Job's configured resource limits remain active;
- Sandboxie's object-namespace isolation continues to apply.

Sandboxie enforces these decisions through both its user-mode API handling and driver-level Job Object access checks.

`AllowBoxedJobs` has been available since Sandboxie Plus 0.8.5 and Sandboxie Classic 5.50.5.

## Comparison

| Configuration | Sandboxie root Job | Root-Job GUI restrictions | Root-Job resource limits | Application-owned Job Objects |
| --- | --- | --- | --- | --- |
| Normal/default | Yes | Yes, unless independently suppressed | Available and configurable | Restricted or compatibility-simulated by default |
| `NoAddProcessToJob=y` | No | No | No | Available outside Sandboxie's root Job |
| `AllowBoxedJobs=y` | Yes | Yes, unless independently suppressed | Remain active | Real nested Jobs on supported Windows versions |
| `NoSecurityIsolation=y` | No | No | No | Not blocked merely because the Sandboxie root Job is absent |

In short:

- `NoAddProcessToJob=y` prevents use of Sandboxie's root Job for the process.
- `AllowBoxedJobs=y` retains Sandboxie's root Job and permits application-owned nested Jobs.

## Resource limits

Sandboxie's root Job Object can carry the settings documented on these pages:

- [Process Memory Limit](ProcessMemoryLimit.md)
- [Total Memory Limit](TotalMemoryLimit.md)
- [Process Number Limit](ProcessNumberLimit.md)
- [CPU Rate Limit](CpuRateLimit.md)

`AllowBoxedJobs=y` does not remove these limits. They become ineffective through Sandboxie's root Job when `NoAddProcessToJob=y`, [`NoSecurityIsolation=y`](NoSecurityIsolation.md), or [`OpenWinClass=*`](OpenWinClass.md) causes Sandboxie to avoid that Job.

`OpenWndStation=y`, `OriginalToken=y`, and `UnrestrictedToken=y` can suppress only the basic Job Object UI restrictions described above; they do not themselves remove the root Job or its resource limits.

## `TerminateJobObject`

```ini
TerminateJobObject=y
```

`TerminateJobObject` is a box-wide Boolean setting introduced in Sandboxie Plus 1.15.4 and Sandboxie Classic 5.70.4. Its default is absent or `n`, and it currently has no dedicated SandMan control.

When enabled, eligible host-side **Terminate All** handling can first attempt to terminate Sandboxie's root Job Object. Sandboxie's process service still enumerates and terminates remaining sandboxed processes afterward, so Job termination is not the sole cleanup mechanism. The option does not guarantee that every termination request uses a Job, particularly when the sandbox has no usable root Job Object.

## Application Compartment and related settings

With:

```ini
NoSecurityIsolation=y
```

Application Compartment processes are not assigned to Sandboxie's root Job Object. The four root-Job GUI restrictions and the resource limits listed above therefore do not apply through that Job. This does not imply that Application Compartment processes cannot use Job Objects of their own. See [No Security Isolation](NoSecurityIsolation.md) for the broader behavior of this box type.

Similarly, `OpenWinClass=*` causes Sandboxie to avoid its root Job Object for the affected configuration. The root-Job GUI restrictions and resource limits consequently do not apply through that Job. Other window-class behavior is documented under [Open Win Class](OpenWinClass.md).

## SandMan configuration

The current controls are located at:

**Sandbox Options > Security Options > Job Object**

**Add sandboxed processes to job objects (recommended)**

- Checked: `NoAddProcessToJob` remains absent or at its default.
- Unchecked: SandMan writes `NoAddProcessToJob=y`.

**Allow use of nested job objects (works on Windows 8 and later)**

- Checked: SandMan writes `AllowBoxedJobs=y`.
- Unchecked: SandMan removes the setting, restoring its default.

SandMan disables the relevant Job Object controls when the current box configuration cannot use Sandboxie's root Job, including Application Compartment and `OpenWinClass=*` cases. `TerminateJobObject` is a manual INI option and is not exposed by a dedicated checkbox. These controls are not part of the New Box Wizard.

## Sandboxie Control Classic

The relevant runtime components are shared by Sandboxie Plus and Classic, so compatible manual INI and template configuration can be consumed by the shared runtime.

SandMan provides the current dedicated controls for `NoAddProcessToJob` and `AllowBoxedJobs`. Current Sandboxie Control Classic does not provide equivalent dedicated controls for those settings or for `TerminateJobObject`; Classic users can configure them manually where applicable.

## Applying configuration changes

Job assignment decisions are made during process initialization. Restart affected sandboxed processes after changing `NoAddProcessToJob` or `AllowBoxedJobs`.

Resource limits and GUI restrictions are configured when Sandboxie creates its root Job Object. If that Job still contains active processes, Sandboxie reuses it. To ensure newly configured Job settings are applied, allow the sandbox to become empty so Sandboxie can create a fresh Job Object when the next process starts. A Windows restart is not normally required.

## Version history

- **Sandboxie Plus 0.3.5 / Classic 5.42.1:** `NoAddProcessToJob` was introduced.
- **Sandboxie Plus 0.5.5 / Classic 5.46.4:** compatibility changes allowed Chrome-related applications to make fuller use of their Job system with `NoAddProcessToJob=y`.
- **Sandboxie Plus 0.8.5 / Classic 5.50.5:** `AllowBoxedJobs` was introduced.
- **Sandboxie Plus 1.1.1 / Classic 5.56.1:** `AllowBoxedJobs=y` became the default.
- **Sandboxie Plus 1.1.3 / Classic 5.56.3:** the default was restored to `n` after compatibility problems.
- **Sandboxie Plus 1.15.4 / Classic 5.70.4:** `TerminateJobObject` was introduced, with individual process termination as the normal default path.

## Related pages

- [Process Memory Limit](ProcessMemoryLimit.md)
- [Total Memory Limit](TotalMemoryLimit.md)
- [Process Number Limit](ProcessNumberLimit.md)
- [CPU Rate Limit](CpuRateLimit.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Open Win Class](OpenWinClass.md)
- [Sandbox Desktop and Window Station](SandboxDesktop.md)
