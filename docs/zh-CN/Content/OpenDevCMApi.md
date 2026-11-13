# 开放设备配置管理器 API {#open-device-configuration-manager-api}

`OpenDevCMApi` 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒范围布尔设置。它会禁用 Sandboxie 对某些具有变更效果的 Windows 设备配置管理器操作所施加的选择性过滤器。默认值为 `n`。

```ini
[DefaultBox]
OpenDevCMApi=y
```

!!! warning
    启用此设置可能让提权后的沙盒化进程对宿主硬件配置做出更改，且这些更改在沙盒删除后依然存在。它不会授予对所有硬件的不受限访问权限，不会绕过 Windows 访问检查，也不会禁用 Sandboxie 的其他资源限制。

## 过滤的内容 {#what-is-filtered}

在默认的 `OpenDevCMApi=n` 下，Sandboxie 驱动程序会检查发往配置管理器 API 端点的设备控制请求：

```text
\Device\DeviceApi\CMApi
```

选定的变更类操作会以访问被拒绝状态被拒绝。当前过滤器涵盖以下类别：

- 更改软件设备的属性或生存期；
- 注册软件设备接口，以及更改这些接口的状态或属性；
- 设置设备节点、设备接口或设备类的属性；
- 设置设备类或设备节点的注册表属性；
- 设置设备节点的问题状态；
- 禁用设备节点，或请求移除某个设备子树；
- 注册或注销设备接口；
- 创建或卸载设备节点；
- 删除设备接口、设备节点或设备类的项。

这是一份选择性的拒绝列表，而不是对配置管理器 API 的完整封锁。当前的查询与读取操作一般会被放行，包括用于枚举设备或设备类、读取属性、查询设备节点状态或深度、解析接口别名、校验设备实例以及打开相关注册表项的代表性操作。未被该过滤器选中的其他操作同样会继续进入底层 Windows 设备控制路径。

`OpenDevCMApi=y` 会跳过这道针对 CMApi 的变更过滤器。底层操作仍受 Windows 权限以及任何独立的 Sandboxie 控制约束，因此该设置并不保证所请求的硬件管理操作一定成功。它本身也不会改变 CMApi 设备对象能否被打开。

## 过滤器存在的原因 {#why-the-filter-exists}

该过滤器是针对安全议题 ID-14 引入的，此前 [issue #552](https://github.com/sandboxie-plus/Sandboxie/issues/552) 表明，提权后的进程可以在沙盒内使用设备管理器移除宿主设备。那些更改影响了宿主，并且独立于沙盒删除而持续存在。

请仅把 `OpenDevCMApi=y` 当作兼容性例外，用于确实需要某项被过滤的设备管理操作的软件。

## 兼容性 {#compatibility}

Sandboxie Plus 0.7.1 / Classic 5.48.5 细化了该过滤器，在保留选定变更限制的同时修复了摄像头访问问题。因此，普通的摄像头访问不应被视为需要 `OpenDevCMApi=y`。

## 应用更改 {#applying-changes}

该设置可以为某个沙盒指定，也可以通过常规的模板与全局配置解析继承。它没有已记录在案的可执行文件限定语法。

驱动程序在初始化每个沙盒化进程时缓存有效值。更改该设置后，请重启受影响的沙盒化应用程序，或重建沙盒化的进程树。新启动的进程通常不需要重启 SandMan、服务或驱动程序。

## SandMan 配置 {#sandman-configuration}

该控件位于：

**沙盒选项 > 常规选项 > 隔离 > 允许沙盒内程序管理硬件设备**

该复选框默认未选中。选中它会写入 `OpenDevCMApi=y`，即限制较少的兼容性状态。当选中 **无安全隔离** 时，SandMan 会禁用该控件。

## 与其他设备功能的关系 {#relationship-to-other-device-features}

[`BlockRegisterDeviceNotification`](BlockRegisterDeviceNotification.md) 控制的是另一组用于设备通知注册的用户态钩子。它不会启用或禁用 CMApi 变更过滤器。

[USB 沙盒化](../PlusContent/USBSandboxing.md) 同样是独立的。该功能是 SandMan 的一项自动化：为符合条件的 USB 卷维护强制文件夹规则；它不使用 `OpenDevCMApi` 来虚拟化或控制 USB 设备。

## 版本历史 {#version-history}

| 更改 | 版本 |
| --- | --- |
| 引入 CMApi 变更过滤器与 `OpenDevCMApi` 兼容性设置 | Sandboxie Plus 0.7.0 / Classic 5.48.0 |
| 改善启用过滤器后的摄像头兼容性 | Sandboxie Plus 0.7.1 / Classic 5.48.5 |

## 相关页面 {#related-pages}

- [阻止注册设备通知](BlockRegisterDeviceNotification.md)
- [USB 沙盒化](../PlusContent/USBSandboxing.md)
- [Sandboxie Ini](SandboxieIni.md)
