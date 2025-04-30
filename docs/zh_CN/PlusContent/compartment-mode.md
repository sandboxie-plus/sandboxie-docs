# 隔离模式

**注意：此功能需要 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)。**

“应用隔离区”模式的概念首次在 **Sandboxie Plus v1.0.0** 中引入。启用此模式后，原本用于安全隔离的基于令牌的机制会被禁用，从而大幅提升兼容性，同时依然保留与其他同类沙箱产品相当的安全性。此举避免了许多因进程运行于深度受限令牌下而导致的典型 Sandboxie 问题。

可以通过在 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的沙箱设置部分添加 `NoSecurityIsolation=y` 来启用沙箱应用隔间设置。同样地，也可在 Sandman 用户界面（UI）内启用。只需右键点击某个沙箱，从下拉菜单中选择 “沙箱选项”（或直接双击该沙箱）即可打开沙箱选项。将沙箱类型预设选择为 “应用隔间（无隔离）”（标识为**绿色**沙箱图标），然后点击 OK 应用更改。在 Sandman UI 的状态栏中，该沙箱会被标记为 **应用隔间**。

![](../Media/Box_CompartmentMode.png)

在隔离模式下，文件系统和注册表的过滤依然有效，以强制执行各项访问规则。因此，进程在运行时不会拥有管理员权限。若需进一步提升兼容性，可以通过在 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的沙箱设置部分添加 `NoSecurityFiltering=y` 来禁用该过滤。

自 **Sandboxie Plus v1.0.16** 起，新安装默认启用全新对象访问过滤器，对进程隔离起到辅助作用，替代了 Sandboxie 旧有的进程/线程句柄过滤。如需在 **Sandboxie Plus v1.0.0** 起的早期版本中启用该功能，可在 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的 [GlobalSettings] 部分添加 `EnableObjectFiltering=y`。

**注意：** 虽然应用隔间会虚拟化文件系统和注册表，但并不会更改进程令牌，也不会施加其他更严格的限制。因此，进程有可能逃离虚拟环境。鉴于安全性有一定（尽管仅为轻微）的降低，**对不受信任的应用程序应避免使用此模式**。

**近期变更：** 后续的 Sandboxie Plus 版本引入了基于令牌的兼容性解决方案，以进一步提升与常见程序的兼容性。这些方案采用 `DropAppContainerToken=y` 实现，若需对某一特定程序禁用此方案，则可使用 `FakeAppContainerToken=program.exe,n`。在 **Sandboxie Plus v1.8.2a** 及更高版本中，隔离模式下默认禁用这些兼容性方案。如果某些程序（主要为浏览器）出现问题，可通过添加 `DeprecatedTokenHacks=y` 来重新启用这些方案。**Sandboxie Plus v1.8.0** 将应用隔间沙箱的内建访问规则迁移到专用模板（包含于 **Templates.ini** 文件的 `[TemplateAppCPaths]` 部分）中，以便于管理。**Sandboxie Plus v1.10.1** 修复并完善了长期存在的影响应用隔间沙箱的各种 bug。

**趣闻（适用于任何沙箱类型）：** 如果你在 **[Sandboxie Ini](../Content/SandboxieIni.md)** 的沙箱设置部分添加 `OpenFilePath=*`（或以其他方式禁用隔离），Sandman UI 的状态栏会显示 **OPEN Root Access**，以警示该沙箱已不再是真正意义上的“沙箱”！自 **Sandboxie Plus v1.3.2** 起，沙箱图标的默认颜色也会相应变化。
