# 使用原始 ACL

_UseOriginalACLs_ 是 [沙盘配置](SandboxieIni.md) 中的一个沙箱设置，自 v1.15.0 / 5.70.0 版本起可用。该设置在文件和文件夹被复制或创建到沙箱时，保留其原始访问控制列表（ACL），而不是应用沙盘的默认安全描述符。启用后，文件将保持其原有的安全权限，同时为当前用户添加具有完全访问权限的 ACL 项。

## 用法

```ini
[DefaultBox]

UseOriginalACLs=y
```

## 技术细节

当设置为 `UseOriginalACLs=y` 时，沙盘在多个关键环节修改了其文件操作行为：

1. **文件创建**：不再使用标准的 `Secure_NormalSD` 安全描述符，系统会从原始文件位置复制安全描述符，并为当前用户添加完全访问权限[^1]

2. **目录创建**：创建目录时，系统会查询源目录的安全描述符，并将其应用到沙箱中的副本，并确保当前用户具有访问权限[^2]

3. **文件复制**：在文件复制操作过程中，普通文件和重解析点（符号链接、挂载点）的原始安全描述符均会被保留[^3]

## 安全影响

- **增强兼容性**：依赖特定 ACL 配置的应用程序能够在沙箱中正常运行
- **支持 MSI 安装程序**：特别适用于需要特殊 ACL 权限的 MSI 安装程序（因此界面中有关于 MSIServer 例外的提示）
- **保证用户访问**：始终为当前用户添加 `GENERIC_ALL` 权限的 ACL 项，确保沙箱功能得以维护[^4]

## 实现说明

该设置由全局变量 `Secure_CopyACLs` 控制，该变量在 DLL 启动期间初始化[^5]。启用后，系统将：

- 使用 `DACL_SECURITY_INFORMATION | SACL_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION` 查询源文件的安全描述符
- 如有必要，将安全描述符转换为自相关格式
- 为当前用户添加包含继承标志 `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE` 的访问控制项（ACE）

## 相关设置

- [MsiInstallerExemptions](MsiInstallerExemptions.md) - 常与本设置配合使用，以提升 MSI 安装程序的兼容性

[^1]: `file.c` 中的文件创建逻辑：当 `Secure_CopyACLs` 为 true 时，`File_DuplicateSecurityDescriptor` 复制原始安全描述符，`File_AddCurrentUserToSD` 为当前用户添加完全权限

[^2]: `file.c` 中的目录创建：系统以 `FILE_READ_ATTRIBUTES` 权限打开源目录，查询其安全描述符，并在为新目录添加当前用户访问后应用

[^3]: `file_copy.c` 中的文件复制操作：普通文件和重解析点复制时，通过 `NtQuerySecurityObject` 查询源安全描述符，保留原始 ACL

[^4]: `file.c` 中的 ACL 修改：`RtlAddAccessAllowedAceEx` 为当前用户添加 `GENERIC_ALL` 权限及 `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE` 继承标志的访问控制项

[^5]: `secure.c` 中的初始化：`Secure_CopyACLs = SbieApi_QueryConfBool(NULL, L"UseOriginalACLs", FALSE)` 在 DLL 初始化期间设置该全局变量