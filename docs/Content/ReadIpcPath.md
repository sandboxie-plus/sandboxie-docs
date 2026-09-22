# Read IPC Path

_ReadIpcPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.0.16 / Classic 5.55.16. Its documented process-target form permits restricted read access from sandboxed programs to an unsandboxed process or a process in another sandbox.

```ini
[DefaultBox]
ReadIpcPath=$:program.exe
```

An optional [Program Name Prefix](ProgramNamePrefix.md) can qualify which sandboxed source process this rule applies to. For example:

```ini
ReadIpcPath=source.exe,$:target.exe
```

Here `source.exe` selects the sandboxed process making the access attempt, while `$:target.exe` identifies the external target process. The source selector determines whether the rule is loaded for that sandboxed process; the `$:` target is then evaluated by the separate process/thread access matcher.

The `$:` prefix identifies the target process. Process-name matching in this path is case-insensitive. The supported documented forms are an executable name and the explicit all-processes special case:

```ini
ReadIpcPath=$:program.exe
ReadIpcPath=$:*
```

Do not treat forms such as `$:service*.exe` as general wildcard matching; the current target-process matcher does not provide that behavior.

For target-process access, the relevant rule order is Closed, then Open, then Read:

* a matching `ClosedIpcPath=$:...` rule denies access;
* a matching `OpenIpcPath=$:...` rule can grant broader process/thread access;
* a matching `ReadIpcPath=$:...` rule permits the restricted read category.

This target-process policy is separate from [Rule Specificity](../PlusContent/RuleSpecificity.md). `UseRuleSpecificity` does not change the `$:` action order.

Generic named IPC object access is governed primarily by Normal, Open, and Closed IPC path rules. `ReadIpcPath` should not be treated as the direct IPC equivalent of `ReadFilePath` for arbitrary named objects; Sandboxie components may have additional bounded consumers of the setting.

The built-in configuration includes read access to `explorer.exe` for compatibility. To override it for a sandbox, use:

```ini
[DefaultBox]
ClosedIpcPath=$:explorer.exe
```

Related Sandboxie Plus settings:

* **Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Read Only**
* **Sandbox Options > General Options > Restrictions > Other restrictions > Allow to read memory of unsandboxed processes (not recommended)**
