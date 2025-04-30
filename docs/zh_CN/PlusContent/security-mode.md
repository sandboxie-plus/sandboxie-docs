# 安全强化模式

**注意：此功能需要 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)。**

安全强化沙箱和安全强化模式的概念在 **Sandboxie Plus v1.3.0** 中引入。它将 NT 系统调用提升限制为已批准的已知安全/经过过滤的系统调用。它还通过将设备访问限制为已知安全/经过过滤的端点来提供设备安全性。

可以通过在 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的沙箱设置部分添加 `UseSecurityMode=y` 来启用安全强化沙箱的设置。也可以在 Sandman 用户界面中启用该设置。右键单击一个沙箱，然后从下拉菜单中选择“沙箱选项”（或者直接双击一个沙箱）以打开沙箱选项用户界面。选择沙箱类型预设为“安全强化沙箱”（带有 **橙色** 沙箱图标），然后单击“确定”以应用更改。Sandman 用户界面的状态列将此沙箱标记为 **增强隔离**。

![](../Media/Box_SecurityMode.png)

在内部，安全强化模式基于以下四个设置：

```
DropAdminRights=y
RestrictDevices=y
SysCallLockDown=y
UseRuleSpecificity=y
```

1. **[DropAdminRights](../Content/DropAdminRights.md)：** 在 **Sandboxie Plus v1.3.0** 之前，任何设置了 `DropAdminRights=y` 的沙箱都被视为 **强化** 沙箱，并在 Sandman 用户界面的状态列中标记为“增强隔离”。从 **Sandboxie Plus v1.3.0** 开始，只有设置了 `UseSecurityMode=y` 的沙箱其状态才会显示为“增强隔离”。

2. **SysCallLockDown：** 设置 `SysCallLockDown=y` 会限制 NT 系统调用的使用。只有那些包含在 **Templates.ini** 文件中的默认调用，或者在 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的 `[GlobalSettings]` 部分配置为 `ApproveWinNtSysCall=...` 或 `ApproveWin32SysCall=...` 的调用，才会使用原始令牌执行。任何未获批准的 NT 系统调用将使用沙箱化令牌执行，这在某些情况下可能会破坏兼容性。要找出使特定程序正常运行所需的系统调用是一项繁琐的工作，需要反复试验。但一旦找到这些系统调用，就可以将它们添加到 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的 `[GlobalSettings]` 部分。请注意，**必须使用“选项 -> 重新加载配置”来重新加载配置，这些设置才能生效**。

3. **RestrictDevices：** 在 **Sandboxie Plus v1.3.0** 中，早期的 **“DeviceSecurity”** 模板被专门的设置 `RestrictDevices=y` 所取代，以进一步强化沙箱的安全性。安全增强型沙箱无法访问主机上安装的驱动程序。但是，使用适当的 **[Normal](../Content/NormalFilePath.md)** 路径指令可以根据需要允许打开特定设备。

4. **[规则特异性](../PlusContent/RuleSpecificity.md)：** 设置 `UseRuleSpecificity=y` 允许根据规则的“特异性”对规则进行优先级排序。当规则特异性与 `Normal[File/Key/Ipc]Path` 条目结合使用时，可以使选定的子路径可读写，同时父路径仍然受到保护。安全强化沙箱以 **默认允许** 模式工作：每个路径都是 `Normal[File/Key/Ipc]Path`（允许对沙箱进行读写更改），除非被覆盖规则专门阻止。

**与其他沙箱类型的比较：** 规则特异性以及 `Normal[File/Key/Ipc]Path` 条目也用于 **蓝色**（[隐私增强](../PlusContent/privacy-mode.md)）沙箱和 **红色** 沙箱（结合了增强的隐私和增强的安全性）。这两种沙箱类型以 **默认阻止** 模式工作：所有驱动器路径都设置为 `WriteFilePath`。这会隐藏沙箱外部的所有文件和文件夹，但允许在沙箱中创建新的文件和文件夹（除非被覆盖规则专门允许）。

**近期更改：** 从 **Sandboxie Plus v1.8.0** 开始，安全强化沙箱的所有内置访问规则都已移至一个专门的模板（包含在 **Templates.ini** 文件的 `[TemplateSModPaths]` 部分）中，以便于管理。
