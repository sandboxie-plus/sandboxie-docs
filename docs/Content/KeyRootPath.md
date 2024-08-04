# Key Root Path

_KeyRootPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the registry location where the registry hive for a particular sandbox is mounted.

As with all sandbox settings, it may also be specified in the global section, and in that case will apply for all sandboxes where the setting is not also specified in the sandbox section.

See [Sandbox Hierarchy](SandboxHierarchy.md) for more information.

Usage:
```
   .
   .
   .
   [DefaultBox]
   KeyRootPath=\REGISTRY\USER\%BOXNAME%
```

The following substitution variables may be useful in this path.

*   The variable %SANDBOX% which expands to the name of the sandbox
*   The variable %USER% which expands to the user name
*   The variable %SID% which expands to the user security-ID (SID)
*   The variable %SESSION% which expands to the Terminal Services session number

If KeyRootPath is not specified, its default value is:

*   _\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%_

The value must begin with the prefix **\REGISTRY\USER\** or Sandboxie will not be able to mount the registry hive.

There is probably no reason to change the default value for this setting, and doing so is not recommended.

If Sandboxie cannot successfully mount or un-mount the sandboxed registry hive, it will issue messages [SBIE1241](SBIE1241.md) and [SBIE2208](SBIE2208.md), respectively.
