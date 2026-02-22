# 无安全过滤

_NoSecurityFiltering_ 是沙盘配置（[Sandboxie Ini](SandboxieIni.md)）中的一个沙箱设置，自 v1.0.0 / 5.55.0 起可用。该设置在应用程序隔离（[Application Compartment](../PlusContent/compartment-mode.md)）模式下，禁用所有剩余的安全过滤机制，从而实现最大兼容性，但几乎失去了所有安全防护。

## 前提条件

> [!IMPORTANT]
> `NoSecurityFiltering` 仅在**[NoSecurityIsolation](NoSecurityIsolation.md)**也被启用时才起作用。该设置在标准沙箱模式下无效。

## 使用方法

```ini
[DefaultBox]

NoSecurityFiltering=y
```

## 语法

```ini
NoSecurityFiltering=<y/n>
```

其中：

- `y` 禁用所有安全过滤（仅在应用程序隔离模式下有效）
- `n`（默认）保持标准的过滤机制

## 与各类过滤设置的交互

`NoSecurityFiltering` 作为主控设置，会启用各独立过滤禁用选项：

- **[DisableFileFilter](DisableFileFilter.md)**：禁用文件过滤（对文件与 `NoSecurityFiltering` 同效）
- **[DisableKeyFilter](DisableKeyFilter.md)**：禁用注册表过滤（对注册表与 `NoSecurityFiltering` 同效）
- **[DisableObjectFilter](DisableObjectFilter.md)**：禁用对象过滤（对对象与 `NoSecurityFiltering` 同效）

当设置 `NoSecurityFiltering=y` 时，三项独立的禁用设置会自动激活[^1][^2][^3]

## 用户界面集成

在 Sandboxie Plus 中，此设置显示为：

- **复选框**：”Disable Security Filtering (not recommended)”[^1]
- **位置**：沙箱选项 > 安全选项 > 沙箱隔离
- **可用性**：仅在“Disable Security Isolation”被勾选时可用[^2]

## 使用场景

此极端配置可用于以下情况：

- **旧版软件**：存在严重兼容性问题的应用程序
- **开发工具**：需无障碍访问系统资源的构建系统
- **系统工具**：必须访问主机资源的管理工具
- **测试场景**：需要验证应用程序在无任何限制下的行为

## 调试与开发场景

`NoSecurityFiltering` 适用于：

- **诊断兼容性问题**：判断过滤机制是否导致程序出错
- **开发测试**：运行需无限制访问的开发工具
- **旧程序支持**：支持不兼容任何过滤的应用程序

## 相关设置

### 替代的细化控制

如果不希望全部禁用过滤，可考虑下列独立选项：

- **[DisableFileFilter](DisableFileFilter.md)**：仅禁用文件系统过滤
- **[DisableKeyFilter](DisableKeyFilter.md)**：仅禁用注册表过滤
- **[DisableObjectFilter](DisableObjectFilter.md)**：仅禁用对象过滤

[^1]: UI 选项在 `OptionsWindow.ui`：复选框文本为 “Disable Security Filtering (not recommended)” 明确提示安全影响并不建议随意启用

[^2]: UI 依赖在 `OptionsAdvanced.cpp`：代码 `ui.chkNoSecurityFiltering->setEnabled(ui.chkNoSecurityIsolation->isChecked());` 确保仅当已启用 NoSecurityIsolation 时才可启用 NoSecurityFiltering，从而落实应用程序隔离模式前提