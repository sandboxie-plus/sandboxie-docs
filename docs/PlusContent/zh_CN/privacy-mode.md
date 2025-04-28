# 隐私模式

**注意：此功能需要 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)。**

隐私模式和隐私增强（或数据保护）沙箱的概念在 **Sandboxie Plus v1.0.0** 版本中引入。
在此模式下，计算机上的大多数位置被设置为像 Write[File/Key]Path 那样处理，这意味着沙箱内的位置可写，但沙箱外的位置不可读。
此外，注册表不允许读取用户根键。换句话说，即使沙箱内的进程可以继续运行，它们也无法访问用户的私人数据。

要启用隐私增强沙箱的设置，可以在 **[Sandboxie 配置文件](../Content/zh_CN/SandboxieIni.md)** 的沙箱设置部分添加 `UsePrivacyMode=y`。也可以在 Sandman 用户界面中启用该设置。右键单击一个沙箱，从下拉菜单中选择“沙箱选项”（或者直接双击一个沙箱），以打开沙箱选项界面。选择沙箱类型预设为“带有数据保护的沙箱”（带有 **蓝色** 沙箱图标），然后点击“确定”应用更改。Sandman 用户界面的状态列会将此沙箱标记为 **隐私增强**。

![](../Media/Box_PrivacyMode.png)

**什么是用户空间？** AppGuard 将 [用户空间](https://malwaretips.com/threads/run-by-smartscreen-utility.65145/post-561364) 定义为“通常可供非管理员 Windows 用户访问的计算机存储空间。它包含用户的配置文件目录（包括我的文档文件夹和桌面）、可移动存储设备、网络共享以及所有非系统硬盘，如额外的外部和内部磁盘驱动器”。可以将“用户空间”视为 **系统** 之外的所有内容（即核心操作系统和程序所在的位置之外），换句话说，就是 `C:\Windows`、`C:\Program Files` 和 `C:\Program Files (x86)` 文件夹之外的所有内容！

从内部实现来看，隐私增强沙箱基于三个默认设置：

1. **允许对系统资源进行读取访问：**

    - `C:\Windows`
    - `C:\Program Files`
    - `C:\Program Files (x86)`
    - `C:\ProgramData\Microsoft`（从 **Sandboxie Plus v1.12.7** 版本开始）
    - HKLM（但不包括 HKCU）下的注册表资源是可读的，并且可以进行沙箱化处理。
    - **注意：** 这种读取访问在隐私和便利性之间取得了良好的平衡。当然，如果需要，用户可以进一步细化，识别出可能泄露私人数据的特定系统资源，并使用 `Write[File/Key]Path` 进一步限制访问。

2. **隐藏（并阻止访问）用户空间：**

    - 在用户空间中，隐私沙箱以 **默认阻止** 模式工作：所有驱动器路径都被设置为 WriteFilePath。这会隐藏沙箱外的所有文件和文件夹，但允许在沙箱内创建新的文件和文件夹（除非有覆盖规则特别允许访问）。可以通过调用 [规则特异性](../PlusContent/zh_CN/RuleSpecificity.md) 来启用对特定路径的访问。

3. **启用 [规则特异性：](../PlusContent/zh_CN/RuleSpecificity.md)**

    - 在内部，隐私模式下 **始终启用** 规则特异性。它使用 **[普通](../Content/zh_CN/NormalFilePath.md)** 路径指令 (`Normal[File/Ipc/Key]Path`) 来打开特定位置，使其 **可读并可进行沙箱化处理**。请注意，只有当父路径首先被设置为其他值时，将路径设置为普通才有意义，就像在隐私模式中所做的那样。因此，这不仅适用于基于隐私模式的 **蓝色** 沙箱，也适用于同时启用了隐私模式和 [安全模式](../PlusContent/zh_CN/security-mode.md) 的 **红色** 沙箱。

**近期更改：** 隐私模式引入后，为一些常见的浏览器和应用程序提供了一些内置访问规则，并且在后续版本中进行了扩展。从 **Sandboxie Plus v1.8.0** 版本开始，所有内置访问规则都已移至一组默认模板中（包含在 **Templates.ini** 文件的 `[TemplatePModPaths]` 部分），以便于管理。
