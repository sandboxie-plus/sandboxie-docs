# 原始令牌 {#original-token}

*OriginalToken* 是一项高级、不安全的兼容性与调试设置。它会阻止 Sandboxie 通过正常的受限令牌路径替换沙盒化进程的 Windows 主访问令牌。它还会在其他位置放宽选定的令牌与模拟处理。它**不会**让进程在沙盒外运行。

> [!WARNING]
> `OriginalToken=y` 会显著削弱 Sandboxie 基于令牌的隔离。Sandboxie 通常会削减的组、权限与完整性特征，可能从传入的令牌中保留下来。因此，以提升权限的令牌启动的应用程序可能保留该提升状态；此设置不会为标准用户授予管理员权限。即使其他沙盒机制仍然生效，更强的令牌也可能增加对宿主资源的访问。Sandboxie 将其归类为不安全的调试选项。

## 配置 {#configuration}

```ini
[DefaultBox]
OriginalToken=y
```

运行时默认值为 `n`（禁用）。这是一项沙盒级布尔设置；正常的配置解析也可以通过适用的模板或全局设置提供该值。当前的使用方不会按可执行文件名选择 *OriginalToken*。不要使用 `OriginalToken=program.exe,y` 这类按可执行文件限定的形式来配置此行为。

SandMan 没有专门的 *OriginalToken* 复选框，其常规的高级选项列表中也没有对应条目。仅在确有特定兼容性或调试需求时，才通过 [Sandboxie Ini](SandboxieIni.md) 进行配置。当前随附的模板不会自动启用它。

## 主令牌行为 {#primary-token-behavior}

对于正常的沙盒化进程，Sandboxie 会获取初始主令牌，在配置了初步过滤时应用该过滤，然后构造或限制，并分配一个由 Sandboxie 管理的主令牌。视配置而定，这些步骤可以削减权限、改变组访问权限并降低完整性。

启用 `OriginalToken=y` 时，驱动程序会在该正常主令牌过滤、限制与分配路径之前返回。进程保留提供给该路径的 Windows 令牌，而不会获得 Sandboxie 通常分配的受限替代令牌。这并不意味着原始权限中的每一项都始终存在：传入的令牌本身可能已经受限，其他 Windows 或 Sandboxie 路径也仍可能影响特定的令牌操作。正常的令牌模型参见 [访问令牌隔离](AccessTokenIsolation.md)。

### 与其他令牌设置的区别 {#distinction-from-other-token-settings}

| 配置 | 正常主令牌路径中的初步过滤 | 后续的受限令牌构造与分配 |
| --- | --- | --- |
| 默认 | 应用 | 应用 |
| `UnfilteredToken=y` | 跳过 | 仍然应用 |
| `UnrestrictedToken=y` | 仍然参与 | 通过 Sandboxie 的令牌路径复制并分配一个限制较少的令牌 |
| `OriginalToken=y` | 跳过正常的主令牌替换路径 | 不通过该路径分配受限主令牌 |

因此，*UnfilteredToken* 和 *UnrestrictedToken* 并不是 *OriginalToken* 的别名。在主令牌替换路径中，*OriginalToken* 会在 *ReplicateToken*、*CopyTokenAttributes*、*UnstrippedToken*、*KeepTokenIntegrity* 等选项以及 *DropAdminRights* 初步过滤的分支之前返回。这并不意味着上述设置的每一个独立使用方都不再起作用。[Advanced Token Settings](AdvancedTokenSettings.md) 介绍了它们各自的阶段。*FakeAdminRights* 在创建子进程期间也有单独的兼容性行为。

## 仍然处于沙盒中的部分 {#what-remains-sandboxed}

进程仍在其沙盒中注册，Sandboxie 的正常进程初始化也仍会建立独立配置的文件、注册表、IPC、GUI 和网络处理。仅凭 *OriginalToken* 并不会禁用 SbieDll 注入与沙盒身份。因此，文件和注册表虚拟化、适用的过滤器以及其他沙盒规则都可以继续生效。

生效的过滤器并不保证能得到与正常受限令牌进程相同的宿主访问结果。Windows 访问检查可以看到 *OriginalToken* 保留下来的更强令牌。应把此设置视为对基于令牌的保护的实质性削弱，而**不是**完全移除沙盒，也不是以同等强度保留其他所有保护。

## 应用隔间 {#application-compartment}

[应用隔间](NoSecurityIsolation.md) 与 *OriginalToken* 共享部分运行时分支，这些分支会绕过受限主令牌替换，并使用更直接的子进程创建路径。应用隔间不会自动写入或启用 `OriginalToken=y`，这两种配置也不等同。应用隔间还有额外的路径策略、过滤和作业对象行为，仅靠 *OriginalToken* 不会启用这些行为。

## 子进程与 AppContainer 令牌 {#child-processes-and-appcontainer-tokens}

在创建子进程时，*OriginalToken* 会跳过 Sandboxie 后续的挂起创建与令牌替换序列，并把最终的令牌选择交给 Windows。它**不**保证每个子进程都获得父进程令牌的精确副本。特别是，[丢弃子进程令牌](DropChildProcessToken.md)可以在 *OriginalToken* 分支运行**之前**清除调用方提供的令牌。*DropAppContainerToken* 也在该分支之前求值，其他特殊情形处理同样可能影响传给 Windows 的令牌。

*OriginalToken* 不会禁用所有 AppContainer 兼容性处理。[AppContainer 令牌兼容性](AppContainerTokens.md)介绍了那些独立的 API、进程属性和调用方提供令牌的阶段。

## 模拟及相关影响 {#impersonation-and-related-effects}

此设置的影响范围不止主令牌替换。驱动程序会放宽 Sandboxie 特有的模拟令牌验证路径，SbieDll 也会省略选定的模拟钩子和令牌兼容性处理。其他 IPC 命名空间与安全钩子仍会安装。这并不意味着模拟总是成功，也不意味着所有 IPC 隔离都被禁用；Windows 检查和其他 Sandboxie 控制仍然生效。

*OriginalToken* 还会改变 Sandboxie 服务所做的部分令牌选择与检查。它本身**不会**让沙盒化的 RpcSs 以 SYSTEM 身份运行：当前自动的 SYSTEM 源路径还需要 *MsiInstallerExemptions* 或 *RunServicesAsSystem* 等设置。这些独立行为参见 [Sandboxed Services](SandboxedServices.md) 和 [RPC Compatibility](RpcCompatibility.md)。

此设置可以省略 Sandboxie 根作业对象上的基本 UI 限制，但不会把进程从该作业对象中移除，也不会自动禁用其资源限制。参见 [Job Objects](JobObjects.md)。

## 应用更改 {#applying-changes}

主令牌替换以及若干钩子安装决策发生在沙盒化进程启动时。更改 *OriginalToken* 不会重建现有进程的令牌，也不会在该进程中重新安装钩子。更改后请重启受影响的沙盒化进程；重启整个沙盒化进程树可以得到一致的测试结果。通常不需要重启 Windows，也不需要重启 SandMan、服务或驱动程序。

## 版本历史 {#version-history}

当前的设置元数据记录为 `AddedVersion=0.2.1`，而变更日志将 *OriginalToken* 描述为 Sandboxie Plus 0.4.5 / Classic 5.44.1 中的实验性测试/调试选项。这些来源并未确定一个明确的引入版本。变更日志后来又称其为不安全的调试选项。

## 相关页面 {#related-pages}

- [访问令牌隔离](AccessTokenIsolation.md)
- [Advanced Token Settings](AdvancedTokenSettings.md)
- [丢弃子进程令牌](DropChildProcessToken.md)
- [无安全隔离](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
