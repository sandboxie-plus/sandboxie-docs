# 禁用对象过滤器

_DisableObjectFilter_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.0.0 / 5.55.0 起可用。此设置禁用对象过滤机制，允许沙盒化进程绕过对象访问限制，直接与沙盒外的进程、线程和其他系统对象交互。

## 前提条件

> [!NOTE]
> 对象过滤需要通过 [GlobalSettings] 节中的 `EnableObjectFiltering=y` 进行全局激活。全局启用后，单个沙盒可以用 `DisableObjectFilter=y` 禁用它。

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

- `y` 为此沙盒禁用对象过滤
- `n`（默认）在全局启用时保持对象过滤

## 安全影响

> [!WARNING]
> 此设置禁用驱动层面对对象访问限制的强制。恶意软件可能通过代码注入、API 钩子或直接系统调用等各种技术绕过这些保护，使此设置不适合不受信任的应用程序。

## 相关设置

### 主覆盖

`DisableObjectFilter` 在以下情况自动启用：

- 在应用程序隔离模式中设置 **[无安全过滤](NoSecurityFiltering.md)** 时[^1]。

### 替代的精细控制

- **[禁用文件过滤器](DisableFileFilter.md)**：只禁用文件系统过滤。
- **[禁用键过滤](DisableKeyFilter.md)**：只禁用注册表过滤。
- **[无安全过滤](NoSecurityFiltering.md)**：在应用程序隔离模式中禁用所有过滤。

[^1]: `process.c` 中的对象过滤控制：设置 `proc->disable_object_flt = no_filtering || Conf_Get_Boolean(proc->box->name, L"DisableObjectFilter", 0, FALSE)` 允许 DisableObjectFilter 独立地或作为应用程序隔离模式中 NoSecurityFiltering 的一部分完全绕过对象过滤。
