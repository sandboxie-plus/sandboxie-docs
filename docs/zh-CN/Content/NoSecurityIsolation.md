# 无安全隔离

_NoSecurityIsolation_ 是自 v1.0.0 / 5.55.0 起可用的一项沙盒设置，它把 Sandboxie 从安全隔离环境转变为**应用程序隔离**模式，把兼容性置于安全性之上。

## 用法

```ini
[DefaultBox]

NoSecurityIsolation=y
```

## 语法

```ini
NoSecurityIsolation=<y/n>
```

其中：

- `y` 启用隔离模式，
- `n`（默认）保持安全隔离。

## 工作原理

启用时，驱动程序设置 `bAppCompartment = TRUE`，通过以下方式从根本上改变 Sandboxie 的运行：

- **绕过令牌过滤**：主令牌和模拟令牌都保持不变[^1][^2][^3]
- **排除作业对象**：进程避免 Windows 作业对象限制[^4]
- **放宽路径控制**：默认的面向安全的路径阻止被禁用[^5]

## 功能对照表

| 功能 | 标准沙盒 | 应用程序隔离 |
|---------|-----------------|-------------------------|
| **文件系统虚拟化** | ✓ | ✓ |
| **注册表虚拟化** | ✓ | ✓ |
| **对象命名空间隔离** | ✓ | ✓ |
| **进程监视** | ✓ | ✓ |
| **基于令牌的安全** | ✓ | ✗ |
| **权限限制** | ✓ | ✗ |
| **作业对象分配** | ✓ | ✗ |
| **安全路径阻止** | ✓ | ✗ |

## 路径控制变化

在应用程序隔离模式中，三个关键的路径行为会被自动禁用[^5]：

- **`AlwaysCloseForBoxed`**：沙盒化进程可以访问通常被阻止的路径[^6]。
- **`DontOpenForBoxed`**：开放路径规则同等地适用于所有进程[^7]。
- **`ProtectHostImages`**：宿主二进制保护被放宽[^8]。

## 兼容性与集成

### 自动激活

- **不支持的 Windows 版本**：自动启用并伴随警告 MSG_1207[^11]。
- **Sandboxie Plus 沙盒类型**：在"应用程序隔离"和"带数据保护的应用程序隔离"中预配置。

### 增强兼容性

- 进程与宿主系统自由交互。
- 减少与依赖权限的应用程序的冲突。
- 更好地支持复杂软件和开发工具。

## 安全影响

> [!IMPORTANT]
> 应用程序隔离模式会显著降低安全隔离：
>
> - 进程以原始安全上下文和权限运行。
> - 没有基于令牌的保护或权限丢弃。
> - 沙盒提供虚拟化，但不提供安全边界。

## 相关设置

### 互补设置

- **[无安全过滤](NoSecurityFiltering.md)**：进一步禁用过滤[^9]。
- **OriginalToken**：在隔离模式下自动启用。
- **模板路径**：应用 `TemplateAppCPaths`[^10]。

### 作业对象限制（已禁用）

由于作业对象被排除，这些设置将失效：

- `ProcessNumberLimit`
- `ProcessMemoryLimit`
- `TotalMemoryLimit`

## 使用场景与故障排除

**何时启用：**

- 软件测试和开发环境。
- 需要完全系统权限的旧应用程序。
- 令牌限制兼容性问题。
- 仅虚拟化场景（文件/注册表分离）。

**常见触发因素：**

- 因令牌限制而无法启动的应用程序。
- 管理员权限要求。
- 复杂软件兼容性问题。

## 相关

- **Sandboxie Plus**：沙盒选项 > 安全选项 > 安全隔离
- [沙盒类型](../PlusContent/box-preset-comparison.md)
- [丢弃子进程令牌](DropChildProcessToken.md)

[^1]: **令牌绕过**：当设置了 `proc->bAppCompartment` 时，`Token_ReplacePrimary` 返回 `TRUE`，绕过所有令牌过滤操作。

[^2]: **主令牌**：应用程序隔离模式激活时，在 `token.c` 中保持未修改。

[^3]: **模拟令牌**：启用 `proc->bAppCompartment` 时，`Thread_CheckTokenForImpersonation` 无限制地返回 `STATUS_SUCCESS`。

[^4]: **作业对象排除**：`process.c` 中的条件 `new_proc->bAppCompartment` 把进程从 Windows 作业对象中排除。

[^5]: **路径处理**：`process.c` 中禁用三种行为：`always_close_for_boxed`、`dont_open_for_boxed` 和 `protect_host_images`。

[^6]: **AlwaysCloseForBoxed**：`proc->always_close_for_boxed = !proc->bAppCompartment && Conf_Get_Boolean(...)` 确保沙盒化进程不会被阻止访问通常封闭的路径。

[^7]: **DontOpenForBoxed**：`proc->dont_open_for_boxed = !proc->bAppCompartment && Conf_Get_Boolean(...)` 允许路径规则同等应用。

[^8]: **ProtectHostImages**：`proc->protect_host_images = !proc->bAppCompartment && Conf_Get_Boolean(...)` 禁用宿主二进制保护。

[^9]: **安全过滤**：`no_filtering = proc->bAppCompartment && Conf_Get_Boolean(..., L"NoSecurityFiltering", ...)` 启用完全过滤绕过。

[^10]: **模板路径**：`Process_GetPaths(proc, list, L"TemplateAppCPaths", setting_name, FALSE)` 应用隔离模式特定的模板路径。

[^11]: **自动回退**：`!Dyndata_Active && !proc->bAppCompartment` 通过 `Log_Msg1(MSG_1207, info)` 触发自动隔离模式。
