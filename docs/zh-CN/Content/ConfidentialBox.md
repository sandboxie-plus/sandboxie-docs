# 保密沙盒

_ConfidentialBox_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，用于为沙盒内运行的进程和线程提供额外保护。

```ini
[DefaultBox]
ConfidentialBox=y
```

此设置默认关闭，需要当前有效且支持此功能的支持者证书。

## 保护范围

启用 `ConfidentialBox=y` 后，沙盒外宿主机进程创建或复制指向沙盒内进程、线程的句柄时，驱动会检查其请求的访问权限。检查涵盖只读和查询权限，不限于可修改或控制目标的权限。

此保护仅作用于进程和线程句柄。它不会加密文件、保护已挂载的沙盒根目录，也不会自动限制网络、剪贴板、图形界面、IPC 等获准使用的数据传输通道。若需要加密底层存储，请参阅[加密沙盒](../PlusContent/BoxEncryption.md)。

Sandboxie 为管理或运行沙盒所需的组件及 Windows 进程保留了例外，包括 SbieSvc 和 Start、某些核心或受保护的 Windows 进程、目标初始化期间启动它的进程，以及符合条件的 SandMan 或 Sandboxie Control 会话主进程（session leader）。[ProtectAdminOnly](ProtectAdminOnly.md) 决定会话主进程的例外是否要求管理员权限。

## DenyHostAccess

`DenyHostAccess` 为同一进程和线程保护机制提供按程序设置的规则，可独立于 `ConfidentialBox` 使用。

```ini
[DefaultBox]
DenyHostAccess=monitor.exe,y
DenyHostAccess=audiodg.exe,n
```

通用语法：

```ini
DenyHostAccess=[host-program-or-group,]y|n
```

- `y` 对匹配的沙盒外宿主机程序施加访问限制，同时保留上述为正常运行所需的例外。
- `n` 让匹配的程序免于此项保护检查，但不会授予 Windows 或其他检查所拒绝的权限。
- 不指定程序前缀时，该值作为整个沙盒的默认值。因此，`DenyHostAccess=y` 等同于默认拒绝规则。
- 程序选择条件遵循 Sandboxie 的[程序名称匹配](ProgramNamePrefix.md)规则，支持通配符，也可以引用已配置的进程组。

未启用 `ConfidentialBox` 时，只有宿主机进程请求的权限超出 Sandboxie 通常允许的权限子集，才会检查 `DenyHostAccess`。进程句柄和线程句柄的允许权限子集不同；若请求的权限全部在对应子集内，则不会触发此项限制。

在对象过滤路径中，匹配的拒绝规则会限制创建或复制句柄时请求的访问掩码，而非直接拒绝整个操作。操作成功时，所得句柄也可能没有任何可用的访问权限。独立的 Windows 访问检查或受保护进程限制仍可能导致操作失败。

启用 `ConfidentialBox` 后，同一检查还会涵盖只读和查询请求，且对宿主机程序默认拒绝访问。显式设置 `DenyHostAccess=program.exe,n` 可添加兼容性例外。内置的 **Less Confidential Box** 模板目前就为 `audiodg.exe` 配置了此类例外。

上述为正常运行所需的例外仍然适用。`DenyHostAccess` 不是通用文件系统规则，也不会阻止指定程序与沙盒进行所有形式的交互。

## 相关设置

- [加密沙盒](../PlusContent/BoxEncryption.md)保护沙盒的底层存储，并可添加挂载后的根目录保护；它与 `ConfidentialBox` 相互独立。
- [ProtectAdminOnly](ProtectAdminOnly.md) 控制会话主进程访问受保护进程，以及访问启用根目录保护的已挂载加密根目录时所适用的例外。
- [ProtectHostImages](ProtectHostImages.md) 限制某些沙盒进程加载可执行映像，是独立的保护机制。

## SandMan 设置

控件位置：

**沙盒选项 > 安全选项 > 沙盒保护**

- 选中“阻止沙盒外程序访问沙盒内进程”会写入 `ConfidentialBox=y`。
- “允许有用的 Windows 进程访问受保护的进程”会启用 **Less Confidential Box** 兼容性模板。
- 宿主机进程列表中的“允许进程”和“阻止进程”操作会写入 `DenyHostAccess` 条目。
- “当沙盒根目录受到保护时，沙盒管理器需要以管理员身份运行才能访问这些文件”控制 `ProtectAdminOnly`。

界面中的宿主机进程编辑器接受程序名称。更复杂的程序组或通配符规则可以手动配置。

## 使更改生效

`ConfidentialBox` 在各沙盒进程初始化时记录，因此修改后需要重新启动相关沙盒进程树。配置重新加载后，宿主机访问检查会查询 `DenyHostAccess`，以及 `ProtectAdminOnly` 中与进程访问有关的部分。

## 版本历史

`ConfidentialBox` 和 `DenyHostAccess` 自 Sandboxie Plus 1.3.3 / Classic 5.58.3 引入。加密沙盒镜像则在之后的 Sandboxie Plus 1.11.0 / Classic 5.66.0 中加入。

## 相关页面

- [黑色沙盒](../PlusContent/black-box.md)
- [加密沙盒](../PlusContent/BoxEncryption.md)
- [仅允许管理员访问](ProtectAdminOnly.md)
- [保护宿主机映像](ProtectHostImages.md)
- [沙盒预设比较](../PlusContent/box-preset-comparison.md)
