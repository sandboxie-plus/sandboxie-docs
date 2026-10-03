# Open Conf Path

_OpenConfPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.0 / 5.55.0. It specifies a path pattern, for which Sandboxie will not apply sandboxing for registry keys. This lets sandboxed programs have direct access to update system settings _outside the sandbox_. This setting essentially _punches a hole_ in the sandbox, at a particular registry key location.

Once selected, _OpenConfPath_ uses the same direct-host Registry access model as [OpenKeyPath](OpenKeyPath.md). Its important difference is eligibility: it is not excluded by the normal boxed-executable Open rule gate. **Open for All** means eligible for boxed executables, not guaranteed precedence; process selectors and [Rule Specificity](../PlusContent/RuleSpecificity.md) still apply.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   OpenConfPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenConfPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

These examples let the Firefox program, _firefox.exe_, have direct access to the Mozilla registry key trees (both system-wide and per-user registry trees).

The value specified for _OpenConfPath_ can include wildcards, although for registry keys, the use of wildcards is rarely needed. For more information on this, including examples that show the use of wildcards, see [OpenFilePath](OpenFilePath.md). (_OpenFilePath_ deals with files, not registry keys, but the principle of using wildcards remains the same.)

**Note:** This setting can apply even when the program executable file resides within the sandbox. This means that (potentially malicious) software downloaded into your computer and executed can take advantage of direct host access when this rule wins and native permissions allow it.

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Open for All
