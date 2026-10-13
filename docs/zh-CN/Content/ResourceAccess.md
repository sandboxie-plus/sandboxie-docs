# 资源访问

[资源访问设置](ResourceAccessSettings.md) 控制沙盒化程序如何访问资源。部分规则会区分发起请求的程序是从沙盒外还是沙盒内加载可执行文件。

下表两列均指在 Sandboxie 中运行的程序。“是”表示规则可以适用于可执行文件位于该位置的程序，并不表示允许访问。程序选择条件、[规则优先级](../PlusContent/RuleSpecificity.md)以及其他安全限制仍会影响最终结果。

| 设置            | 可执行文件位于沙盒外 | 可执行文件位于沙盒内 |
|-----------------|---------|--------|
|[关闭 Clsid](ClosedClsid.md)        | 是     | 是    |
|[封闭文件路径](ClosedFilePath.md)   | 是     | 是    |
|[封禁 IPC 路径](ClosedIpcPath.md)    | 是     | 是    |
|[封禁注册表项路径](ClosedKeyPath.md)    | 是     | 是    |
|[封禁 RT](ClosedRT.md)   | 是     | 是    |
|[不重命名窗口类](NoRenameWinClass.md) |  是    |    是    |
|[标准文件路径](NormalFilePath.md)    | 是     | 是      |
|[标准 IPC 路径](NormalIpcPath.md)     | 是     | 是      |
|[标准注册表路径](NormalKeyPath.md)     | 是     | 是      |
|[开放 Clsid](OpenClsid.md)        | 是     | 是    |
|[开放配置路径](OpenConfPath.md)        | 是     | 是    |
|[开放文件路径](OpenFilePath.md)     | 是     | 默认不适用       |
|[开放 IPC 路径](OpenIpcPath.md)      | 是     | 是      |
|[开放注册表路径](OpenKeyPath.md)      | 是     | 默认不适用       |
|[开放管道路径](OpenPipePath.md)     | 是     | 是    |
|[开放窗口类](OpenWinClass.md)     | 是     | 是    |
|[只读文件路径](ReadFilePath.md)     | 是  | 是   |
|[读取 IPC 路径](ReadIpcPath.md)       | 是     | 是   |
|[读取注册表项路径](ReadKeyPath.md)       | 是  | 是   |
|[只写文件路径](WriteFilePath.md)   | 是      | 是     |
|[写入注册表项路径](WriteKeyPath.md)     | 是      | 是     |

表中的“默认不适用”指普通 `OpenFilePath` 和 `OpenKeyPath` 规则默认不适用于从沙盒内加载可执行文件的程序。设置 `DontOpenForBoxed=n` 或使用[应用隔间](NoSecurityIsolation.md)模式均可取消这一限制。`OpenPipePath` 和 `OpenConfPath` 不受此限制。

此处的 `ReadIpcPath` 指其 `$:...` 目标进程规则。这些规则允许对另一个进程进行有限的读取访问，所用策略独立于常规命名 IPC 对象的匹配；详见[读取 IPC 路径](ReadIpcPath.md)。

启用 `AlwaysCloseForBoxed` 时（应用隔间模式之外的默认行为），`ClosedFilePath`、`ClosedKeyPath` 或 `ClosedIpcPath` 中的排除式程序选择条件（如 `!program.exe`）不会豁免从沙盒内加载可执行文件的程序。设置 `AlwaysCloseForBoxed=n` 可恢复正常的程序匹配行为。对于带排除式程序选择条件的 `ClosedIpcPath` 条目，Sandboxie 自身组件另有豁免。
