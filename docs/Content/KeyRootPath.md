# Key Root Path

_KeyRootPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the registry location where the registry hive for a particular sandbox is mounted. The hive's backing file, `RegHive`, resides beneath [FileRootPath](FileRootPath.md); the two roots are not interchangeable.

It may be set for a box or supplied through `[GlobalSettings]` or an applicable enabled template. The expanded root is established when Sandboxie constructs the box path information, and an already mounted hive can constrain a change to the same registry target.

See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) and [Sandbox Hierarchy](SandboxHierarchy.md) for the distinction between hive file and registry mount point.

Usage:
```
   .
   .
   .
   [DefaultBox]
   KeyRootPath=\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%
```

The following substitution variables may be useful in this path.

*   The variable %SANDBOX% which expands to the name of the sandbox
*   The variable %USER% (or %USERNAME%) which expands to the user name
*   The variable %SID% which expands to the user security-ID (SID)
*   The variable %SESSION% which expands to the Terminal Services session number

If KeyRootPath is not specified, its default value is:

*   _\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%_

`%BOXNAME%` is not a supported alias in this root-expansion path; use `%SANDBOX%`. The current root initializer does not itself enforce a `\REGISTRY\USER\` prefix on a custom value. Nevertheless, the expanded value must be a usable registry mount target or hive mounting will fail. The default under `\REGISTRY\USER\` is the appropriate choice for ordinary boxes.

There is usually no reason to change this default. The service also uses the registry root to identify a mounted image or RAM-disk box; changing it while a box is in use can create a mount conflict. This setting does not change registry access permissions.

If Sandboxie cannot successfully mount or un-mount the sandboxed registry hive, it will issue messages [SBIE1241](SBIE1241.md) and [SBIE2208](SBIE2208.md), respectively.

In SandMan, the global default is at **Global Settings > Advanced Config > Sandboxie Config > Sandbox registry root**. A per-box value can be entered in **Sandbox Options > Advanced Options > Miscellaneous > Add Option**.
