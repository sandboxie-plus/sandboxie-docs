# 使用原始 ACL

_UseOriginalACLs_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.15.0 / 5.70.0 起可用。此设置在文件或文件夹被复制或创建到沙盒内时保留其原始访问控制列表（ACL），而不是应用 Sandboxie 的默认安全描述符。启用后，文件保持其原始安全权限，同时把当前用户以完全访问权限添加到 ACL。

## 用法

```ini
[DefaultBox]

UseOriginalACLs=y
```

## 技术细节

设置 `UseOriginalACLs=y` 时，Sandboxie 会在几个关键领域修改其文件操作行为：

1. **文件创建**：系统不使用标准的 `Secure_NormalSD` 安全描述符，而是从原始文件位置复制安全描述符，并把当前用户以完全访问权限添加进去[^1]。

2. **目录创建**：创建目录时，系统查询源目录的安全描述符，并将其应用于沙盒副本，同时确保当前用户有权访问[^2]。

3. **文件复制**：在文件复制操作期间，常规文件与重解析点（符号链接、交接点）都保留其原始安全描述符[^3]。

## 安全影响

- **增强兼容性**：依赖特定 ACL 配置的应用程序可以在沙盒内正常运行
- **MSI 安装程序支持**：对需要特定 ACL 权限的 MSI 安装程序尤其有益（因此界面有关于 MSIServer 豁免的说明）
- **用户访问保证**：当前用户总是以 `GENERIC_ALL` 权限被添加到 ACL，确保沙盒功能得以维持[^4]

## 实现说明

此设置由 DLL 启动期间初始化的全局变量 `Secure_CopyACLs` 控制[^5]。激活时，系统：

- 使用 `DACL_SECURITY_INFORMATION | SACL_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION` 查询源文件安全描述符。
- 如有必要，把安全描述符复制为自相对格式。
- 为当前用户添加带继承标志 `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE` 的访问控制项（ACE）。

## 相关设置

- [MSI 安装程序豁免](MsiInstallerExemptions.md) - 常与 MSI 安装程序兼容性一起使用

[^1]: `file.c` 中的文件创建逻辑：`Secure_CopyACLs` 为真时，`File_DuplicateSecurityDescriptor` 复制原始安全描述符，`File_AddCurrentUserToSD` 把当前用户以完全权限添加进去。

[^2]: `file.c` 中的目录创建：系统以 `FILE_READ_ATTRIBUTES` 打开源目录，查询其安全描述符，并在添加当前用户访问权限后将其应用于新目录。

[^3]: `file_copy.c` 中的文件复制操作：常规文件复制和重解析点复制都通过 `NtQuerySecurityObject` 查询源安全描述符来保留原始 ACL。

[^4]: `file.c` 中的 ACL 修改：`RtlAddAccessAllowedAceEx` 把当前用户以 `GENERIC_ALL` 权限和继承标志 `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE` 添加进去。

[^5]: `secure.c` 中的初始化：`Secure_CopyACLs = SbieApi_QueryConfBool(NULL, L"UseOriginalACLs", FALSE)` 在 DLL 初始化期间设置全局变量。
