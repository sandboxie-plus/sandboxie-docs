# 禁用文件过滤器

_DisableFileFilter_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.9.0 / 5.51.0 起可用。此设置禁用文件系统过滤机制，允许沙盒化进程绕过文件访问限制，直接与宿主文件系统交互。

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

- `y` 完全禁用文件系统过滤
- `n`（默认）保持正常文件过滤行为

## 安全影响

> [!WARNING]
> 此设置禁用驱动层面对文件系统访问限制的强制。恶意软件可能通过代码注入、API 钩子或直接系统调用等各种技术绕过这些保护，使此设置不适合不受信任的应用程序。

## 相关设置

### 主覆盖

`DisableFileFilter` 在以下情况自动启用：
- 在应用程序隔离模式中设置 **[无安全过滤](NoSecurityFiltering.md)** 时[^1]。

### 替代的精细控制

- **[禁用键过滤](DisableKeyFilter.md)**：只禁用注册表过滤。
- **[禁用对象过滤器](DisableObjectFilter.md)**：只禁用对象过滤。
- **[无安全过滤](NoSecurityFiltering.md)**：在应用程序隔离模式中禁用所有过滤。

[^1]: `process.c` 中的文件过滤控制：设置 `proc->disable_file_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableFileFilter", 0, FALSE)` 允许 DisableFileFilter 独立地或作为应用程序隔离模式中 NoSecurityFiltering 的一部分完全绕过文件系统过滤。
