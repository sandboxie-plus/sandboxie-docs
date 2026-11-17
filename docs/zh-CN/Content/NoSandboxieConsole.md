# 无 Sandboxie 控制台 {#no-sandboxie-console}

_NoSandboxieConsole_ 是一项高级调试与兼容性设置，用于绕过 Sandboxie 自定义的控制台重定向与代理路径。

```ini
[DefaultBox]
NoSandboxieConsole=y
```

默认值为 `n`。这是一项沙盒级布尔设置；常规的模板与 `GlobalSettings` 继承可以贡献它的生效值。

> [!IMPORTANT]
> 这个名称并不意味着控制台应用程序被禁用，也不意味着不能存在控制台窗口。它禁用 Sandboxie 的自定义控制台处理，以便在可能的情况下使用 Windows 的常规控制台行为。

## 有哪些变化 {#what-changes}

启用 `NoSandboxieConsole=y` 后，Sandboxie 在进程初始化期间进入无自定义控制台的分支：

- 驱动程序跳过特殊的初始化步骤，该步骤可能把控制台应用程序从其初始控制台分离，并标记为稍后创建代理控制台；
- 底层初始化跳过相应的 WOW64 控制台句柄调整；
- SbieDll 跳过其代理控制台重连与 `AllocConsole` 替换路径，以及常规分支所安装的控制台标题钩子；
- Sandboxie 的 `ConsoleControl` 钩子不会被导入或安装。

这些变化绕过了 SbieDll 请求 SbieSvc GUI 代理创建一个辅助控制台、再把沙盒化进程附加到该控制台的路径。该设置不会阻止 `cmd.exe`、PowerShell 或其他控制台应用程序运行。

## 仍然生效的部分 {#what-remains-active}

该设置并不会移除 Sandboxie 所有与控制台相关的代码路径。只要存在当前控制台窗口，SbieDll 仍会记录它，以便其后来的辅助 GUI/消息线程可以工作，包括用于设备更改通知的消息处理。

Sandboxie 的其他隔离与虚拟化机制也保持独立。`NoSandboxieConsole` 不是用于终端、桌面、令牌或 GUI 隔离的通用开关。

## 兼容性与调试 {#compatibility-and-debugging}

该选项是为那些无法与 Sandboxie 自定义控制台重定向配合工作的应用程序提供的调试与兼容性逃生通道。它不是常规默认值，也不应被描述为禁用 Windows 控制台宿主。

当前源代码实现的是上文描述的经典 Sandboxie 控制台路径。它并未为 Windows Terminal 或伪控制台（ConPTY）会话确立全面的行为。

## 应用隔间 {#application-compartment}

[应用隔间](NoSecurityIsolation.md) 进程在驱动程序、底层与 SbieDll 初始化期间本来就会绕过同样的自定义控制台分支。在应用隔间沙盒中再添加 `NoSandboxieConsole=y` 不会第二次启用该控制台行为。这种等效性仅限于相关的控制台路径；除此之外，两项设置并不可以互换。

## 与 DropConHostIntegrity 的关系 {#relationship-to-dropconhostintegrity}

[降低 ConHost 完整性](DropConHostIntegrity.md) 作用于通过 Sandboxie 代理/辅助路径创建的外部控制台宿主。由于 `NoSandboxieConsole=y` 绕过了该路径，不应指望 `DropConHostIntegrity` 会修改通过由此产生的常规 Windows 控制台路径创建的控制台宿主。

## SandMan 配置 {#sandman-configuration}

SandMan 目前没有为 `NoSandboxieConsole` 提供专门的控件。请在 `Sandboxie.ini` 的沙盒节中手动配置它，或通过适用的模板或 `GlobalSettings` 条目配置。

## 应用更改 {#applying-changes}

该设置在进程与控制台的早期初始化期间被读取，无法为已在运行的进程改用另一种控制台路径。更改后请重启受影响的沙盒化控制台应用程序。通常不需要重启 SandMan、服务或驱动程序。

## 版本历史 {#version-history}

`NoSandboxieConsole` 在 Sandboxie Plus 0.9.8 / Classic 5.53.0 中引入。更新日志指出，该控制台行为此前属于 `NoSandboxieDesktop=y`；当前源代码把 `NoSandboxieConsole` 与 `NoSandboxieDesktop` 作为两项独立的设置读取。

## 相关页面 {#related-pages}

- [降低 ConHost 完整性](DropConHostIntegrity.md)
- [无安全隔离](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
