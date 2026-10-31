# 访问令牌隔离 {#access-token-isolation}

Sandboxie 将高度受限的主访问令牌用作沙盒隔离的一层。该令牌限制沙盒化进程通过直接的 Windows 访问检查所能执行的操作。文件、注册表、IPC 以及其他沙盒规则是更广泛的隔离模型中各自独立的层次。

Sandboxie Plus 1.14.1 引入了 `UseCreateToken` 和 `SandboxieAllGroup` 设置。自引入以来，它们的行为和默认值都有所演变。

## 当前行为 {#current-behavior}

虽然 `UseCreateToken` 本身默认为 `n`，但 `SandboxieAllGroup` 默认为 `y`，并且同样会选择新令牌构造路径。因此，即使没有显式写入 `UseCreateToken`，创建新的沙盒化令牌也是当前的正常行为。

## UseCreateToken {#usecreatetoken}

```ini
UseCreateToken=y
```

此设置显式选择 Sandboxie 的令牌构造路径，该路径会构造新的主令牌，而不是使用历史上的 `SepFilterToken` 过滤路径。`SepFilterToken` 是 Windows 内核的内部例程，Sandboxie 历史上通过针对具体实现的分析来定位它；它不是公开且有文档记录的 Windows API。

实际生效的行为如下：

- `UseCreateToken=y` 会选择新令牌路径，与 `SandboxieAllGroup` 无关。
- 当 `SandboxieAllGroup=y` 时，仅设置 `UseCreateToken=n` 不会选择历史路径。
- 当 `UseCreateToken=n` 且 `SandboxieAllGroup=n` 时，如果 Sandboxie 能定位到该内部例程，就可以使用历史过滤路径。
- 如果无法定位该内部例程，Sandboxie 会回退到构造新令牌。

## SandboxieAllGroup {#sandboxieallgroup}

```ini
SandboxieAllGroup=y
```

此设置启用共享的 Sandboxie SID：

```text
S-1-5-100-0
```

Windows 将该 SID 显示为：

```text
Sandboxie\All Sandboxes
```

Sandboxie 会将该 SID 作为普通启用组添加到沙盒化令牌中。该组由所有沙盒中的进程共享，因此 Windows 的访问控制或审核策略可以用它来统一匹配沙盒化进程。该 SID 本身不授予访问权限；必须由 ACL 或其他策略引用它。它既不能标识单个沙盒，也不能把一个沙盒与另一个沙盒隔离开。

## 实际生效的设置 {#effective-settings}

| `UseCreateToken` | `SandboxieAllGroup` | 实际行为 |
| --- | --- | --- |
| 默认 / 未设置 | 默认 / 未设置 | 带共享 Sandboxie 组的新令牌路径 |
| `n` | `y` | 带共享组的新令牌路径 |
| `y` | `y` | 带共享组的新令牌路径 |
| `y` | `n` | 不带共享组的新令牌路径 |
| `n` | `n` | 可用时使用历史过滤路径；否则回退到新令牌 |

当某项设置未写入单个沙盒时，全局设置会影响其实际生效的值。

## SandMan 控件 {#sandman-control}

在 SandMan 中，该控件位于**沙盒选项 > 安全选项 > 高级安全 > 沙盒令牌**下，标签为**创建新的沙盒令牌，而不是剥离原始令牌**。

| 界面状态 | 含义 |
| --- | --- |
| 已勾选 | 创建新的沙盒化令牌，并包含共享的 `Sandboxie\All Sandboxes` 组 |
| 部分勾选 | 创建新的沙盒化令牌，但不包含共享组 |
| 未勾选 | 同时禁用这两个选项，在可用时允许使用历史过滤路径 |

当默认值或全局继承已经产生所选状态时，SandMan 可能会删除某项设置，而不是写入字面的 `y` 或 `n`。共享组是否启用还由另一个单独的全局选项控制。

## 令牌限制 {#token-restrictions}

在正常的新令牌路径中，Sandboxie 会构造一个高度受限的主访问令牌，除其他限制外，它会：

- 削减进程可以使用的权限；
- 通常把普通组转换为仅拒绝，使其无法授予访问权限；
- 视配置应用低或不可信完整性策略；
- 替换 Sandboxie 隔离模型所使用的沙盒身份。

令牌的具体内容还可能受其他高级设置影响。

### 共享组与按沙盒身份 {#shared-group-and-per-sandbox-identity}

`Sandboxie\All Sandboxes` 为所有沙盒共有，当策略需要匹配所有沙盒化进程时很有用。与 SandboxieLogon 配合使用的按沙盒身份则标识特定的沙盒，用途不同。

## 安全影响 {#security-implications}

受限主令牌有助于确保直接的 Windows 访问尝试不会简单地以原始未受限身份执行。随后，Sandboxie 经由驱动程序中介的路径可以单独执行文件、注册表、IPC 和其他资源访问规则。

新令牌路径与历史过滤路径的主要区别在于实现方式和令牌内容。两者都参与 Sandboxie 更广泛的隔离设计；两者都不应被视为完整的安全模型，新令牌路径也并非在每种配置下都绝对更安全。

## 管理员与提升权限行为 {#administrator-and-elevation-behavior}

以提升权限方式运行应用程序，并不意味着沙盒化进程使用的主令牌会保留完整的管理员组和权限集。Sandboxie 仍会应用其令牌限制。[撤销管理员权限](DropAdminRights.md) 是一项独立设置，会进一步影响管理员权限与提升权限的行为。

## 与 NoSecurityIsolation 的交互 {#nosecurityisolation-interaction}

当以下设置生效时，这些令牌隔离设置不会用于正常的令牌替换：

```ini
NoSecurityIsolation=y
```

该模式的更广泛影响参见 [无安全隔离](NoSecurityIsolation.md)。

## 兼容性与失败行为 {#compatibility-and-failure-behavior}

新令牌路径避免依赖 `SepFilterToken` 作为正常实现路径，并在后续的 Sandboxie Plus 版本中成为正常行为。当两项设置都实际禁用了新路径且内部例程可用时，仍可使用历史路径。

如果无法定位历史过滤例程，Sandboxie 会回退到构造新令牌。在真正构造或应用沙盒化令牌时发生运行时失败，可能导致进程无法初始化。

## 版本历史 {#version-history}

- Sandboxie Plus 1.14.1 引入了 `UseCreateToken` 和 `SandboxieAllGroup`。
- 后续版本为该实现加入了兼容性和安全修复。
- 从 Sandboxie Plus 1.17.0 起，`SandboxieAllGroup` 默认启用，使新令牌路径成为正常行为。

## 相关设置 {#related-settings}

- [Sandboxie Ini](SandboxieIni.md)
- [撤销管理员权限](DropAdminRights.md)
- [无安全隔离](NoSecurityIsolation.md)
- [隔离机制](IsolationMechanism.md)
- [SandboxieDrv 令牌内部实现](TokenMagic.md)
