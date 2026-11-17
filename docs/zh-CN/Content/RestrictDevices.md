# 限制设备访问 {#restrict-devices}

*RestrictDevices* 可减少沙盒化进程对 NT `\Device` 命名空间下任意驱动程序与设备终结点的访问。它使用 Sandboxie 的文件/路径过滤规则：把宽泛的设备路径限制与更具体的内置兼容性例外结合起来。它既不是通用的硬件阻断器，也不是网络防火墙。

## 配置 {#configuration}

该设置默认禁用。要为某个沙盒启用它，请添加：

```ini
[DefaultBox]
RestrictDevices=y
```

该设置按整个沙盒进行评估，包括适用的配置继承。它没有可执行文件限定的形式。更改后，请重启受影响的沙盒化进程。

[安全强化模式](../PlusContent/security-mode.md)（`UseSecurityMode=y`）即使 `RestrictDevices` 缺失或被显式设为 `n`，也会启用相同的设备限制行为。它还会启用其他安全功能；选择该模式并不需要另外添加 `RestrictDevices=y` 条目。

## 设备路径策略 {#device-path-policy}

当前的内置策略保存在 `Templates.ini` 的内部 `[TemplateSModPaths]` 节中，它用 `ClosedFilePath` 宽泛地封闭 `\Device\*`，并包含更具体的 `NormalFilePath` 例外。这些例外包括 `\Device\CNG` 与 `\Device\NamedPipe\*` 等 Windows 兼容性终结点。NT `\Device` 命名空间还包含命名管道之类的对象，它们并不是物理硬件。随附的例外列表可能随版本变化。

该限制是一种 Sandboxie 路径策略。它不会更改 Windows 设备 ACL、卸载设备、禁用宿主驱动程序，也不保证 `\Device` 下的每一项操作都被阻止。当宿主驱动程序提供强大的设备控制接口时，它可以减少暴露给沙盒化应用程序的攻击面；但它并不能阻止所有针对脆弱驱动程序的漏洞利用。

设备限制还会启用 [规则特异性](../PlusContent/RuleSpecificity.md)，即使配置了 `UseRuleSpecificity=n` 也是如此。这样，足够具体的例外便可优先于宽泛的设备路径封闭。

普通驱动器与卷路径会单独处理，以便启用该限制时不至于让正常的文件系统访问直接不可用。在隐私模式之外，内置的驱动器模式按常规路径处理。使用 [隐私模式](../PlusContent/privacy-mode.md) 时，设备限制仍然生效，但这些驱动器模式改为接受隐私模式的 `WriteFilePath` 处理。这并不是允许不受限制的原始磁盘访问。

## 允许特定终结点 {#allowing-a-specific-endpoint}

如果某个应用程序需要被宽泛规则封闭的设备终结点，请在确认真实的 NT 路径后，使用最窄且合适的 [标准文件路径](NormalFilePath.md) 例外。下例中的 `VendorDevice` 只是占位符：

```ini
[DefaultBox]
RestrictDevices=y
NormalFilePath=\Device\VendorDevice*
```

对于匹配的终结点，`NormalFilePath` 会恢复 Sandboxie 的常规路径处理：读取可以使用真实路径，而在适用的情况下，写入仍受常规的沙盒复制/虚拟化行为约束。非文件系统的驱动程序终结点可能不会像普通文件那样工作。相比之下，[开放文件路径](OpenFilePath.md) 请求直接访问真实宿主路径；它不是此设置的标准兼容性例外。Windows 权限与其他 Sandboxie 控制仍然适用。

> [!WARNING]
> 只添加兼容性所需的例外。覆盖 `\Device` 命名空间大部分区域的宽泛 `NormalFilePath` 规则，在其比内置设备封闭规则更具体时，会大幅削弱这层防护。请优先使用能解决兼容性问题的最窄的终结点专属规则。

排查问题时，请保持 `RestrictDevices=y`，在可用的情况下借助 Sandboxie 的跟踪日志或资源访问监视器找出被拒绝的 `\Device\...` 路径，添加一条较窄的 `NormalFilePath` 规则，然后重新测试。并非每一次拒绝都有专门的 SBIE 消息。特定外设的结果还取决于它的 NT 终结点、Windows 权限、设备控制操作以及其他 Sandboxie 规则。

## 与其他设置的交互 {#interaction-with-other-settings}

- [阻止网络文件访问](BlockNetworkFiles.md)：当它被禁用时，Sandboxie 会为其网络重定向器与 MUP 路径添加常规路径例外。当它被启用时，则不添加这些特定的例外。`RestrictDevices` 不能取代网络访问规则或 Windows 筛选平台的强制执行。
- [禁用文件过滤器](DisableFileFilter.md)：设备限制依赖 Sandboxie 的文件/路径过滤层。为某个进程禁用该层会削弱这项设备路径策略的执行。
- [应用隔间](NoSecurityIsolation.md)：仅 `NoSecurityIsolation=y` 不会关闭设备限制。不过在应用隔间中，[无安全过滤](NoSecurityFiltering.md) 会禁用用于执行该限制的文件过滤层。
- [开放设备配置管理器 API](OpenDevCMApi.md)：内置设备策略为 `\Device\DeviceApi*` 系列设置了常规路径例外。`OpenDevCMApi` 则通过其 CMApi 终结点单独控制选定的配置管理器操作；两者不是同一项限制。
- [阻止注册设备通知](BlockRegisterDeviceNotification.md) 与 [USB 沙盒化](../PlusContent/USBSandboxing.md) 处理的是另外的通知与 USB 强制执行行为。`RestrictDevices` 不会启用其中任何一项。

已有的设备句柄不会因这项路径策略被追溯剥夺权限。该设置影响的是后续相关的路径/打开评估。路径规则列表可以为正在运行的进程刷新，但刷新不会重新计算该进程已保存的 `RestrictDevices` 状态。更改该设置本身后，请重启受影响的进程树以获得一致的测试结果；对于新启动的进程，不需要重启 Windows，也不需要常规的驱动程序或服务重启。

## SandMan 界面与证书 {#sandman-interface-and-certificate}

在 SandMan 中，打开 **沙盒选项 > 安全选项 > 安全加固** 并选中 **将对“驱动程序/设备”的访问权限制在已知的终结点列表内**。在普通沙盒中，它默认未选中。**启用所有安全增强功能(安全防护加固型沙盒选项)** 控件会将其显示为已选中，并禁用该独立复选框，因为 `UseSecurityMode=y` 已经启用了该行为。在选中设备限制期间，规则特异性复选框同样显示为已选中并被禁用；这种显示并不表示会保存单独的 `UseRuleSpecificity=y` 条目。

*RestrictDevices* 需要具备 Sandboxie 安全增强能力的有效支持者证书。没有该证书时，当前运行时会记录一条功能可用性消息，并在约五分钟的评估期后安排终止受影响的普通进程；它并不会普遍地立即拒绝启动。

## 版本历史 {#version-history}

- Sandboxie Plus 1.0.7 / Classic 5.55.7 引入了较早的 `DeviceSecurity` 模板。
- Sandboxie Plus 1.3.0 / Classic 5.58.0 以 `RestrictDevices=y` 设置取代了它，并引入了当前与安全强化模式的关系。
- Sandboxie Plus 1.7.1 / Classic 5.62.1 修复了与 `BlockNetworkFiles=y` 的交互问题。
- Sandboxie Plus 1.8.0 / Classic 5.63.0 将内置访问规则移入模板节。当前的设备规则位于内部 `[TemplateSModPaths]` 节，而不是已弃用的 `Template_DeviceSecurity` 模板。

## 相关页面 {#related-pages}

- [Sandboxie Ini](SandboxieIni.md)
- [安全强化模式](../PlusContent/security-mode.md)
- [规则特异性](../PlusContent/RuleSpecificity.md)
- [标准文件路径](NormalFilePath.md)
- [阻止网络文件访问](BlockNetworkFiles.md)
