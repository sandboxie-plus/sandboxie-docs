# Ipc Root Path

_IpcRootPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the NT named-object namespace root for a box, not a folder on disk. Sandboxie also derives a related pipe-path representation from this root.

It may be set for a box or supplied through `[GlobalSettings]` or an applicable enabled template. Its default contains `%SESSION%`, so the expanded namespace root can differ between Windows sessions.

See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) and [Sandbox Hierarchy](SandboxHierarchy.md) for its relationship to the other roots.

Usage:
```
   .
   .
   .
   [DefaultBox]
   IpcRootPath=\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%
```

The following substitution variables may be useful in this path.

*   The variable %SANDBOX% which expands to the name of the sandbox
*   The variable %USER% (or %USERNAME%) which expands to the user name
*   The variable %SID% which expands to the user security-ID (SID)
*   The variable %SESSION% which expands to the Terminal Services session number

If IpcRootPath is not specified, its default value is:

*   _\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%_

There is probably no reason to change the default value for this setting, and doing so is not recommended.

`%BOXNAME%` is not a supported alias in this root-expansion path; use `%SANDBOX%`. Changing this namespace root does not itself permit access to host IPC objects or replace [NT Namespace Isolation](NtNamespaceIsolation.md) and IPC access rules. Restart affected sandboxed processes after a change; an existing process retains its initialized root.

In SandMan, the global default is at **Global Settings > Advanced Config > Sandboxie Config > Sandbox ipc root**. A per-box value can be entered in **Sandbox Options > Advanced Options > Miscellaneous > Add Option**.
