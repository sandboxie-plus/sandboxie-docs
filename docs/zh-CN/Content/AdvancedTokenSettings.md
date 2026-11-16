# 高级令牌设置 {#advanced-token-settings}

本页面的设置会改变 Sandboxie 过滤或重建 Windows 访问令牌的方式。其中大多数是高级兼容性或调试选项，用于保留 Sandboxie 通常会移除或限制的属性。通常仅应在需要兼容性或专门测试时才使用这些设置。

这些设置只影响基于令牌的隔离。文件系统和注册表虚拟化、IPC 控制、网络限制、GUI 隔离以及其他独立的 Sandboxie 机制不受影响。

## 令牌处理阶段 {#token-processing-stages}

令牌处理的相关部分可以简化为如下流程：

```text
原始主令牌
    |
    v
初步过滤
    |
    |-- UnfilteredToken 可跳过此阶段
    |
    v
限制 / 重建
    |
    |-- UnrestrictedToken 可跳过此阶段
    |
    |-- 常规的现代路径会重建令牌
    |
    v
沙盒主令牌
```

初步过滤器与后续的限制或重建阶段是相互独立的。因此，*UnfilteredToken* 并不意味着令牌不受限制，*UnrestrictedToken* 也不会恢复初步过滤所移除的属性。同时启用两者比单独启用任一选项能保留更多源令牌的特征。

Sandboxie 有新令牌构造路径和历史过滤路径。当前的常规配置通常使用新的 `Token_CreateToken` 路径，因为 *SandboxieAllGroup* 的运行时默认值为启用；*UseCreateToken* 也可以选择该路径。这一区别对 *UnstrippedToken* 尤为重要，其行为在两条路径之间有所不同。

这只是令牌处理的概念性概述，并非 Sandboxie 完整的隔离模型。

## 通用语法与范围 {#common-syntax-and-scope}

本页面的所有设置都是沙盒级布尔设置：

```ini
SettingName=y
SettingName=n
```

当前的运行时查找不按可执行文件限定，因此这些设置不支持 `SettingName=program.exe,y` 这类语法。常规的 Sandboxie 配置和模板继承仍会影响沙盒实际生效的配置。

## NoUntrustedToken {#nountrustedtoken}

```ini
NoUntrustedToken=y
```

```ini
NoUntrustedToken=n
```

*NoUntrustedToken* 在设置元数据和当前运行时中的默认值均为 `n`。正常的受限沙盒令牌使用 Windows 的**不可信**完整性级别。启用 *NoUntrustedToken* 时，Sandboxie 改用**低**完整性级别。

此设置不会禁用令牌替换或限制，不会保留源完整性级别，也不会禁用安全隔离。它把沙盒令牌降低后的完整性级别从不可信改为低，其余令牌隔离步骤仍然生效。

如果启用了 *KeepTokenIntegrity*，正常的完整性降级会被跳过，不可信与低之间的选择就无关紧要了。当 [`NoSecurityIsolation=y`](NoSecurityIsolation.md) 绕过正常的主令牌替换时，此设置同样是多余的。

SandMan 在以下位置公开此设置：

**沙盒选项 > 安全选项 > 高级安全**

该复选框的标签为**使用 低完整性令牌 而不是 不受信任的完整性令牌（会降低隔离）**。

## UnfilteredToken {#unfilteredtoken}

```ini
UnfilteredToken=y
```

```ini
UnfilteredToken=n
```

*UnfilteredToken* 默认值为 `n`。它会跳过 Sandboxie 的初步令牌过滤阶段。该阶段通常会移除一组固定的敏感权限，并在配置后应用 [`DropAdminRights`](DropAdminRights.md) 过滤。

后续的限制或重建仍会发生。因此，所得的令牌仍可能收到替换后的令牌用户或被降低的完整性级别，组被转换为仅拒绝，在重建过程中丢失权限，以及被添加 Sandboxie 特定的令牌组。

简而言之，*UnfilteredToken* 跳过初步过滤阶段；后续的令牌限制或重建步骤仍可能修改令牌。当前代码在相关的模拟令牌验证和 WTS 令牌处理中也会参考此行为。

由于 *DropAdminRights* 参与初步过滤，*UnfilteredToken* 可以绕过其对管理员相关组和选定权限的初步移除。但它不会移除后续的 Sandboxie 限制。

## UnrestrictedToken {#unrestrictedtoken}

```ini
UnrestrictedToken=y
```

```ini
UnrestrictedToken=n
```

*UnrestrictedToken* 默认值为 `n`。它会跳过重量级的令牌限制或重建阶段，使 Sandboxie 复制从上一阶段收到的令牌。

该令牌可能已经受过初步过滤的修改。单独启用 *UnrestrictedToken* 不会恢复先前被移除的组、权限或其他属性。

*UnrestrictedToken* 跳过正常的重量级令牌限制阶段，但其他 Sandboxie 隔离机制仍然生效，较早的令牌过滤也可能已经修改过令牌。它不会禁用文件系统或注册表虚拟化与隔离、IPC 控制、网络限制或其他独立的沙盒机制。

## UnfilteredToken 与 UnrestrictedToken 的对比 {#unfilteredtoken-versus-unrestrictedtoken}

| 配置 | 初步过滤 | 限制/重建 |
|---|---|---|
| 正常 | 已应用 | 已应用 |
| `UnfilteredToken=y` | 跳过 | 仍然应用 |
| `UnrestrictedToken=y` | 仍然应用 | 跳过 |
| 两者均启用 | 跳过 | 跳过 |

同时使用两个选项比单独使用任一选项能保留更多源令牌的特征。这并不会完全禁用 Sandboxie，因为其他隔离层仍然是独立的。

## ReplicateToken {#replicatetoken}

```ini
ReplicateToken=y
```

```ini
ReplicateToken=n
```

*ReplicateToken* 默认值为 `n`，专门应用于新的 `Token_CreateToken` 重建路径。它会创建新令牌，同时保留源令牌的更多属性；它不是简单地复制原始令牌对象。

重建的令牌会保留或复用源令牌的用户、组、权限、令牌类型、模拟级别、身份验证 ID、过期时间、所有者、主组、默认 DACL 和令牌源。它还会避免几项正常的转换，包括 Sandboxie 或 Anonymous 令牌用户替换、组转换为仅拒绝、正常的权限削减，以及正常添加 *SandboxieAll* 组。

*ReplicateToken* 还会启用可选的设备组检索和令牌安全属性复制，无论是否显式设置 `CopyDeviceGroups=n` 或 `CopyTokenAttributes=n`。这两项可选操作都不保证能成功保留；它们各自的行为和限制参见后文相应小节。

除非同时启用 *UnfilteredToken*，传入此阶段的源令牌可能已经受过初步过滤。因此，*ReplicateToken* 不一定能恢复先前被移除的组或权限。

该实现不会显式复制每一种令牌信息类。研究未能确认会显式复制 `TokenRestrictedSids`、`TokenOrigin`、`TokenSessionId` 或 AppContainer 能力。*ReplicateToken* 在保留源令牌更多属性的同时重建沙盒令牌；不应把它当作对每一个令牌字段的精确克隆。

## CopyDeviceGroups {#copydevicegroups}

```ini
CopyDeviceGroups=y
```

```ini
CopyDeviceGroups=n
```

*CopyDeviceGroups* 请求在新的令牌重建过程中保留源令牌的 `TokenDeviceGroups`。未配置有效值时，其使用方回退值（consumer fallback）为 `n`。它是一项沙盒级布尔设置：适用的已启用模板和 `GlobalSettings` 回退值可以参与构成实际生效的配置，但不支持按可执行文件限定的选择器。

它适用于 [令牌处理阶段](#token-processing-stages) 所述的新的重建路径，而不适用于历史过滤或 *UnrestrictedToken* 所选择的复制路径。无需显式设置 `UseCreateToken=y`：新的路径也可以由 *SandboxieAllGroup* 选择，或在历史过滤器不可用时选用。启用 *CopyDeviceGroups* 本身不会选择该路径。

即使显式配置了 `CopyDeviceGroups=n`，*ReplicateToken* 仍会启用设备组复制决策。这些设置不是别名：*CopyDeviceGroups* 只请求这个可选字段，而不执行 *ReplicateToken* 所做的更广泛的保留。

检索是尽力而为的。Sandboxie 需要可用的源令牌句柄，并且必须成功查询并为设备组信息分配空间。如果句柄不可用、分配失败或查询无法获取该信息，构造过程可以在没有它的情况下继续。

传递还取决于可用的令牌构造函数。扩展的 `ZwCreateTokenEx` 路径接受设备组；较旧的 `ZwCreateToken` 回退路径则不然。扩展构造函数失败不会自动触发不带设备组的重试。因此，启用此设置并不保证在每个受支持的系统上都能保留。

设备组与普通令牌组（`TokenGroups`）、令牌安全属性（`TokenSecurityAttributes`）和 AppContainer 能力是不同的。它们不是硬件设备列表。此设置不控制普通组成员身份或仅拒绝转换、*SandboxieAll* 组插入、用户 SID 替换、完整性降级、权限削减，或独立的 *CopyTokenAttributes* 操作。

保留设备组信息本身不会恢复管理员权限、更改设备 ACL、禁用 Sandboxie 设备限制或文件和注册表虚拟化、绕过其他安全控制，或授予不受限制的宿主设备访问权限。它不保证应用程序兼容性。

## CopyTokenAttributes {#copytokenattributes}

```ini
CopyTokenAttributes=y
```

```ini
CopyTokenAttributes=n
```

*CopyTokenAttributes* 应用于新的 `Token_CreateToken` 路径，专门指 `TokenSecurityAttributes`。Sandboxie 从源令牌读取这些安全属性，并把它们添加到新创建的令牌中。此设置不会复制每一种令牌信息类，也不意味着会复制 AppContainer 能力。

元数据与当前运行时默认值之间存在重要区别：

- 设置元数据列出的默认值为 `n`；
- 当前的 `Token_CreateToken` 实现在设置缺失时使用 `true` 作为运行时默认值。

因此，在当前实现中，该路径默认会复制令牌安全属性。显式设置 `CopyTokenAttributes=n` 会禁用此可选复制。启用 *ReplicateToken* 会强制启用复制行为，无论 *CopyTokenAttributes* 的显式取值如何。

属性复制发生在新令牌创建之后，并且是尽力而为的。查询、分配或应用 `TokenSecurityAttributes` 时失败不会使本来成功创建的令牌失效。

## KeepTokenIntegrity {#keeptokenintegrity}

```ini
KeepTokenIntegrity=y
```

```ini
KeepTokenIntegrity=n
```

*KeepTokenIntegrity* 默认值为 `n`。Sandboxie 通常会把源完整性 SID 替换为降低后的沙盒完整性级别。启用此设置则会保留源令牌的完整性级别，因此以高完整性级别起始的令牌可以保持高完整性级别。

完整性级别、组成员身份和权限是相互独立的令牌属性。*KeepTokenIntegrity* 保留源完整性级别；令牌组和权限则被独立过滤。它不会撤销 *DropAdminRights*，也不会改变 [`FakeAdminRights`](FakeAdminRights.md) 的兼容性行为。

启用此设置会使 *NoUntrustedToken* 失去意义。当正常的主令牌替换被 *NoSecurityIsolation* 绕过时，它同样是多余的。

## KeepUserGroup {#keepusergroup}

```ini
KeepUserGroup=y
```

```ini
KeepUserGroup=n
```

*KeepUserGroup* 默认值为 `n`。这里的“用户组”指 SID 与令牌的 `TokenUser` 相匹配的令牌组条目。它不特指 `BUILTIN\Users`、*SandboxieAll* 组或登录 SID。

在正常的组限制过程中，Sandboxie 可以禁用组或将它们转换为仅拒绝。启用 *KeepUserGroup* 后，与令牌用户 SID 相匹配的组会被保留，而不接受这种正常处理。`TokenUser` 身份本身仍可能在后续被正常的匿名登录（Anonymous Logon）或 Sandboxie SID 路径替换。

## UnstrippedToken {#unstrippedtoken}

```ini
UnstrippedToken=y
```

```ini
UnstrippedToken=n
```

*UnstrippedToken* 默认值为 `n`。它会跳过选定的剥离操作，但具体保留哪些属性取决于令牌构造路径。

### 新令牌构造路径 {#modern-token-construction-path}

在新的 `Token_CreateToken` 路径上，启用 *UnstrippedToken* 会跳过正常的组限制转换和完整性级别替换。正常的令牌用户替换仍会发生，权限仍会被削减到新路径的受限权限集，该权限集通常会保留 `SeChangeNotifyPrivilege`。

因此，它不会保留每一个令牌组成部分。

### 历史过滤路径 {#legacy-filtering-path}

在历史路径上，完整性处理发生在 *UnstrippedToken* 提前返回之前。后续的组剥离和限制步骤会被跳过。因此，不能把此设置一概等同于 *KeepTokenIntegrity*，两种实现的行为并不一致。

*UnstrippedToken* 的作用比 *UnfilteredToken* 更晚且范围更窄，不如 *UnrestrictedToken* 全面，也不是任何一者的别名。新行为与当前的常规配置最相关，但在其他配置或平台条件下，历史行为的区别仍然存在。

## 与 NoSecurityIsolation 的交互 {#interaction-with-nosecurityisolation}

当 [`NoSecurityIsolation=y`](NoSecurityIsolation.md) 时，Sandboxie 通常会绕过主令牌替换。因此，本页面介绍的设置对于正常主令牌而言通常是多余的，或者根本不会被执行：

- *NoUntrustedToken*
- *ReplicateToken*
- *CopyDeviceGroups*
- *CopyTokenAttributes*
- *UnfilteredToken*
- *UnrestrictedToken*
- *KeepTokenIntegrity*
- *KeepUserGroup*
- *UnstrippedToken*

该模式更广泛的影响参见 [无安全隔离](NoSecurityIsolation.md)。

## 与管理权限相关设置的交互 {#interaction-with-administrative-rights-settings}

[`DropAdminRights`](DropAdminRights.md) 执行真正的令牌过滤，包括禁用管理员相关组和移除选定权限。*UnfilteredToken* 可以绕过其初步过滤阶段，而单独启用 *UnrestrictedToken* 不会恢复在那里已被移除的属性。*KeepTokenIntegrity* 可以保留高完整性级别，但不会恢复管理员组或权限。

[`FakeAdminRights`](FakeAdminRights.md) 则不同：其当前实现主要使用兼容性钩子，使选定的管理员检查看起来成功。它不会恢复被令牌过滤移除的真实管理员组或权限。

## SandMan 配置 {#sandman-configuration}

在本页面的设置中，只有 *NoUntrustedToken* 有当前 SandMan 中的专用控件：

**沙盒选项 > 安全选项 > 高级安全 > 使用 低完整性令牌 而不是 不受信任的完整性令牌（会降低隔离）**

其余设置是高级的手动 [`Sandboxie.ini`](SandboxieIni.md) 选项。对于 *CopyDeviceGroups*，请使用**沙盒选项 > 配置文本 > 编辑配置**；没有专用的复选框。

## Sandboxie Plus 与 Classic {#sandboxie-plus-and-classic}

令牌处理由共享的 Sandboxie 组件实现。SandMan 公开 *NoUntrustedToken* 控件，而本页面的其他设置使用手动配置。当前源代码中不包含等效的专用 Sandboxie Control Classic 控件，但共享运行时在适用的情况下可以使用兼容的手动 INI 设置。Classic 通过**配置 > 编辑配置**提供手动编辑。

## 应用配置更改 {#applying-configuration-changes}

这些设置主要在 Sandboxie 准备、过滤或创建进程令牌时被读取。更改它们不会追溯性地重建已分配的主令牌。更改设置后请重启受影响的沙盒化进程；重建沙盒化进程树可获得一致的行为。通常不需要重启 SandMan、服务或驱动程序。

*UnfilteredToken* 在后续相关的模拟令牌处理中也会被读取，但这并不能免除在更改主令牌策略时重启进程的必要性。

*CopyDeviceGroups* 决策在到达新令牌构造时求值，包括后续相关的模拟令牌处理；它不是仅在进程启动时读取一次的缓存。后续读取配置不会重建已有的主令牌。

## 失败行为 {#failure-behavior}

必要的令牌过滤、构造或分配失败会导致进程初始化失败，而不会故意回退到限制较少的宿主令牌。具体的错误取决于失败的操作。

可选的 *CopyDeviceGroups* 检索失败则不同：源令牌句柄不可用、信息查询失败或分配失败都可能让构造过程在缺少可选设备组信息的情况下继续。这并不保证令牌创建或分配会成功，并且构造函数失败不会自动触发不带设备组的重试。

可选的 *CopyTokenAttributes* 步骤也有所不同：复制 `TokenSecurityAttributes` 失败不会使本来成功创建的令牌失效。

## 版本历史 {#version-history}

- *UnfilteredToken* 和 *UnrestrictedToken* 自 Sandboxie Plus 0.2.1 / Classic 5.41.1 起存在。
- *KeepTokenIntegrity* 自 Sandboxie Plus 0.3.0 / Classic 5.42 起存在。
- *KeepUserGroup* 和 *UnstrippedToken* 自 Sandboxie Plus 1.0.6 / Classic 5.55.6 起存在。
- 设置元数据记录 *NoUntrustedToken*、*ReplicateToken* 和 *CopyTokenAttributes* 为 Sandboxie Plus 1.14.1 新增。
- *CopyDeviceGroups* 在 Sandboxie Plus 1.17.0 / Classic 5.72.0 中引入。
- 专用的 *NoUntrustedToken* SandMan 控件在 Sandboxie Plus 1.17.0 / Classic 5.72.0 时期的变更中有记录。

## 相关页面 {#related-pages}

- [隔离机制](IsolationMechanism.md)
- [无安全隔离](NoSecurityIsolation.md)
- [撤销管理员权限](DropAdminRights.md)
- [模拟管理员权限](FakeAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
