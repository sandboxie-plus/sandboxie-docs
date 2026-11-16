# 模板架构 {#template-architecture}

Sandboxie 模板主要是一组可复用的 [Sandboxie 配置](SandboxieIni.md)条目。选中某个模板会使其中的普通设置成为有效配置的一部分；选中操作不会把这些条目永久复制到沙盒的显式配置中。模板的呈现数据与发现数据独立于 Sandboxie 在运行时应用的规则。

例如：

```ini
[Template_Example]
Tmpl.Title=Example
Tmpl.Class=Misc
OpenFilePath=C:\Example\*
OpenIpcPath=\RPC Control\Example

[DefaultBox]
Template=Example
```

在这里，`OpenFilePath` 与 `OpenIpcPath` 为 `DefaultBox` 提供配置。`Tmpl.*` 条目用于描述模板本身；它们不是沙盒访问规则。

## 官方模板与本地模板 {#official-and-local-templates}

官方模板随 Sandboxie 安装包以 `Templates.ini` 的形式提供。可以把该文件作为现有定义的参考，但自定义模板应放入 [`Sandboxie.ini`](SandboxieIni.md)，而不要修改这个随附文件。

官方模板的节通常使用 `[Template_Name]`。用户创建的模板按惯例使用 `[Template_Local_Name]`，这样既能在界面中把它们区分开来，也能避免与将来新增的官方名称冲突：

```ini
[Template_Local_ExampleSoft]
Tmpl.Title=ExampleSoft
Tmpl.Class=Local
OpenWinClass=ExampleSoft_WindowClass
OpenIpcPath=*\BaseNamedObjects*\ExampleSoft_*
```

本地模板可以像官方模板一样手动启用。`Template_Local_` 只是一种命名与呈现约定，并不是独立的运行时继承机制。[应用程序设置](ApplicationsSettings.md#local)页面也介绍了旧的本地模板界面。

## 选择模板 {#selecting-templates}

在 `Template=` 后面写上模板名称，即可为某个沙盒启用该模板：

```ini
[DefaultBox]
Template=Example
```

一个节中可以包含多个 `Template=` 条目。Sandboxie 会逐个处理选中的模板，并把其中的设置合并到该节的有效配置中。模板也可以全局选中：

```ini
[GlobalSettings]
Template=Example
```

全局选中会把设置贡献到全局有效配置中。它不会在每个沙盒节里另外生成一份模板定义的永久副本。

`TemplateReject=Name` 应放在 `[GlobalSettings]` 中。它记录兼容性模板的选择状态，使被检测到的模板被视为已拒绝/已配置，而不再停留在待推荐的候选状态。单个沙盒节中的同名值不用于此目的。它不会从显式选中的 `Template=Name` 中扣除设置；对该选择而言，常规的模板合并仍然生效。

## 模板如何合并 {#how-templates-are-merged}

在加载配置时，Sandboxie 先处理 `GlobalSettings` 中选中的模板，然后把 `[DefaultTemplates]` 应用到全局有效配置，最后处理各沙盒选中的模板。被选中模板中的普通设置会合并到目标的有效配置中。`Tmpl.*` 元数据在这一运行时合并过程中会被跳过。

显式条目与来自模板的条目可以在有效配置中共存。Sandboxie 会记录哪些条目来自模板，而直接条目通常排在随后合并进来的条目之前。相互竞争的条目最终如何生效，仍取决于使用它们的子系统；配置来源的顺序并不是通用的优先级规则。资源规则冲突请参见 [规则特异性](../PlusContent/RuleSpecificity.md)。

## 默认模板 {#default-templates}

随附的 `Templates.ini` 中的 `[DefaultTemplates]` 列出了会自动合并到全局有效配置中的内置模板。用户无需为某个沙盒单独选中这些模板，即可获得它们提供的基线设置。当前列表包括 `RpcPortBindings`、`SpecialImages`、`COM`、`WindowsExplorer`、`ThirdPartyIsolation`、`BlockSoftwareUpdaters`、`BlockWinRM`、`OpenWinInetCache`、`CredentialUIBroker` 和 `MSI_Lite`。随附列表可能在不同版本之间变化；默认模板并非不可更改的策略。

这种自动合并与为特定沙盒启用某个可选的应用程序兼容性模板并不相同。

## 模板变量与内部节 {#template-variables-and-internal-sections}

`[TemplateSettings]` 提供共享的 `%Tmpl.*%` 变量定义以及相关的元数据基础设施。模板可以使用这些变量，具体见 [可展开变量](ExpandableVariables.md#template-variables)。`[TemplateSettings]` 并不是用 `Template=TemplateSettings` 选中的兼容性模板；自定义模板无需复制或编辑它。

其他以 `Template` 开头的节同样不是普通的应用程序模板。`TemplateDefaultPaths`、`TemplateSModPaths`、`TemplatePModPaths` 与 `TemplateAppCPaths` 通过各自独立的加载路径，为运行时子系统提供内置路径规则。不要通过应用程序模板列表启用它们，也不要假定 `Template=Name` 能控制它们。

## 模板元数据 {#template-metadata}

以 `Tmpl.` 开头的条目用于描述模板，或帮助发现该模板何时可能有用。当模板规则合并进运行时配置时，这些条目会被跳过。

| 条目 | 用途 |
| --- | --- |
| `Tmpl.Title` | 显示标题 |
| `Tmpl.Class` | 界面类别 |
| `Tmpl.Url` | 相关软件或厂商的 URL |
| `Tmpl.Comment` | 描述或注释 |
| `Tmpl.Hide` | 在常规呈现中隐藏模板 |
| `Tmpl.Entry` | 专门的兼容性或已知冲突条目元数据 |
| `Tmpl.Version` | 模板/配置元数据版本 |
| `Tmpl.Scan` | 兼容性发现模式 |
| `Tmpl.Scan*` | 用于检测模板是否可能适用的证据 |
| `Tmpl.ScanScript` | SandMan 现代检查器中的脚本化检测 |

这些字段大多由模板呈现或兼容性发现代码使用，驱动程序并不把它们用作访问规则。

## 模板发现 {#template-discovery}

模板发现决定 Sandboxie 或 SandMan 是否应推荐某个兼容性模板。它本身并不强制执行该模板的沙盒规则。只有当模板被选中，或通过默认模板机制被应用之后，这些规则才会进入有效配置。

`Tmpl.Scan` 用于选择一种或多种证据模式：

- `i` 使用 `OpenIpcPath` 与 `Tmpl.ScanIpc` 证据检查 IPC 对象。除非选中了 `i`，否则仅有 `OpenIpcPath` 条目并不意味着会进行扫描。
- `w` 使用 `OpenWinClass` 与 `Tmpl.ScanWinClass` 证据检查已知的窗口类。
- `s` 检查软件存在性证据，例如 `Tmpl.ScanService`、`Tmpl.ScanProduct`、`Tmpl.ScanKey` 与 `Tmpl.ScanFile`。这类证据可以指向服务、已安装的产品、注册表项或文件；`s` 并不限于服务。

当存在扫描脚本时，SandMan 的现代兼容性检查器会先求值 `Tmpl.ScanScript`。较旧的 C++ 回退扫描器则改用 `Tmpl.Scan` 的证据字段，不会执行该脚本路径。现代检查器的自动扫描会跳过 `Local_` 模板；本地模板仍可供手动选择。

## 阻止软件更新程序 {#software-updater-blocking}

随附的 `[DefaultTemplates]` 列表包含 `Template=BlockSoftwareUpdaters`。它的 `[Template_BlockSoftwareUpdaters]` 节会向有效配置提供持续维护的 `SoftwareUpdater` 模式。该默认模板已经包含在内；用户无需把它作为可选的应用程序模板选中，即可获得这些定义。

这些规则由起始应用程序映像，以及随后的更新程序可执行文件或路径模式组成：

```ini
SoftwareUpdater=starting_image.exe,updater_path\updater_image.exe

SoftwareUpdater=firefox.exe,*\mozilla firefox\updater.exe
SoftwareUpdater=msedge.exe,*\Microsoft\EdgeUpdate\MicrosoftEdgeUpdate.exe
```

`BlockSoftwareUpdaters` 是一个独立的运行时开关，其查询默认值为 `y`。当该开关启用且子进程匹配某条 `SoftwareUpdater` 规则时，Sandboxie 会以 `ERROR_ACCESS_DENIED` 阻止其创建，并把 **Blocked start of an updater** 报告到其监控路径。设为 `BlockSoftwareUpdaters=n` 时，该默认模板及其模式仍可能存在于有效配置中，但这一进程创建拦截机制不会强制执行它们。

`BlockSoftwareUpdaters` 于 0.5.5 引入，1.0.11 中移除，1.14.4 中重新引入。它在当前运行时中处于生效状态。该机制只涵盖匹配的更新程序进程创建；它并不保证所有软件更新、安装程序或基于网络的更新途径都会被阻止。

## SandMan 与应用更改 {#sandman-and-applying-changes}

在 SandMan 中，模板按标题和类别显示在 **沙盒选项 > 应用模板** 下。为某个沙盒启用模板，相当于选中它的配置，无需手动修改 `Template=`。

启用、禁用或编辑模板后，请重启受影响的沙盒化进程，以便在进程初始化期间缓存的设置能按照一致的方式重建。不同模板派生设置的生存期各不相同；不应假定更改模板会立即更新每一个正在运行的进程。通常不需要重启 Windows、重启驱动程序或重启服务。

## 相关页面 {#related-pages}

- [Sandboxie Ini](SandboxieIni.md)
- [应用程序设置](ApplicationsSettings.md)
- [可展开变量](ExpandableVariables.md)
- [规则特异性](../PlusContent/RuleSpecificity.md)
