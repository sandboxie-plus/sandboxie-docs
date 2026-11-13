# 对象名称查找兼容性 {#object-lookup-compatibility}

`UseDriverObjLookup` 与 `UseObjectNameForKeys` 是两项高级兼容性设置，用于控制 Sandboxie 如何从既有对象与注册表项句柄取得名称。两者都默认禁用。它们改变的是 Sandboxie 内部的名称解析，而不是那些授予或拒绝对文件、注册表项或命名对象访问的规则。

## Sandboxie 中的对象名称查找 {#object-name-lookup-in-sandboxie}

某些 Sandboxie 路径处理操作需要取得与已打开句柄关联的名称。Sandboxie 内部的 `Obj_GetObjectName` 辅助函数通常通过 `NtQueryObject` 向 Windows 请求 `ObjectNameInformation`。其他内部的文件、IPC 以及选定的安全对象路径也使用这一辅助函数。这与 Sandboxie 为应用程序自身的 `NtQueryObject` 调用所设的钩子不同：启用 `UseDriverObjLookup` 并不会把每一个此类调用都改由驱动程序处理。

## UseDriverObjLookup {#usedriverobjlookup}

在标准沙盒中，`UseDriverObjLookup=y` 会让 Sandboxie 内部的对象名称辅助函数请求 Sandboxie 驱动程序来解析句柄名称，而不是使用它常规的用户态 `NtQueryObject` 查找：

```ini
[DefaultBox]
UseDriverObjLookup=y
```

这是针对特定句柄与 I/O 状况的按需变通手段——在那些状况下，对象名称查询可能挂起，典型情形是带有待处理读取的同步管道句柄。它不是通用的性能选项，也不保证能解决所有对象查找问题。驱动程序使用自己的对象名称路径解析所提供句柄的名称，并对某些文件对象做特殊处理。如果该查找失败，辅助函数会返回失败，不会退回原生的 `NtQueryObject` 路径重试。

即使配置了 `UseDriverObjLookup=y`，应用隔间也不会启用这条由驱动程序协助的辅助函数路径。其 `Obj_GetObjectName` 调用继续使用原生路径。

## UseObjectNameForKeys {#useobjectnameforkeys}

当注册表操作提供 `RootDirectory` 项句柄与一个相对名称时，Sandboxie 会在拼接相对部分之前先取得根项的完整名称。默认情况下，`Key_GetName` 通过 `NtQueryKey(KeyNameInformation)` 取得该根名称。`UseObjectNameForKeys=y` 则改为把这次根句柄查找交给 `Obj_GetObjectName`：

```ini
[DefaultBox]
UseObjectNameForKeys=y
```

该选项不会替换所有 `NtQueryKey` 调用，也不改变注册表访问规则。当某个操作没有根句柄时，这一选择不参与其路径的构造。

保留该替代方案是为了兼容性：早先基于 `NtQueryObject` 的根名称查找已被回退，它曾解决 `NtQueryKey` 对某些项可能失败的情况，但在 Windows 10 版本 1803 及更早版本上引发了问题。这属于历史背景，并不意味着今天应在某个特定的 Windows 版本上启用它。

## 两项设置如何相互影响 {#how-the-settings-interact}

| `UseObjectNameForKeys` | `UseDriverObjLookup` | 注册表根句柄名称查找 |
| --- | --- | --- |
| `n` | 任意取值 | `NtQueryKey(KeyNameInformation)`。驱动程序设置仍可能影响其他内部 `Obj_GetObjectName` 调用方。 |
| `y` | `n` | `Obj_GetObjectName`，使用原生 `NtQueryObject(ObjectNameInformation)`。 |
| `y` | `y`，标准沙盒 | `Obj_GetObjectName`，使用由驱动程序协助的查找。 |
| `y` | `y`，应用隔间 | `Obj_GetObjectName`，使用原生 `NtQueryObject`；该模式下由驱动程序协助的辅助函数路径仍处于禁用状态。 |

两项设置互不要求对方先启用。所选查找失败时，失败结果会返回给调用方，而不会自动切换到另一种查找方式。

## 应用更改 {#applying-changes}

这些是沙盒范围的“是/否”设置，既不是按可执行文件限定的规则，也不是进程组规则。有效值可以来自沙盒自身、`[GlobalSettings]` 或某个适用的已启用模板。Sandboxie 会在沙盒化进程中初始化其 DLL 时读取各项取值，因此更改后请重启受影响的沙盒化进程。新进程读取更改后的配置，通常不需要重启驱动程序、服务或 Windows。

SandMan 没有为这两项设置提供专用复选框，也没有把它们列入内置的高级选项建议。它的 **沙盒选项 > 高级选项 > 杂项 > 添加选项** 字段接受手动输入的选项名；上面的示例同时给出了直接写 `Sandboxie.ini` 的形式。

## 版本历史 {#version-history}

- `UseObjectNameForKeys` 在 Sandboxie Plus 0.8.8 / Classic 5.50.8 中作为按需启用的兼容性设置加入。
- `UseDriverObjLookup` 针对罕见的对象名称查询挂起情形，在 Sandboxie Plus 1.10.3 / Classic 5.65.3 中加入。

## 相关页面 {#related-pages}

- [Sandboxie Ini](SandboxieIni.md) 说明了沙盒配置与继承。
- [注册表根路径](KeyRootPath.md) 描述了沙盒注册表配置单元挂载在哪里；它并不选择根句柄的查找方式。
- [Nt 命名空间隔离](NtNamespaceIsolation.md) 关注的是命名对象目录的隔离，而不是既有句柄名称的查找。
