# 禁用对象过滤器

_DisableObjectFilter_ 是自 v1.0.0 / 5.55.0 版本起，在 [沙盘配置](SandboxieIni.md) 文件中可用的一个沙箱设置。启用此设置后，将关闭对象过滤机制，允许受沙箱保护的进程绕过对象访问限制，并直接与沙箱外的进程、线程及其它系统对象进行交互

## 前提条件

> [!NOTE]
> 对象过滤功能需要通过 [GlobalSettings] 部分的 `EnableObjectFiltering=y` 全局激活。在全局启用的情况下，单独的沙箱可通过 `DisableObjectFilter=y` 关闭此功能

## 用法

```ini
[DefaultBox]

DisableObjectFilter=y
```

## 语法

```ini
DisableObjectFilter=<y/n>
```

其中：

- `y` 表示为该沙箱禁用对象过滤
- `n`（默认值）在全局启用时保持对象过滤

## 安全影响

> [!WARNING]
> 此设置将禁用驱动级别的对象访问限制强制措施。恶意软件可能通过代码注入、API 挂钩或直接系统调用等多种技术手段绕过这些保护，因此该设置不适合用于不可信的应用程序

## 相关设置

### 主开关

当以下条件满足时，`DisableObjectFilter` 会自动启用：

- 在应用程序隔离模式下设置了 **[NoSecurityFiltering](NoSecurityFiltering.md)**

### 其他细粒度控制

- **[DisableFileFilter](DisableFileFilter.md)**：仅禁用文件系统过滤
- **[DisableKeyFilter](DisableKeyFilter.md)**：仅禁用注册表过滤
- **[NoSecurityFiltering](NoSecurityFiltering.md)**：在应用程序隔离模式下禁用所有过滤

[^1]: `process.c` 中的对象过滤控制：设置 `proc->disable_object_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableObjectFilter", 0, FALSE)`，允许 DisableObjectFilter 独立地或作为应用程序隔离模式下 NoSecurityFiltering 的一部分，完全绕过对象过滤