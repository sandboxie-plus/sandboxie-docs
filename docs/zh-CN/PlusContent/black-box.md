# 黑色沙盒

**黑色沙盒**是新建沙盒向导中的一个组合选项，在保留所选基础沙盒类型的同时，启用以下两种独立的保护：

- [加密沙盒存储](BoxEncryption.md)：将沙盒根目录及注册表配置单元存放在加密磁盘镜像中。
- [保密沙盒](../Content/ConfidentialBox.md)：限制沙盒外的宿主机进程通过句柄访问沙盒内的进程和线程。

在新建沙盒向导的常规流程中，选择“加密沙盒内容并启用保密功能”会在基础配置上添加 `UseFileImage=y` 和 `ConfidentialBox=y`。这两项设置对应不同的机制：加密主要在镜像未挂载时保护其中的存储内容，保密沙盒的访问过滤则在沙盒进程运行期间生效。

基础类型可以是标准沙盒、[安全加固沙盒](security-mode.md)或[应用程序隔离沙盒](compartment-mode.md)，每种类型均可选择是否启用[数据保护](privacy-mode.md)。创建后，“沙盒类型预设配置”可在这六种基础组合之间切换；加密和保密沙盒功能则分别配置。

SandMan 可显示加密与保密的组合外观，不受基础模式限制；已有沙盒同时启用这两项设置时，也可采用该外观。向导仍根据所选基础类型设置边框颜色，不会因为启用黑色沙盒选项就将边框改为黑色。颜色和图标不能保证实际的保护效果，详见[沙盒外观](../Content/BoxPresentation.md)。

挂载后的根目录保护、[ProtectAdminOnly](../Content/ProtectAdminOnly.md)、`DenyHostAccess` 例外规则及 [ProtectHostImages](../Content/ProtectHostImages.md) 等其他控制项，各有其作用范围和默认值。

黑色沙盒并不意味着所有通信或数据传输通道都会被阻断。沙盒运行期间允许哪些操作，仍由 Sandboxie 的文件、注册表、IPC、网络、剪贴板、图形界面等常规策略决定。
