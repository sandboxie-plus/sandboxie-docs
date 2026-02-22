# 将沙箱锁定到用户

_LockBoxToUser_ 是自 v1.15.0 / 5.70.0 起在 [沙盘配置](SandboxieIni.md) 中可用的一个设置。该设置用于控制沙盘是否仅允许创建沙箱的用户访问沙箱文件夹。

## 使用方法

```ini
[GlobalSettings]

LockBoxToUser=y
```

默认情况下（未指定 `LockBoxToUser` 或设置为 `n` 时），沙盘会使用允许系统内所有已验证用户访问的 ACLs[^1] 来创建沙箱文件夹。这意味着任何已登录用户都可能访问其他用户创建的沙箱文件夹中的文件。

当指定 `LockBoxToUser=y` 时，沙盘会创建更加严格的 ACLs，只允许以下账户访问：

- 创建沙箱的用户
- SYSTEM 账户[^2]
- Administrators 组[^3]

该设置在多用户环境下增强了安全性和隐私性，能够防止未授权用户访问沙箱内容。

## 安全性考虑

该设置旨在解决一个安全漏洞（[CVE-2024-49360](https://github.com/sandboxie-plus/Sandboxie/security/advisories/GHSA-4chj-3c28-gvmp)），该漏洞使得系统上的所有用户都能访问沙箱内的文件。

> [!IMPORTANT]
> 为确保此设置有效，请确保您的沙箱根文件夹路径包含 `%USER%` 宏，这样每个用户都能拥有独立的沙箱文件夹。默认路径 `\??\%SystemDrive%\Sandbox\%USER%\%SANDBOX%` 已包含该宏，推荐在多用户系统中使用。

## 实现细节

启用 `LockBoxToUser=y` 时，沙盘会修改安全描述符生成过程[^4]，采用更为严格的 SID 集合：

- **System Logon SID** (`S-1-5-18`)：允许 SYSTEM 账户访问
- **Administrators SID** (`S-1-5-32-544`)：允许本地管理员访问
- **用户 SID**：允许创建沙箱的用户访问

禁用该选项时，标准行为会允许以下账户访问：

- **Authenticated Users SID** (`S-1-5-11`)：允许所有已验证用户访问
- **用户 SID**：允许创建沙箱的用户访问

[^1]: 访问控制列表（ACLs）是 Windows 的安全结构，用于定义哪些用户和组可以访问特定资源以及他们拥有的权限。它们是 Windows 安全模型的一部分，用于控制对文件、文件夹、注册表项和其他对象的访问。

[^2]: SYSTEM 账户（SID `S-1-5-18`）是 Windows 内置的账户，拥有本地计算机最高权限。沙盘的核心组件在该账户下运行，并需要对沙箱文件夹进行访问以确保正常运作。

[^3]: Administrators 组（SID `S-1-5-32-544`）包含具有计算机管理员权限的用户账户。该组成员可以访问沙箱文件夹，以便进行系统维护和故障排查。

[^4]: 安全描述符生成由 `Secure_InitSecurityDescriptors()` 函数在 `secure.c` 中处理。该函数会查询 `LockBoxToUser` 配置项，并根据其值生成不同的 ACL 结构。启用时，会创建一个包含受限 SID 的 512 字节 ACL，而默认情况下则生成包含更广泛访问权限的 256 字节 ACL。