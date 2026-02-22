# 禁用键过滤

_DisableKeyFilter_ 是 [沙盘配置](SandboxieIni.md) 文件中的一种沙箱设置，自 v0.9.0 / 5.51.0 起可用。此设置可禁用注册表过滤机制，使沙箱内的进程能够绕过注册表访问限制，直接修改主机系统注册表

## 使用方法

```ini
[DefaultBox]

DisableKeyFilter=y
```

## 语法

```ini
DisableKeyFilter=<y/n>
```

其中：

- `y` 表示完全禁用注册表过滤
- `n`（默认值）表示保持正常的注册表过滤行为

## 安全影响

> [!WARNING]
> 此设置会禁用驱动层对注册表访问限制的强制执行。恶意软件有可能通过代码注入、API 钩子或直接系统调用等多种方式绕过此类保护，因此该设置不适用于不可信应用程序

## 相关设置

### 主控覆盖

当以下情况成立时，`DisableKeyFilter` 会自动启用：
- **[NoSecurityFiltering](NoSecurityFiltering.md)** 在应用程序隔离模式下启用

### 其他细粒度控制选项

- **[DisableFileFilter](DisableFileFilter.md)**：仅禁用文件系统过滤
- **[DisableObjectFilter](DisableObjectFilter.md)**：仅禁用对象过滤
- **[NoSecurityFiltering](NoSecurityFiltering.md)**：在应用程序隔离模式下禁用所有过滤

[^1]: 注册表过滤控制在 `process.c` 中：`proc->disable_key_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableKeyFilter", 0, FALSE)` 设置允许 DisableKeyFilter 独立或作为应用程序隔离模式下 NoSecurityFiltering 的一部分，完全绕过注册表过滤