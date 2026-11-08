# 进程组 {#process-group}

`ProcessGroup` 定义一组可重用的命名可执行映像选择器。接受进程限定选择器的设置可以引用该组，而不必重复列出每个可执行文件名，前提是对应的运行时解析器支持进程组。

例如：

```ini
[DefaultBox]
ProcessGroup=<Browsers>,firefox.exe,chrome.exe
```

仅凭该定义本身不会授予或拒绝访问、不会将程序强制放入沙盒、不会启动或停止进程、不会创建 Windows 进程组或作业对象，也不会以其他方式应用策略。必须有另一项设置把 `<Browsers>` 用作其进程选择器，该组才会影响运行时行为。

Sandboxie 驱动程序侧与 SbieDll 用户态的配置匹配器都会为使用这些匹配器的设置解析进程组。这并不意味着每项 Sandboxie 设置都接受进程组；请查阅将要引用该组的设置的语法。

## 语法 {#syntax}

一般形式为：

```ini
ProcessGroup=<GroupName>,program1.exe,program2.exe
```

尖括号是组选择器的一部分。当前的运行时匹配会在选择器以 `<` 开头时识别组引用；像 `Browsers` 这样的裸名称会被视为普通映像选择器，而不是名为 `<Browsers>` 的 `ProcessGroup`。

组名和普通的可执行映像成员匹配均不区分大小写。请使用可执行映像名（如 `firefox.exe`），不要使用进程 ID 或可执行文件的完整路径。

某些通用配置匹配器可以解释通配符映像模式，但并非每条活跃的进程组匹配路径都能做到。对于必须在各使用方之间保持一致行为的配置，请使用字面可执行映像名和嵌套组引用，而不要使用通配符成员。

取反属于使用组的规则中的进程选择器，而不属于 `ProcessGroup` 定义。在某设置支持取反的进程选择器时：

- `<Browsers>` 匹配组内成员；
- `!<Browsers>` 匹配不属于该组的进程。

不要把组定义为 `ProcessGroup=!<Browsers>,...`。

## 在规则中使用组 {#using-a-group-in-rules}

下面这个资源访问示例把文件规则应用于 `<Browsers>` 的成员：

```ini
[DefaultBox]
ProcessGroup=<Browsers>,firefox.exe,chrome.exe
OpenFilePath=<Browsers>,C:\Shared\*
```

`OpenFilePath` 是一个已验证的使用方，但不是唯一的一个。内置模板也在文件、注册表、IPC 和窗口类规则中使用进程组。

在使用 Sandboxie 通用进程匹配层级的使用方中，直接的可执行文件匹配或组匹配比取反选择器具有更高的进程匹配优先级，而取反选择器又比全局或 `*` 选择器更强。这是限定规则之间的优先级关系。`ProcessGroup` 内部成员的顺序不会使某个成员优先于另一个成员。

## 嵌套组 {#nested-groups}

一个进程组可以包含另一个进程组：

```ini
[DefaultBox]
ProcessGroup=<Browsers>,firefox.exe,chrome.exe
ProcessGroup=<WebApps>,<Browsers>,electron-app.exe
```

因此 `<WebApps>` 可以匹配 `firefox.exe`、`chrome.exe` 和 `electron-app.exe`。

在当前运行时中，嵌套展开的深度被有意限制。对循环定义或过深定义的展开是有界的，不会无限递归，但这类定义并不是有用的配置，不应依赖。SandMan 允许把已有组选为成员，且目前不阻止直接或间接循环。

## 重复与继承的定义 {#repeated-and-inherited-definitions}

同名的重复定义会贡献额外成员：

```ini
ProcessGroup=<Browsers>,firefox.exe
ProcessGroup=<Browsers>,chrome.exe
```

生效的组匹配任一可执行文件。当同名定义来自沙盒、`[GlobalSettings]` 或已启用的模板时，运行时行为相同：适用的定义都会贡献成员，而不是仅按来源选中某一个定义。因此：

- `[GlobalSettings]` 可以通过常规的全局配置查找为沙盒提供组；
- 已启用的模板可以贡献组；
- 同名的沙盒本地定义不会在运行时移除继承而来的成员；
- 多个已启用模板中的同名定义同样会贡献成员。

当前 SandMan 中的说明文字称，为沙盒定义的组会覆盖模板中定义的组。该表述并未反映当前运行时匹配器的行为——匹配器会检查所有适用的同名定义。当意外的合并成员关系会造成歧义时，请避免在不同配置来源之间重用同一个组名。

## 在 SandMan 中管理组 {#managing-groups-in-sandman}

打开**沙盒选项 > 程序组**。该页面提供：

- **添加组**；
- **添加程序**；
- **移除**；
- **显示模板**。

**添加组**会把输入的名称连同尖括号一起存储。**添加程序**可以选择一个已有的组（显示为**组：GroupName**），从而创建嵌套组引用。

**显示模板**会把来自 `[GlobalSettings]` 和该沙盒已启用模板的组与本地组一起显示。在此视图中，源自模板的条目是只读的；该页面只写入沙盒本地的 `ProcessGroup` 条目。

在此页面中重命名本地组会改变其定义名称，但这不是一次全局重构操作。其他进程组或配置规则中对旧名称的引用不会被自动改写。同样，移除组会删除所选定义，但不一定删除引用它的设置。悬空的组选择器无法通过已删除的定义进行匹配，尽管另一个同名的适用定义仍可能提供成员。

## 界面管理的组 {#ui-managed-groups}

某些更高级的 SandMan 功能会在内部维护 `ProcessGroup` 条目。目前的例子包括 Internet Access 和 Start/Run 限制使用的程序列表，其组包括 `<InternetAccess>`、`<StartRunAccess>` 和 `<StartRunAccessDisabled>`。

因此，手动编辑或删除这些条目可能会改变这些控件所代表的含义。这些名称是普通的运行时进程组；它们的意义来自引用它们的规则和 SandMan 功能。

## ProcessGroup 与 BoxGrouping {#processgroup-vs-boxgrouping}

`ProcessGroup` 和 [`BoxGrouping`](BoxGrouping.md) 的用途互不相关。

| 设置 | 包含内容 | 范围与效果 |
| ------- | -------- | ---------------- |
| `ProcessGroup` | 可执行映像选择器和嵌套进程组 | 用于运行时规则匹配的沙盒、全局或模板配置；以 `<GroupName>` 引用 |
| `BoxGrouping` | 沙盒和可视子组 | 每用户的 SandMan 层级和排序元数据；无运行时策略效果 |

把两个沙盒放进同一个 `BoxGrouping` 分支，不会共享它们的 `ProcessGroup` 定义，也不会使这些沙盒中的进程成为同一个进程组的成员。

## 应用更改 {#applying-changes}

保存 `ProcessGroup` 更改会更新配置，但新成员关系何时变得可观察取决于引用该组的设置。动态求值的检查可以在后续操作中使用更新后的定义，而在进程初始化期间构建或缓存有效规则的使用方则可能需要重启受影响的沙盒化进程。仅为了更改进程组，通常不需要重启 SandMan、服务或驱动程序。

## Sandboxie Plus 与 Classic {#sandboxie-plus-and-classic}

`ProcessGroup` 是一项共享的运行时配置机制，并非 Sandboxie Plus 独有的功能。SandMan 提供了当前的**程序组**页面，Sandboxie Control Classic 也包含程序组的配置和选择支持。两者的界面并不相同，但兼容的 INI 定义由共享的运行时使用。

## 版本历史 {#version-history}

当前的设置元数据没有记录 `ProcessGroup` 的 `AddedVersion`，因此这里无法确定其确切的引入版本。程序组处理早于 Sandboxie Plus 0.4.3 / Classic 5.43.7；该版本修复的是 SandMan 界面中的解析问题，而不是引入该运行时设置。后来的 SandMan 版本还修复了更多程序组界面问题。

## 相关页面 {#related-pages}

- [Box Grouping](BoxGrouping.md) — 在 SandMan 界面中组织沙盒
- [Sandboxie Ini](SandboxieIni.md) — 说明 Sandboxie 配置文件的节与编辑方法
