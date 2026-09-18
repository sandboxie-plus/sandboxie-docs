# 启用 EFS

_EnableEFS_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.15.0 / 5.70.0 起可用。它允许沙盒化进程访问受 Windows 加密文件系统（EFS）保护的文件。

> [!NOTE]
> 此设置需要有效的进阶 [支持者证书](https://sandboxie-plus.com/supporter-certificate/)[^1]。

## 用法

```ini
[DefaultBox]

EnableEFS=y
```

## 通过 Sandboxie Manager 图形界面启用

你可以通过以下步骤，在 Sandboxie Manager（又称沙盒管理器）中为特定沙盒（或 DefaultBox）启用此设置：

1. 打开沙盒管理器。
2. 右键点击要配置的沙盒，选择"沙盒选项"。
3. 在设置对话框中，选择左侧的"文件选项"类别。
4. 切换到"文件选项"选项卡组（顶部选项卡），滚动到"磁盘/文件访问"部分。
5. 勾选标记为"允许沙盒化进程打开受 EFS 保护的文件"的选项。
6. 点击"应用"或"确定"保存设置。

这对应 [Sandboxie.Ini](SandboxieIni.md) 沙盒节中的 `EnableEFS=y` 设置，但在通过图形界面配置单个沙盒时更方便。

## 概述

加密文件系统（EFS）是 Windows 的一项功能，提供文件系统级加密。默认情况下，Sandboxie 会阻止沙盒化进程访问 EFS 加密的文件和文件夹，以保持安全隔离。`EnableEFS` 设置允许你在需要时覆盖此限制。

## 工作原理

当启用 `EnableEFS` 时：

1. **EFS 检测**：Sandboxie 检测沙盒化进程何时尝试访问 EFS 加密的文件或文件夹[^2]
2. **证书验证**：系统验证是否存在带加密功能的有效进阶支持者证书[^3]
3. **代理访问**：Sandboxie 不是阻止访问，而是使用代理机制在沙盒外处理文件操作[^4]
4. **句柄复制**：文件句柄在 UserServer 服务中创建，然后复制回沙盒化进程[^5]

## 安全注意事项

- **隔离减弱**：启用 EFS 访问会降低沙盒的安全隔离，因为它允许直接访问通常会被阻止的加密文件
- **路径验证**：代理服务在允许操作之前，会验证请求的文件路径是否匹配配置的访问规则[^6]
- **写访问控制**：对 EFS 文件的写操作会根据沙盒的文件访问配置接受额外验证[^7]

## 证书要求

此功能需要包含加密功能标志（`opt_enc`）的进阶支持者证书[^8]。没有此证书，尝试使用 EFS 将导致错误消息 `SBIE6004`。

## 相关消息

- [SBIE2225](SBIE2225.md) - "尝试访问 EFS 文件" - EFS 访问失败时记录的警告[^9]
- [SBIE6004](SBIE6004.md) - 缺少进阶支持者证书时的证书要求错误

## 限制

- 仅适用于硬盘卷上的文件（路径以 `\Device\HarddiskVolume` 开头）[^10]。
- 受沙盒的文件 [资源访问规则](ResourceAccess.md) 约束（`OpenFilePath`、`ClosedFilePath` 等）。

[^1]: 证书验证在 `UserServer::OpenFile()` 方法中执行，检查 `CertInfo.active && CertInfo.opt_enc`
[^2]: EFS 文件检测发生在 `File_NtCreateFile12()` 中，通过检查 `(FileType & TYPE_EFS) != 0`，其中 `TYPE_EFS` 定义为 `FILE_ATTRIBUTE_ENCRYPTED`
[^3]: 证书检查验证证书既处于活动状态又设置了加密选项标志：`!(CertInfo.active && CertInfo.opt_enc)`
[^4]: EFS 代理机制通过 `File_NtCreateFileProxy()` 实现，它通过 `SbieDll_CallProxySvr()` 向 UserServer 服务发送请求
[^5]: 句柄复制在 UserServer 中使用 `DuplicateHandle()` 执行，把文件句柄从服务进程转移到沙盒化进程
[^6]: UserServer 中的路径验证检查路径以 `\Device\HarddiskVolume` 开头，并使用 `SbieDll_MatchPathImpl()` 对照文件访问规则验证
[^7]: 写访问验证检查与写相关的访问标志、`FILE_OPEN` 以外的创建处置，以及 `FILE_DELETE_ON_CLOSE` 选项
[^8]: 加密功能标志 `opt_enc` 在证书验证结构中定义为 Box 加密和 Box 保护功能的一部分
[^9]: 当 `File_NtCreateFileProxy()` 以 `SbieApi_Log(2225, TruePath)` 失败时记录错误
[^10]: 设备路径限制通过在 UserServer 中检查 `_wcsnicmp(path_buff, L"\\Device\\HarddiskVolume", 22) != 0` 实现
