# 受保护存储

Windows 受保护存储（PStore）是一种旧版接口，应用程序可通过 `PStoreCreateInstance` 和 `IPStore` API 存储密码等需要保护的用户数据。它与[开放凭据](OpenCredentials.md)中介绍的 Windows 凭据 API（WinCred）不同，不能将二者视为现代 Windows 密码存储的不同名称。

在普通沙盒中，Sandboxie 通常会用自己的 `IPStoreImpl` 兼容实现替代 `PStoreCreateInstance`。本地修改的数据存放在沙盒内的存储文件中。当前代码默认在 Windows 目录下构造 `SbiePst.dat` 文件名，但文件名可在构建时覆盖，实际物理位置也取决于沙盒文件虚拟化，因此不能依赖固定的宿主路径。此实现旨在兼容使用旧版 PStore 接口的应用程序，并不保证隔离所有 Windows 凭据机制。

PStore 读取在本地没有相应记录时，也可以通过 Sandboxie 服务查询原生 PStore；枚举同样可以结合原生提供程序返回的结果。因此，使用本地存储文件并不意味着只能读取沙盒内的数据。实际结果取决于原生提供程序是否可用及其访问检查。

Sandboxie 默认的 WinCred 兼容层也使用此 PStore 实现存储被拦截的凭据修改。WinCred 的读取和枚举路径仍可查询 Windows 原生凭据存储。有关这一边界，参见[开放凭据](OpenCredentials.md)。

<div id="data-visibility-and-protection"></div>

## 数据可见性与保护

Sandboxie 的替代实现使用沙盒化 Windows 路径中的一个共用存储文件，而不是为每个应用程序建立独立的 PStore 文件。能否访问该文件仍取决于沙盒和宿主权限，因此不能据此推断不同 Windows 用户账户之间的数据可见性。

当前文件格式对存储的数据块施加的是简单的可逆变换，而非强加密。应将含有 PStore 条目的沙盒数据视为敏感数据。只要存储文件仍位于沙盒内，删除沙盒内容也会删除这些本地条目；这不会删除宿主凭据，也不会删除通过已开放宿主路径存储的数据。

<div id="opening-the-system-implementation"></div>

## 开放系统实现

选择[开放受保护的存储](OpenProtectedStorage.md)模板，可添加相关系统端点的开放规则。当受保护存储 IPC 端点的有效策略为开放时，Sandboxie 会跳过其替代 PStore 钩子以及用户模式下的 WinCred 钩子。旧的 `OpenProtectedStorage=y` 布尔设置不是当前的配置方法。

[应用隔间](../PlusContent/compartment-mode.md)模式也会跳过 Sandboxie 的替代 PStore 钩子。WinCred 钩子有独立的检查，因此不能将应用隔间模式本身描述为自动启用 `OpenCredentials`。

这些兼容性选项并不涵盖沙盒化应用程序存储或访问敏感信息的所有方式。不受支持的 PStore 方法参见 [SBIE2205](SBIE2205.md)；Sandboxie 凭据后端存储初始化失败的问题参见 [SBIE2213](SBIE2213.md)。
