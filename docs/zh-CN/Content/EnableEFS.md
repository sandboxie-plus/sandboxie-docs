# 启用 EFS

_EnableEFS_ 是一个沙箱设置，位于 [沙盘配置](SandboxieIni.md) 文件，自 v1.15.0 / 5.70.0 起可用。它允许沙箱内的进程访问受 Windows 加密文件系统（EFS）保护的文件。

> [!NOTE]
> 此设置需要一个有效的高级 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)[^1]。

## 用法

```ini
[DefaultBox]

EnableEFS=y
```

## 通过沙盘管理器界面启用

你可以通过沙盘管理器（也称为 SandMan）为指定的沙箱（或 DefaultBox）启用此设置，步骤如下：

1. 打开 SandMan
2. 右键点击需要配置的沙箱，选择“沙箱选项”
3. 在设置对话框左侧，选择“文件选项”类别
4. 切换到顶部标签组中的“文件选项”标签页，滚动到“磁盘/文件访问”部分
5. 勾选“允许沙箱内进程打开受 EFS 保护的文件”选项
6. 点击“应用”或“确定”以保存设置

这相当于在 [沙盘.Ini](SandboxieIni.md) 文件中的沙箱区块设置 `EnableEFS=y`，但通过界面配置单个沙箱更加方便。

## 概述

加密文件系统（EFS）是 Windows 提供的文件系统级加密功能。默认情况下，沙盘会阻止沙箱内进程访问 EFS 加密的文件和文件夹，以保持安全隔离。当需要时，`EnableEFS` 设置可以允许你突破这一限制。

## 工作原理

当启用 `EnableEFS` 时：

1. **EFS 检测**：沙盘会检测沙箱内的进程是否尝试访问 EFS 加密的文件或文件夹[^2]
2. **证书验证**：系统会验证是否存在包含加密功能的有效高级支持者证书[^3]
3. **代理访问**：沙盘通过代理机制处理相关文件操作，而不是直接阻止访问[^4]
4. **句柄复制**：文件句柄在 UserServer 服务中创建后，会被复制到沙箱内的进程中[^5]

## 安全考量

- **隔离性降低**：启用对 EFS 文件的访问会降低沙箱的安全隔离性，因为允许直接访问本应被阻止的加密文件
- **路径校验**：代理服务会校验请求的文件路径是否符合已配置的访问规则后才允许操作[^6]
- **写入访问控制**：对 EFS 文件的写入操作会依据沙箱的文件访问配置进行额外校验[^7]

## 证书要求

此功能需要包含加密功能标志（`opt_enc`）的高级支持者证书[^8]。没有该证书的情况下尝试使用 EFS 会导致出现 `SBIE6004` 错误信息。

## 相关消息

- [SBIE2225](SBIE2225.md) - “尝试访问 EFS 文件”——当 EFS 访问失败时记录警告日志[^9]
- [SBIE6004](SBIE6004.md) - 在缺少高级支持者证书时出现证书要求错误

## 限制

- 仅适用于硬盘卷上的文件（路径以 `\Device\HarddiskVolume` 开头）[^10]
- 受沙箱的文件 [资源访问规则](ResourceAccess.md)（如 `OpenFilePath`、`ClosedFilePath` 等）限制

[^1]: 证书验证在 `UserServer::OpenFile()` 方法中进行，检查 `CertInfo.active && CertInfo.opt_enc`
[^2]: EFS 文件检测发生于 `File_NtCreateFile12()`，通过判断 `(FileType & TYPE_EFS) != 0`，其中 `TYPE_EFS` 定义为 `FILE_ATTRIBUTE_ENCRYPTED`
[^3]: 证书验证会同时检查证书是否有效且带有加密选项标志：`!(CertInfo.active && CertInfo.opt_enc)`
[^4]: EFS 代理机制通过 `File_NtCreateFileProxy()` 实现，通过 `SbieDll_CallProxySvr()` 向 UserServer 服务发送请求
[^5]: 在 UserServer 中使用 `DuplicateHandle()` 将文件句柄从服务进程复制到沙箱内进程
[^6]: UserServer 中的路径校验会检查路径是否以 `\Device\HarddiskVolume` 开头，并通过 `SbieDll_MatchPathImpl()` 校验文件访问规则
[^7]: 写入访问校验会检查涉及写操作的访问标志，创建动作为非 `FILE_OPEN`，以及 `FILE_DELETE_ON_CLOSE` 选项
[^8]: 加密功能标志 `opt_enc` 被定义在证书验证结构中，属于沙箱加密和沙箱保护功能的一部分
[^9]: 当 `File_NtCreateFileProxy()` 失败时，会记录日志 `SbieApi_Log(2225, TruePath)`
[^10]: 设备路径限制通过 UserServer 检查 `_wcsnicmp(path_buff, L"\\Device\\HarddiskVolume", 22) != 0` 实现