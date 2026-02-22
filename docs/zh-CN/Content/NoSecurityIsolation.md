# 无安全隔离

_NoSecurityIsolation_ 是自 v1.0.0 / 5.55.0 起提供的一项沙箱设置，将沙盘从安全隔离环境转换为 **应用程序隔离** 模式，优先考虑兼容性而非安全性。

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
- `n`（默认值）保持安全隔离。

## 工作机制

启用后，驱动会设置 `bAppCompartment = TRUE`，从根本上改变沙盘的运行方式，具体表现为：

- **绕过令牌过滤**：主令牌和模拟令牌均保持未修改[^1][^2][^3]
- **不使用作业对象**：进程不受 Windows 作业对象限制[^4]
- **放宽路径控制**：默认的安全路径阻断功能被禁用[^5]

## 功能矩阵

| 功能 | 标准沙箱 | 应用程序隔离 |
|------|----------|--------------|
| **文件系统虚拟化** | ✓ | ✓ |
| **注册表虚拟化** | ✓ | ✓ |
| **对象命名空间隔离** | ✓ | ✓ |
| **进程监控** | ✓ | ✓ |
| **基于令牌的安全** | ✓ | ✗ |
| **权限限制** | ✓ | ✗ |
| **作业对象分配** | ✓ | ✗ |
| **安全路径阻断** | ✓ | ✗ |

## 路径控制变化

在应用程序隔离模式下，三项关键路径行为会自动禁用[^5]：

- **`AlwaysCloseForBoxed`**：沙箱进程可访问通常被阻断的路径[^6]
- **`DontOpenForBoxed`**：打开路径规则对所有进程均等适用[^7]
- **`ProtectHostImages`**：放宽对宿主二进制文件的保护[^8]

## 兼容性与集成

### 自动激活

- **不支持的 Windows 版本**：自动启用并显示警告 MSG_1207[^11]
- **沙盘 Plus 沙箱类型**：在 `应用程序隔离` 和 `应用程序隔离并保护数据` 中预设开启

### 兼容性提升

- 进程可与主机系统自由交互
- 降低与依赖权限的应用程序的冲突
- 更好地支持复杂软件与开发工具

## 安全影响

> [!IMPORTANT]
> 应用程序隔离模式显著降低安全隔离能力：
>
> - 进程以原有的安全上下文和权限运行
> - 无基于令牌的保护或权限降级
> - 沙盘仅提供虚拟化，不提供安全边界

## 相关设置

### 配套项

- **[NoSecurityFiltering](NoSecurityFiltering.md)**：进一步禁用过滤[^9]
- **OriginalToken**：在隔离模式下自动启用
- **模板路径**：应用 `TemplateAppCPaths`[^10]

### 作业对象限制（已禁用）

以下设置因作业对象排除而失效：

- `ProcessNumberLimit`
- `ProcessMemoryLimit`
- `TotalMemoryLimit`

## 使用场景与故障排查

**启用时机：**

- 软件测试和开发环境
- 需要完整系统权限的遗留应用
- 令牌限制兼容性问题
- 仅需虚拟化（文件/注册表隔离）场景

**常见触发因素：**

- 应用因令牌限制无法启动
- 需要管理员权限
- 复杂软件兼容性问题

## 相关

- **沙盘 Plus**：沙箱选项 > 安全选项 > 安全隔离
- [沙箱类型](../PlusContent/box-preset-comparison.md)
- [DropChildProcessToken](DropChildProcessToken.md)

[^1]: **令牌绕过**：`Token_ReplacePrimary` 在 `proc->bAppCompartment` 设置后返回 `TRUE`，从而绕过所有令牌过滤操作

[^2]: **主令牌**：在 `token.c` 中，应用程序隔离模式下保持未修改

[^3]: **模拟令牌**：`Thread_CheckTokenForImpersonation` 在启用 `proc->bAppCompartment` 时返回 `STATUS_SUCCESS`，不做限制

[^4]: **作业对象排除**：`process.c` 中 `new_proc->bAppCompartment` 条件排除进程加入 Windows 作业对象

[^5]: **路径处理**：`process.c` 中禁用三项行为：`always_close_for_boxed`、`dont_open_for_boxed`、`protect_host_images`

[^6]: **AlwaysCloseForBoxed**：`proc->always_close_for_boxed = !proc->bAppCompartment && Conf_Get_Boolean(...)`，确保沙箱进程不会因通常关闭的路径被阻断

[^7]: **DontOpenForBoxed**：`proc->dont_open_for_boxed = !proc->bAppCompartment && Conf_Get_Boolean(...)`，允许所有进程均等应用路径规则

[^8]: **ProtectHostImages**：`proc->protect_host_images = !proc->bAppCompartment && Conf_Get_Boolean(...)`，禁用宿主二进制文件保护

[^9]: **安全过滤**：`no_filtering = proc->bAppCompartment && Conf_Get_Boolean(..., L"NoSecurityFiltering", ...)`，即可完全绕过过滤

[^10]: **模板路径**：`Process_GetPaths(proc, list, L"TemplateAppCPaths", setting_name, FALSE)` 应用隔离模式专用模板路径

[^11]: **自动回退**：`!Dyndata_Active && !proc->bAppCompartment` 触发自动隔离模式，并记录 `Log_Msg1(MSG_1207, info)`