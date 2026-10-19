# AppContainer 令牌兼容性 {#appcontainer-token-compatibility}

Sandboxie 在多个独立阶段处理 AppContainer 相关请求：配置文件和令牌 API 调用、进程创建属性、调用者提供的子进程令牌，以及后续的沙盒主令牌处理。在 Windows 创建子进程前修改令牌参数，与禁用 Sandboxie 随后的主令牌替换，是不同的操作。这些高级设置分别用于特定的兼容性处理，并不是一个统一的 AppContainer 开关。

在标准沙盒中，Sandboxie 会替代部分 AppContainer 创建行为以兼顾兼容性，不会原样保留 Windows 的原生 AppContainer 模型。真正的 Windows AppContainer 令牌、Sandboxie 用于兼容的替代令牌，以及配置文件 API 返回的形似 AppContainer 的 SID，是不同的对象。

## 标准沙盒与应用隔间 {#standard-sandbox-and-application-compartment}

下表适用于 Sandboxie Plus 1.18.8 / Classic 5.73.8 及后续版本。

| 行为 | 标准沙盒 | 应用隔间 |
| --- | --- | --- |
| 正常的 Sandboxie 受限主令牌替换 | 通常启用 | 跳过 |
| `CreateAppContainerToken` 兼容性钩子 | 在 Windows 8.1 及更高版本中安装 | 不安装 |
| 直接调用 `NtCreateLowBoxToken` 的兼容性钩子 | 在 Windows 8.1 及更高版本中安装 | 不安装 |
| AppContainer 相关进程创建属性 | 默认不传递；`FakeAppContainerToken=n` 时传递 | 此分支始终传递 |
| `CreateAppContainerProfile` 兼容性 SID 钩子 | 在 Windows 8 及更高版本中安装 | 不安装 |
| `DropAppContainerToken` 运行时默认值 | `y` | `n` |
| `UnRestrictAppContainerToken` 替代令牌路径 | 通过已安装的钩子生效 | 不通过该钩子使用 |

应用隔间允许 Windows 原生 AppContainer 处理更直接地参与，同时跳过 Sandboxie 正常的受限主令牌替换。其他沙盒策略仍然独立生效。参见[应用隔间](../PlusContent/compartment-mode.md)、[无安全隔离](NoSecurityIsolation.md)和[访问令牌隔离](AccessTokenIsolation.md)。

## AppContainer API 兼容性 {#appcontainer-api-compatibility}

在 Windows 8.1 及更高版本的标准沙盒中，Sandboxie 会挂钩 `CreateAppContainerToken`。通常，它会打开当前进程的令牌，并使用 `DISABLE_MAX_PRIVILEGE` 和 `CreateRestrictedToken` 禁用选定的组，返回受限的兼容性替代令牌。自 1.18.8 起，默认会将四个常用组排除在禁用列表之外；参见 [KeepBroadGroupsInAppContainerToken](#keepbroadgroupsinappcontainertoken)。所得令牌并不是真正包含所请求 AppContainer SID 和能力的 AppContainer 令牌。

标准沙盒的进程创建兼容性钩子还可以不传递 `PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES` 和 `PROC_THREAD_ATTRIBUTE_ALL_APPLICATION_PACKAGES_POLICY`，同时向调用者返回成功。自 1.18.8 起，此行为由 [FakeAppContainerToken](#fakeappcontainertoken) 控制。直接调用 `NtCreateLowBoxToken` 则由独立的 [NeutralizeLowBoxToken](#neutralizelowboxtoken) 设置控制。

Sandboxie 在标准沙盒中的 `CreateAppContainerProfile` 钩子会返回一个本地分配、形如 `S-1-15-2-...` 的 SID。它不会调用 Windows 原生的配置文件创建函数，也不会创建正常的 AppContainer 配置文件。当前使用的固定兼容性 SID 并不根据请求的配置文件名称或能力生成。

Sandboxie 可以另外通过 `TokenAppContainerSid` 检测进程令牌是否是真正的 AppContainer 令牌。这种检测并不意味着标准沙盒的替代令牌或配置文件钩子合成的 SID 具有原生 AppContainer 的隔离语义。

<div id="fakeappcontainertoken-historical-setting"></div>

### FakeAppContainerToken {#fakeappcontainertoken}

```ini
FakeAppContainerToken=program.exe,n
```

自 1.18.8 起，标准沙盒的进程属性处理路径重新读取此项按映像匹配的设置。运行时默认值为 `y`，表示不传递上述两个属性。设为 `n` 时，Sandboxie 会将它们转交给 Windows，允许原生 AppContainer 进程属性参与子进程创建。应用隔间始终在此分支中传递这些属性，不读取此设置。

此设置控制的是进程创建属性，不控制独立的配置文件 SID 钩子、`CreateAppContainerToken` 替代处理或直接 LowBox 令牌钩子。设为 `n` 不会禁用所有 AppContainer 兼容性处理，也不保证每个子进程都使用原生 AppContainer 令牌运行。

在 1.18.6 和 1.18.7 中，此路径的配置检查被注释掉，因此修改设置值不会影响属性是否传递。元数据记录的历史引入版本为 1.8.2；这与该设置在 1.18.8 中重新生效是两回事。

## 创建子进程时由调用者提供的令牌 {#caller-supplied-tokens-during-child-creation}

`DropAppContainerToken` 和[丢弃子进程令牌](DropChildProcessToken.md)作用于调用进程在创建子进程时提供的令牌。两者都不会从已有令牌中移除 AppContainer SID，也不会直接禁用 Sandboxie 随后的主令牌替换。

### DropAppContainerToken {#dropappcontainertoken}

```ini
DropAppContainerToken=browser.exe,n
```

此设置生效且传给 `CreateProcessInternalW` 的 `hToken` 是 AppContainer 令牌时，Sandboxie 会清除此令牌参数（`hToken = NULL`），并在跟踪记录中输出 **Dropped AppContainer Token**。随后创建子进程时将不再使用调用者提供的这个令牌参数；已有令牌对象不会被改写。

标准沙盒中的运行时默认值为 `y`，应用隔间中为 `n`。此设置按映像匹配：示例中的 `browser.exe` 选择的是**发起子进程创建请求的沙盒内调用进程**，不是子进程的可执行文件。设为 `n` 时，此项设置不会丢弃 `browser.exe` 提供的 AppContainer 令牌。

在标准沙盒中，子进程创建后，驱动通常仍会对其执行 `Token_ReplacePrimary()`。丢弃调用者提供的 AppContainer 令牌与应用 Sandboxie 正常的受限主令牌，是两个独立阶段。

在应用隔间中，原生 AppContainer 处理可以更直接地参与，而正常的受限主令牌替换会被跳过。因此，显式设置 `DropAppContainerToken=program.exe,y` 可能移除原本会作用于子进程的 Windows 令牌限制。这会降低令牌隔离程度，但不会自动提升权限。

### UnRestrictAppContainerToken {#unrestrictappcontainertoken}

```ini
UnRestrictAppContainerToken=program.exe,y
```

此项按映像匹配的设置控制标准沙盒的 `CreateAppContainerToken` 替代令牌路径。自 1.18.8 起，所有映像的运行时默认值均为 `n`，包括 `msedge.exe`，因此 Sandboxie 会创建受限的兼容性替代令牌。设为 `y` 时，Sandboxie 改为调用 `NtDuplicateToken`，将传入该钩子的 `TokenHandle` 复制为主令牌并返回。传入的令牌本身可能已经受限；`y` 不保证得到完整或不受限的用户令牌。与 Sandboxie 的受限替代路径相比，它会保留更多传入令牌的属性。

在 1.18.6 和 1.18.7 中，出于兼容性考虑，`msedge.exe` 的运行时默认值为 `y`。1.18.8 对常用组的处理调整使受限替代令牌重新适用于 Edge，因此移除了这项默认例外。显式设置 `UnRestrictAppContainerToken=msedge.exe,y` 仍会选择令牌复制路径。应用隔间不安装此替代钩子，因此此设置不是该模式的常规控制项。

### KeepBroadGroupsInAppContainerToken {#keepbroadgroupsinappcontainertoken}

```ini
KeepBroadGroupsInAppContainerToken=program.exe,n
```

此设置自 1.18.8 引入，按映像匹配，默认值为 `y`。它在标准沙盒的 `CreateAppContainerToken` 钩子构造受限替代令牌时生效（`UnRestrictAppContainerToken=n`）。Sandboxie 会将 Everyone、Users、Authenticated Users 和 INTERACTIVE 排除在待禁用组列表之外。这些组保留源令牌中的既有状态；此设置不会重新启用源令牌中已经禁用的组。其他组仍会传入限制操作，`DISABLE_MAX_PRIVILEGE` 也仍然生效。

设为 `n` 会恢复旧行为，将查询到的所有组都传给 `CreateRestrictedToken` 以禁用它们。旧行为可能导致子进程无法打开 `\KnownDlls` 等资源。此选项用于兼容性排查和调试，不建议普遍修改默认值。它不控制 `UnRestrictAppContainerToken=y` 所选择的令牌复制路径，也不控制独立的直接 LowBox 令牌钩子。

### NeutralizeLowBoxToken {#neutralizelowboxtoken}

```ini
NeutralizeLowBoxToken=program.exe,n
```

自 1.18.8 起，Sandboxie 还会在 Windows 8.1 及更高版本的标准沙盒中挂钩直接的 `NtCreateLowBoxToken` 调用。此设置按映像匹配，默认值为 `y`：钩子会将 `ExistingTokenHandle` 复制为主令牌并返回，不会创建请求中指定包 SID 和能力的原生 LowBox 令牌。传入的令牌本身可能已经受限。

设为 `n` 时，钩子会将原始调用及其参数转交给 Windows，Windows 的访问检查和失败条件仍然适用。应用隔间不安装此钩子。此设置与 `UnRestrictAppContainerToken`、`KeepBroadGroupsInAppContainerToken` 以及进程属性是否传递相互独立；修改其中一项不会同时配置其他项。

### 其他子进程令牌兼容性路径 {#other-child-token-compatibility-paths}

`DropChildProcessToken` 默认值为 `n`，可以为选定的调用进程清除其提供的任意子进程令牌。对于分类为 Acrobat Reader 或插件容器的映像，同样的清除行为已在代码中固定启用。独立的 Firefox 分支可在子进程命令行包含 `-sandboxingKind` 时清除令牌。这些是不同的处理路径；旧的 Flash 专用条件已被注释掉。该设置的作用范围见[丢弃子进程令牌](DropChildProcessToken.md)。

代码仍会为旧的 Chromium/Edge 兼容性分支查询 `DeprecatedTokenHacks`，但仅限应用隔间之外且未启用 `OriginalToken` 的情况。启用时，如果调用进程被分类为 Chrome，且子进程命令行包含 `--service-sandbox-type`，该分支可以清除调用者提供的子进程令牌。它不控制 `FakeAppContainerToken`，也不是所有历史令牌变通处理的统一开关。

## 已有沙盒与 AppContainer 权限 {#existing-boxes-and-appcontainer-permissions}

1.18.8 在沙盒根目录和沙盒内对象使用的安全描述符中加入了 AppContainer 访问控制项（ACE），帮助原生 AppContainer 子进程访问所需的沙盒资源。已有沙盒可能仍保留旧的文件系统自由访问控制列表（DACL），因此更新新对象使用的描述符本身，并不能修复每个已有沙盒。

对于受影响的已有沙盒，1.18.8 新增了以下命令。应在 Sandboxie 安装目录中、以能够修改沙盒文件夹 DACL 的权限运行；管理员可以执行此修复：

```cmd
KmdUtil.exe fixboxdacls
```

工具会枚举对当前调用账户和会话启用的沙盒，解析已有的文件根目录；如果检查发现缺少相应授权，就会为 `ALL APPLICATION PACKAGES`（`S-1-15-2-1`）和 `ALL RESTRICTED APPLICATION PACKAGES`（`S-1-15-2-2`）添加可继承的完全访问条目。已禁用或不允许该账户使用的沙盒不会被处理。此命令不局限于某个选中的沙盒。1.18.8 中，原有的 `fixdacls` 命令也会调用这项沙盒文件夹修复。

此操作会修改已保存的文件系统权限，并非只读诊断。枚举沙盒和查询路径需要驱动可用。无法解析或不存在的根目录会被跳过，自定义权限和继承设置也可能影响结果。不能假定运行命令后，每个已有子对象都能被 AppContainer 访问，也不能假定不可用的镜像沙盒根目录已得到修复。使用前应核对自定义 ACL 的要求。此修复与上述令牌设置相互独立。

## 安全性与配置 {#security-and-configuration}

这些设置会改变特定的 Windows 令牌选择，可能显著影响访问检查。它们本身不会禁用文件或注册表虚拟化、网络限制、IPC 策略或沙盒归属，也不会授予管理员权限。[原始令牌](OriginalToken.md)和[高级令牌设置](AdvancedTokenSettings.md)介绍了令牌处理后续阶段中的独立选项。

目前未找到 SandMan 为本页令牌设置提供的专用控件。应仅针对具体的兼容性或调试需要，通过 [Sandboxie.ini](SandboxieIni.md) 配置。可选的[程序名称前缀](ProgramNamePrefix.md)选择的是发起相关 API 调用的沙盒内进程，不是其子进程的可执行文件。

这些路径在 SbieDll 初始化、AppContainer API 挂钩或子进程创建时选定。更改配置不会重新构建已分配给运行中进程的令牌。修改后应重启受影响的沙盒进程树；通常无需重启 Windows、服务或驱动。

当前设置元数据记录的引入版本为：`DropAppContainerToken` 是 1.7.2，`FakeAppContainerToken` 是 1.8.2，`UnRestrictAppContainerToken` 是 1.8.4，`DropChildProcessToken` 是 1.15.6。重新启用 `FakeAppContainerToken` 检查、统一 `UnRestrictAppContainerToken=n` 默认值，以及新增 `KeepBroadGroupsInAppContainerToken`、`NeutralizeLowBoxToken` 和 `fixboxdacls` 命令，均属于 1.18.8 的变化。

## 相关页面 {#related-pages}

- [丢弃子进程令牌](DropChildProcessToken.md)
- [原始令牌](OriginalToken.md)
- [高级令牌设置](AdvancedTokenSettings.md)
- [无安全隔离](NoSecurityIsolation.md)
- [应用隔间](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
