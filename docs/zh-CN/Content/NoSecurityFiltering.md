# 无安全过滤

_NoSecurityFiltering_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.0.0 / 5.55.0 起可用。此设置禁用 [应用程序隔离](../PlusContent/compartment-mode.md) 模式中所有剩余的安全过滤机制，以几乎所有安全保护为代价提供最大兼容性。

## 前提条件

> [!IMPORTANT]
> `NoSecurityFiltering` 仅在同时启用 **[无安全隔离](NoSecurityIsolation.md)** 时才起作用。此设置在标准沙盒模式中无效。

## 用法

```ini
[DefaultBox]

NoSecurityFiltering=y
```

## 语法

```ini
NoSecurityFiltering=<y/n>
```

其中：

- `y` 禁用所有安全过滤（仅在应用程序隔离模式中有效）。
- `n`（默认）保持标准过滤机制。

## 与各过滤设置的交互

`NoSecurityFiltering` 作为主覆盖开关，启用各个单独过滤禁用设置：

- **[禁用文件过滤器](DisableFileFilter.md)**：禁用文件过滤（对文件的效果与 `NoSecurityFiltering` 相同）。
- **[禁用键过滤](DisableKeyFilter.md)**：禁用注册表过滤（对注册表的效果与 `NoSecurityFiltering` 相同）。
- **[禁用对象过滤器](DisableObjectFilter.md)**：禁用对象过滤（对对象的效果与 `NoSecurityFiltering` 相同）。

设置 `NoSecurityFiltering=y` 时，三个单独禁用设置都会被自动激活[^1][^2][^3]。

## 界面集成

在 Sandboxie Plus 中，此设置显示为：

- **复选框**："禁用安全过滤（不推荐）"[^1]。
- **位置**：沙盒选项 > 安全选项 > 沙盒隔离。
- **可用性**：仅在勾选"禁用安全隔离"时可用[^2]。

## 使用场景

这种极端配置可能对以下情况合理：

- **旧软件**：有严重兼容性问题的应用程序。
- **开发工具**：需要不受限制的系统访问的构建系统。
- **系统实用程序**：必须访问宿主资源的管理工具。
- **测试场景**：当你需要在没有任何限制的情况下验证应用程序行为时。

## 调试和开发

`NoSecurityFiltering` 对以下情况可能有用：

- **诊断兼容性问题**：确定过滤机制是否导致应用程序问题。
- **开发测试**：运行需要不受限制访问的开发工具。
- **旧应用程序支持**：支持在任何过滤下都无法运行的应用程序。

## 相关设置

### 替代的精细控制

与其禁用所有过滤，不如考虑这些单独控制：

- **[禁用文件过滤器](DisableFileFilter.md)**：只禁用文件系统过滤。
- **[禁用键过滤](DisableKeyFilter.md)**：只禁用注册表过滤。
- **[禁用对象过滤器](DisableObjectFilter.md)**：只禁用对象过滤。

[^1]: `OptionsWindow.ui` 中的界面标签：复选框文本"禁用安全过滤（不推荐）"清楚表明安全影响，并阻止随意使用此设置。

[^2]: `OptionsAdvanced.cpp` 中的界面依赖：代码 `ui.chkNoSecurityFiltering->setEnabled(ui.chkNoSecurityIsolation->isChecked());` 确保 NoSecurityFiltering 只能在 NoSecurityIsolation 也激活时启用，强制执行应用程序隔离模式前提。
