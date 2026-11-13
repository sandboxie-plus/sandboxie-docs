# 阻止注册设备通知 {#block-register-device-notification}

`BlockRegisterDeviceNotification` 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒范围布尔设置。启用后，它会抑制通过选定的 USER32 API 发出的设备通知注册。默认值为 `n`。

```ini
[DefaultBox]
BlockRegisterDeviceNotification=y
```

## 运行时行为 {#runtime-behavior}

启用该设置后，Sandboxie 会为以下函数安装用户态钩子：

- `RegisterDeviceNotificationA`；
- `RegisterDeviceNotificationW`；
- `UnregisterDeviceNotification`。

被拦截的 ANSI 与 Unicode 注册调用不会去调用底层的 Windows 注册函数。Sandboxie 会清除最后一个错误值，并返回一个看起来成功的占位句柄，因此应用程序可能认为注册已经成功，尽管并未通过该调用做出任何注册。被拦截的注销函数同样会清除最后一个错误值并报告成功，而不执行真正的注销操作。

该占位句柄属于实现细节，应用程序不应依赖它。

## 作用范围与限制 {#scope-and-limitations}

此设置抑制的是通过 `RegisterDeviceNotificationA/W` 做出的注册；它并不是对所有设备更改通知或即插即用通知机制的通用封锁。当前实现并未确立“沙盒化应用程序永远无法通过其他路径收到 `WM_DEVICECHANGE`、广播通知、配置管理器通知、服务通知或内核级通知”这一结论。

需要特别说明的是，驱动程序那套独立的配置管理器过滤器目前并不拒绝与 `CMP_Register_Notification` 关联的函数。该路径与此设置所拦截的 USER32 注册函数不同。

## 应用更改 {#applying-changes}

该设置可以为某个沙盒指定，也可以通过常规的模板与全局配置解析继承。它没有已记录在案的可执行文件限定语法。

Sandboxie 在沙盒化进程中初始化 GUI 钩子时读取有效值。更改该设置不会在已经完成初始化的进程中动态安装或移除这些钩子。更改后，请重启受影响的沙盒化应用程序，或重建沙盒化的进程树。通常不需要重启 SandMan、服务或驱动程序。

## SandMan 配置 {#sandman-configuration}

SandMan 目前没有为 `BlockRegisterDeviceNotification` 提供专用复选框。请在沙盒的 INI 配置节中手动配置。

## 与其他设备功能的关系 {#relationship-to-other-device-features}

[`OpenDevCMApi`](OpenDevCMApi.md) 控制的是另一套驱动程序过滤器，作用于选定的、具有变更效果的设备配置管理器操作。两项设置独立运作。

[USB 沙盒化](../PlusContent/USBSandboxing.md) 是 SandMan 的宿主侧自动化：它检测符合条件的 USB 卷并维护强制文件夹规则。`BlockRegisterDeviceNotification` 不控制该自动化，也不会阻止 SandMan 自身观察到设备更改。

## 版本历史 {#version-history}

当前设置元数据列出 `BlockRegisterDeviceNotification` 引入于 Sandboxie Plus 1.9.5 / Classic 5.64.5。相应的运行时改动使通知注册钩子以此设置为条件。同一版本的更新日志还记录了一项修复，涉及使用 `DBT_DEVTYP_DEVICEINTERFACE` 的 `RegisterDeviceNotificationW` 注册。

## 相关页面 {#related-pages}

- [开放设备配置管理器 API](OpenDevCMApi.md)
- [USB 沙盒化](../PlusContent/USBSandboxing.md)
- [Sandboxie Ini](SandboxieIni.md)
