# Privacy Mode

**NOTE: This feature requires a [supporter certificate](https://sandboxie-plus.com/supporter-certificate/).**

The concept of privacy mode and privacy enhanced (or Data Protection) boxes was introduced in **Sandboxie Plus v1.0.0**.
In this mode, most of the locations on a PC are set to be treated like a Write[File/Key]Path, which means the sandboxed locations are writable, but the unsandboxed locations are not readable.
In addition, the registry does not allow reading of user root keys. In other words, even though sandboxed processes can continue to work, they cannot access private user data.

The setting for a privacy enhanced box can be enabled by adding `UsePrivacyMode=y` to the box settings section of **[Sandboxie Ini](../Content/SandboxieIni.md)**. It can also be enabled in the Sandman UI. Right-click on a box and select "Sandbox Options" from the drop-down menu (or simply double-click on a box) to bring up the Box Options UI. Select the box type preset as "Sandbox with Data Protection" (with a **blue** box icon) and click OK to apply changes. The status column of Sandman UI labels this box as **Privacy Enhanced**.

![](../Media/Box_PrivacyMode.png)

**What is User Space?** AppGuard refers to [user space](https://malwaretips.com/threads/run-by-smartscreen-utility.65145/post-561364) as "computer storage space that is typically accessible by non-admin Windows users. It contains the user's pr# 隐私模式

**注意：此功能需要 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)。**

隐私模式以及增强隐私（或数据保护）沙盒的概念是在 **Sandboxie Plus v1.0.0** 中引入的。在该模式下，计算机上的大多数位置都被设置为类似于 Write[File/Key]Path，也即沙盒内的位置可写，但非沙盒位置不可读。

此外，注册表不允许读取用户根密钥。换句话说，即使沙盒中的进程可以继续工作，但它们无法访问用户的私人数据。

要启用增强隐私沙盒，可在 **[Sandboxie Ini](../Content/zh_CN/SandboxieIni.md)** 文件的沙盒设置部分添加 `UsePrivacyMode=y` 。也可以在 Sandman 用户界面中启用。右键点击沙盒并从下拉菜单选择“沙盒选项”（或直接双击沙盒），即可打开沙盒选项界面。将沙盒类型预设为“带数据保护的沙盒”（带有**蓝色**沙盒图标），点击 OK 以应用更改。Sandman 用户界面的状态列会将该沙盒标记为 **隐私增强**。

![](../Media/Box_PrivacyMode.png)

**什么是用户空间？** AppGuard 将 [用户空间](https://malwaretips.com/threads/run-by-smartscreen-utility.65145/post-561364) 定义为“通常可供非管理员 Windows 用户访问的计算机存储空间。它包含用户的配置文件目录（包括我的文档文件夹和桌面），可移动存储设备，网络共享，以及所有非系统硬盘（例如额外的外部和内部磁盘驱动器）”。可以将“用户空间”视为**系统**之外的所有内容（即核心操作系统和程序所在位置之外），换句话说，就是 `C:\Windows`、`C:\Program Files` 和 `C:\Program Files (x86)` 文件夹之外的空间。

在内部机制上，增强隐私沙盒基于以下三个默认原则：

1. **允许读取系统资源：**

    - `C:\Windows`
    - `C:\Program Files`
    - `C:\Program Files (x86)`
    - `C:\ProgramData\Microsoft`（自 **Sandboxie Plus v1.12.7** 起）
    - 注册表中 HKLM 下的资源（但不包括 HKCU）可读并可被沙盒隔离
    - **注意：**读取权限在隐私与便捷之间提供了良好的平衡。当然，也可以进一步梳理并对可能泄露私人数据的特定系统资源进行更严格的限制（通过 `Write[File/Key]Path` 实现）

2. **隐藏（并阻止访问）用户空间：**

    - 在用户空间内，隐私沙盒以**默认阻止**模式运行：所有驱动器路径均被设置为 WriteFilePath。这会隐藏沙盒外的所有文件和文件夹，但允许在沙盒内新建文件和文件夹（除非被覆盖规则特别允许）。选定路径的访问可以通过 [规则特异性](../PlusContent/RuleSpecificity.md) 机制实现

3. **启用 [规则特异性](../PlusContent/zh_CN/RuleSpecificity.md)：**

    - 在隐私模式下，规则特异性机制**始终启用**。它使用 **[Normal](../Content/zh_CN/NormalFilePath.md)** 路径指令（`Normal[File/Ipc/Key]Path`）将选中的路径设置为**可读且可被沙盒隔离**。需要注意的是，仅当父路径首先被设置为其他类型（如隐私模式中所做）时，将路径设置为 标准 才有意义。这不仅适用于**蓝色**箱体（基于隐私模式），也适用于**红色**箱体（同时启用了隐私模式**和**[安全模式](../PlusContent/zh_CN/security-mode.md)）

**最近更新：**在最初引入隐私模式时，系统提供了一些常见浏览器和应用程序的内置访问规则，并在后续版本中进行了增强。从 **Sandboxie Plus v1.8.0** 起，所有内置访问规则已迁移至一组默认模板（包含在 **Templates.ini** 文件的 `[TemplatePModPaths]` 部分），以便更加便捷地进行管理ofile directory (which includes the My Documents folder and Desktop), removable storage devices, network shares, and all non-system hard drives such as additional external and internal disk drives." Think of "user space" as everything outside the **system** (where the core operating system and programs live), in other words, outside the `C:\Windows`, `C:\Program Files`, and `C:\Program Files (x86)` folders!

Internally, a privacy enhanced box is based on three defaults:

1. **Allow read access to system resources:**

    - `C:\Windows`
    - `C:\Program Files`
    - `C:\Program Files (x86)`
    - `C:\ProgramData\Microsoft` (since **Sandboxie Plus v1.12.7**)
    - Registry resources under HKLM (but not HKCU) are readable and can be sandboxed.
    - **Note:** The read access provides a good balance between privacy and convenience. One could, of course, drill down to identify selected system resources that may leak private data and further restrict them (using `Write[File/Key]Path`) if desired.

2. **Hide (and block access to) user space:**

    - In user space, a privacy box works in **default block** mode: all drive paths are set to WriteFilePath. This hides all files and folders outside the sandbox, but allows new files and folders to be created in the sandbox (unless specifically allowed by an overriding rule). Access to selected paths is enabled by invoking [Rule Specificity](../PlusContent/RuleSpecificity.md).

3. **Enable [Rule Specificity:](../PlusContent/RuleSpecificity.md)**

    - Internally, rule specificity is **always enabled** in privacy mode. It uses the **[Normal](../Content/NormalFilePath.md)** path directive (`Normal[File/Ipc/Key]Path`) to open selected locations to be **readable and sandboxed**. Note that setting a path to normal is meaningful only when a parent path was first set to something else, as done in privacy mode. It is thus relevant not only for **blue**  boxes (based on privacy mode) but also for **red** boxes (with both privacy mode **and** [security mode](../PlusContent/security-mode.md) enabled).

**Recent Changes:** Upon the introduction of privacy mode, a few built-in access rules were offered for some of the more common browsers and applications and these were augmented in later versions. Starting with **Sandboxie Plus v1.8.0**, all built-in access rules have been moved to a set of default templates (included in the file **Templates.ini** under the `[TemplatePModPaths]` section) for easier management.
