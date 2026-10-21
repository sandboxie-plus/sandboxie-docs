# 开放凭据

`OpenCredentials` 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，用于控制 Sandboxie 在用户模式下对 Windows 凭据 API（WinCred）的兼容处理。默认禁用（`n`）。这是按沙盒生效的布尔设置，不支持按可执行文件名指定规则。

Windows 凭据 API 允许应用程序存储和读取用户名、密码及其他登录信息，包括网络资源的凭据。此设置只涉及 Sandboxie 对其拦截的 WinCred 调用的处理，并不涵盖 Windows 的所有凭据机制。

```ini
[DefaultBox]
OpenCredentials=y
```

启用后，Sandboxie 不会为受影响的沙盒化进程安装 WinCred 钩子，因此这些 API 调用会使用 Windows 原生实现。单独启用此设置**不会**禁用 Sandboxie 对旧版[受保护存储](ProtectedStorage.md)（PStore）的独立钩子。此设置也不能用于概括所有 Windows 凭据、身份验证或密码存储机制的行为。

<div id="behavior-when-disabled-in-a-standard-sandbox"></div>

## 在标准沙盒中禁用时的行为

除非有效 IPC 规则开放了 `\RPC Control\protected_storage`（例如通过[开放受保护的存储](OpenProtectedStorage.md)模板），否则 Sandboxie 会拦截 `CredWriteA/W`、`CredReadA/W`、`CredWriteDomainCredentialsA/W`、`CredReadDomainCredentialsA/W`、`CredDeleteA/W` 和 `CredEnumerateA/W`。这些是已实现的 WinCred 钩子，不代表覆盖了所有与凭据相关的 API。

默认兼容层主要对修改操作进行虚拟化，同时保留回退读取宿主数据的行为：

- 被拦截的凭据和域凭据写入会序列化到 Sandboxie 以 PStore 为后端的存储中，而不会通过这些调用直接更新原生凭据。
- `CredReadW` 会先检查沙盒中的表示形式；如果没有找到有效条目，可以回退到原生 `CredReadW`。`CredReadDomainCredentialsW` 在没有找到匹配的沙盒条目时，同样会回退到原生域凭据读取。
- `CredEnumerateW` 可以合并沙盒条目与原生凭据枚举结果。因此，沙盒化进程可能通过此 API 看到宿主凭据条目。
- 被拦截的删除操作会写入本地删除标记，而不是通过该路径调用原生凭据删除 API。

应用隔间模式在 PStore 层的行为不同。在该模式下，Sandboxie 不会安装替代 `PStoreCreateInstance` 的钩子；但如果受保护存储端点未开放，且未启用 `OpenCredentials=y`，WinCred 钩子仍可安装。此时，WinCred 后端存储的初始化会使用原生 PStore 提供程序，而不是 Sandboxie 的 `IPStoreImpl`。因此，上述标准沙盒的存储行为不能直接套用于应用隔间模式。

这些行为不能构成保护宿主凭据机密性的完整边界，也不能说明 Sandboxie 钩子范围之外的 API 会如何运行。

<div id="interaction-with-open-protected-storage"></div>

## 与开放受保护存储的关系

`Template=OpenProtectedStorage` 模板会添加开放受保护存储 IPC 端点的规则。当有效 IPC 策略开放了该端点时，Sandboxie 会同时跳过 PStore 钩子和 WinCred 钩子。因此，此模板的作用范围比单独设置 `OpenCredentials=y` 更广。它并不是在内部设置旧的 `OpenProtectedStorage` 布尔值。

SandMan 中对应的控件是 **沙盒选项 > 常规选项 > 限制选项 > 其它限制 > 开放 Windows 凭据存储访问权限（用户模式）**。选中 **开放“系统保护的存储”权限** 时，凭据控件会显示为已勾选且禁用。这不会自动保存 `OpenCredentials=y`；取消选中 PStore 控件后，会恢复已保存的凭据设置状态。

钩子是否安装取决于沙盒化进程中相关模块初始化时的配置。更改此设置或模板后，应重启受影响的沙盒化应用程序及其子进程；通常无需仅为这些钩子重启 Windows、Sandboxie 驱动程序或服务。

另请参阅[受保护存储](ProtectedStorage.md)、[开放受保护的存储](OpenProtectedStorage.md)和 [SBIE2213](SBIE2213.md)。
