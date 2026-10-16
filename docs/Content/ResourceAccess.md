# Resource Access

[Resource Access Settings](ResourceAccessSettings.md) control how sandboxed programs access resources. Some rules distinguish whether the requesting program's executable file is loaded from outside or inside the sandbox.

Both columns below describe programs running under Sandboxie. "Yes" means that a rule is eligible to apply to a program at that executable location, not that access is allowed. Program selectors, [rule precedence](../PlusContent/RuleSpecificity.md), and other security restrictions still affect the result.


| Setting         | Executable outside the sandbox | Executable inside the sandbox |
|-----------------|---------|--------|
|[ClosedClsid](ClosedClsid.md)        | Yes     | Yes    |
|[ClosedFilePath](ClosedFilePath.md)   | Yes     | Yes    |
|[ClosedIpcPath](ClosedIpcPath.md)    | Yes     | Yes    |
|[ClosedKeyPath](ClosedKeyPath.md)    | Yes     | Yes    |
|[ClosedRT](ClosedRT.md)   | Yes     | Yes    |
|[NoRenameWinClass](NoRenameWinClass.md) |  Yes    |    Yes    |
|[NormalFilePath](NormalFilePath.md)    | Yes     | Yes      |
|[NormalIpcPath](NormalIpcPath.md)     | Yes     | Yes      |
|[NormalKeyPath](NormalKeyPath.md)     | Yes     | Yes      |
|[OpenClsid](OpenClsid.md)        | Yes     | Yes    |
|[OpenConfPath](OpenConfPath.md)        | Yes     | Yes    |
|[OpenFilePath](OpenFilePath.md)     | Yes     | No by default       |
|[OpenIpcPath](OpenIpcPath.md)      | Yes     | Yes      |
|[OpenKeyPath](OpenKeyPath.md)      | Yes     | No by default       |
|[OpenPipePath](OpenPipePath.md)     | Yes     | Yes    |
|[OpenWinClass](OpenWinClass.md)     | Yes     | Yes    |
|[ReadFilePath](ReadFilePath.md)     | Yes  | Yes   |
|[ReadIpcPath](ReadIpcPath.md)       | Yes     | Yes   |
|[ReadKeyPath](ReadKeyPath.md)       | Yes  | Yes   |
|[WriteFilePath](WriteFilePath.md)   | Yes      | Yes     |
|[WriteKeyPath](WriteKeyPath.md)     | Yes      | Yes     |


The "No by default" entries describe the exclusion of ordinary `OpenFilePath` and `OpenKeyPath` rules for executables loaded from inside the sandbox. `DontOpenForBoxed=n` disables this exclusion, as does [Application Compartment](NoSecurityIsolation.md) mode. `OpenPipePath` and `OpenConfPath` are not subject to this exclusion.

`ReadIpcPath` refers here to its `$:...` target-process rules. These permit limited read access to another process and use a separate policy from generic named IPC-object matching; see [Read IPC Path](ReadIpcPath.md).

When `AlwaysCloseForBoxed` is active (the default outside Application Compartment mode), a negated program selector such as `!program.exe` on `ClosedFilePath`, `ClosedKeyPath`, or `ClosedIpcPath` does not exempt an executable loaded from inside the sandbox. Setting `AlwaysCloseForBoxed=n` restores normal selector matching. Sandboxie components have an additional exception for negated `ClosedIpcPath` entries.
