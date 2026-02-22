# 禁用文件过滤

_DisableFileFilter_ 是一个自 v0.9.0 / 5.51.0 版本起在 [沙盘配置](SandboxieIni.md) 中引入的沙箱设置。该设置用于禁用文件系统过滤机制，使得被沙箱保护的进程可以绕过文件访问限制，直接与宿主文件系统进行交互

## 用法

```ini
[DefaultBox]

DisableFileFilter=y
```

## 语法

```ini
DisableFileFilter=<y/n>
```

其中：

- `y`：完全禁用文件系统过滤
- `n`（默认）：保持正常的文件过滤行为

## 安全影响

> [!WARNING]
> 此设置会禁用驱动级别的文件系统访问限制。恶意软件可能利用代码注入、API 挂钩或直接系统调用等多种技术绕过这些防护，因此该设置不适用于不受信任的应用程序

## 相关设置

### 主控开关

当以下条件满足时，`DisableFileFilter` 会被自动启用：
- 在应用程序隔离模式下设置了 **[NoSecurityFiltering](NoSecurityFiltering.md)**

### 其他细粒度的控制

- **[DisableKeyFilter](DisableKeyFilter.md)**：仅禁用注册表过滤
- **[DisableObjectFilter](DisableObjectFilter.md)**：仅禁用对象过滤
- **[NoSecurityFiltering](NoSecurityFiltering.md)**：在应用程序隔离模式下禁用所有过滤

[^1]: process.c 文件中的文件过滤控制：设置 `proc->disable_file_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableFileFilter", 0, FALSE)`，允许 DisableFileFilter 独立或作为 NoSecurityFiltering 的一部分，在应用程序隔离模式下完全绕过文件系统过滤