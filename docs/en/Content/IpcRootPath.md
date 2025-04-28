# Ipc Root Path

_IpcRootPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the location within the NT object namespace where a particular sandbox is created.

As with all sandbox settings, it may also be specified in the global section, and in that case will apply for all sandboxes where the setting is not also specified in the sandbox section.

See [Sandbox Hierarchy](SandboxHierarchy.md) for more information.

Usage:
```
   .
   .
   .
   [DefaultBox]
   IpcRootPath=\Sandbox\%BOXNAME%
```

The following substitution variables may be useful in this path.

*   The variable %SANDBOX% which expands to the name of the sandbox
*   The variable %USER% which expands to the user name
*   The variable %SID% which expands to the user security-ID (SID)
*   The variable %SESSION% which expands to the Terminal Services session number

If IpcRootPath is not specified, its default value is:

*   _\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%_

There is probably no reason to change the default value for this setting, and doing so is not recommended.
