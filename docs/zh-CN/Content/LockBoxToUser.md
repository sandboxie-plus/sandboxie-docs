# 将沙盒锁定到用户

_LockBoxToUser_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项设置，自 v1.15.0 / 5.70.0 起可用。它控制 Sandboxie 是否把沙盒文件夹的访问限制为仅限创建沙盒的用户。

## 用法

```ini
[GlobalSettings]

LockBoxToUser=y
```

默认情况下（未指定 `LockBoxToUser` 或设为 `n`），Sandboxie 创建带 ACL[^1] 的沙盒文件夹，允许系统上所有经过身份验证的用户访问。这意味着任何登录用户都可能访问其他用户创建的沙盒文件夹中存储的文件。

指定 `LockBoxToUser=y` 时，Sandboxie 创建的沙盒文件夹带更严格的 ACL，只允许以下对象访问：

- 创建沙盒的用户。
- SYSTEM 帐户[^2]。
- 管理员组[^3]。

此设置通过防止未授权访问沙盒内容，增强了多用户环境中的安全性和隐私性。

## 安全考虑

此设置是为了解决一个安全漏洞（[CVE-2024-49360](https://github.com/sandboxie-plus/Sandboxie/security/advisories/GHSA-4chj-3c28-gvmp)）而引入的，该漏洞中沙盒文件可被系统上的所有用户访问。

> [!IMPORTANT]
> 要使此设置生效，请确保你的沙盒根文件夹路径包含 `%USER%` 宏，以便每个用户获得专用的沙盒文件夹。默认路径 `\??\%SystemDrive%\Sandbox\%USER%\%SANDBOX%` 包含此宏，推荐用于多用户系统。

## 实现细节

启用 `LockBoxToUser=y` 时，Sandboxie 会修改安全描述符创建过程[^4]，使用更严格的一组 SID：

- **系统登录 SID**（`S-1-5-18`）：允许 SYSTEM 帐户访问。
- **管理员 SID**（`S-1-5-32-544`）：允许本地管理员访问。
- **用户 SID**：允许创建用户访问。

禁用时，标准行为授予以下对象访问：

- **经过身份验证的用户 SID**（`S-1-5-11`）：允许所有经过身份验证的用户访问。
- **用户 SID**：允许创建用户访问。

[^1]: 访问控制列表（ACL）是 Windows 安全结构，定义哪些用户和组可以访问特定资源以及他们拥有什么权限。它们是控制对文件、文件夹、注册表项和其他对象访问的 Windows 安全模型的一部分。

[^2]: SYSTEM 帐户（SID `S-1-5-18`）是本地计算机上拥有最高权限的内置 Windows 帐户。Sandboxie 在此帐户下运行核心组件，需要访问沙盒文件夹才能正常运行。

[^3]: 管理员组（SID `S-1-5-32-544`）包含在计算机上拥有管理权限的用户帐户。该组成员可以出于系统维护和故障排除目的访问沙盒文件夹。

[^4]: 安全描述符创建在 `secure.c` 的 `Secure_InitSecurityDescriptors()` 函数中处理，它查询 `LockBoxToUser` 配置设置，并根据其值创建不同的 ACL 结构。启用时，它创建带受限 SID 的 512 字节 ACL，而非默认的带更宽访问权限的 256 字节 ACL。
