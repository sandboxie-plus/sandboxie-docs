# Win32k 钩子

## 概述

Sandboxie 可以挂钩选定的 Win32k 系统调用，以兼容那些需要特定 GUI 或图形驱动调用穿过 Sandboxie 中介的应用程序。该机制有两个配置层级：必须先有全局支持，盒或进程才能使用这些钩子。

这不是通用的 GPU 加速开关，不会挂钩每一个 Win32k 系统调用，也不会切换某项 Windows 安全缓解措施。实验性的 Win32k 过滤表支持是另一套内部机制。

## 全局钩子支持

全局可用性设置是：

```ini
[GlobalSettings]
EnableWin32kHooks=y
```

当前运行时默认启用。驱动只在 Windows 内部版本 14393 或更高、且 `EnableWin32kHooks` 已启用时，才初始化 Win32k 系统调用支持。这使该机制可用；它不会把钩子强行装入每个沙盒进程。

禁用该设置会阻止后续的逐进程 Win32k 钩子路径被安装。当前设置元数据把该全局控件归类为高级且实验性。

SandMan 在 **全局设置 > 高级选项 > Sandboxie 配置** 下以如下标签暴露它：

> Hook selected Win32k system calls to enable GPU acceleration (required for chrome, firefox and more)

该控件在低于 14393 的 Windows 内部版本上不可用。界面标签描述的是兼容性动机，但仅启用全局支持并不会选定每个应用程序，也不保证 GPU 加速。

## 逐进程钩子选择

`UseWin32kHooks` 选择哪些沙盒进程使用可用的钩子路径。它支持带可执行文件限定的配置，例如：

```ini
UseWin32kHooks=program.exe,y
```

该进程设置要求全局 `EnableWin32kHooks=y`。不带可执行文件限定的值可以设置整个盒的行为，而带限定的条目可以针对特定可执行文件。

当没有适用的 `UseWin32kHooks` 值时，当前默认只对 Sandboxie 归类为其 Google Chrome/Chromium 映像类型的进程启用。当前模板与应用程序检测逻辑可以把其他浏览器或 Electron 进程归入该类型。该归类由项目维护，不应视为固定的应用程序清单。

在 SandMan 中，`UseWin32kHooks` 可通过 **沙盒选项 > 高级选项 > 杂项** 下的逐进程高级选项编辑器使用。其说明指出必须先启用全局 Win32k 钩子支持。它不是一个专门的常规复选框。

## GPU 加速兼容性

主要的兼容动机是 Chrome/Chromium GPU 处理所使用的图形驱动交互。Sandboxie 默认的 Win32k 钩子映射包含名称匹配 `GdiDdDDI*` 的选定调用。

这些钩子让选定的调用走 Sandboxie 的 Win32k 中介与令牌处理路径。这并不意味着每个 GPU 调用都被挂钩、每个基于 Chromium 的应用程序都需要手工配置，或者启用钩子就一定能获得硬件加速。

## 平台与进程门限

只有当所有相关条件都满足时，才会为进程安装 Win32k 钩子。在下列情况中（以及其他条件），安装会被跳过：

- Windows 内部版本或驱动支持不可用；
- 进程不具备 Sandboxie 的可挂钩 Win32k 能力；
- 全局 `EnableWin32kHooks` 被禁用；
- 进程运行在应用程序隔离模式下；
- 低层系统调用钩子设施在内部被禁用；
- `UseWin32kHooks` 被禁用，或对该进程未默认启用。

这些检查发生在沙盒进程初始化其钩子路径时。更改设置后请重启受影响的沙盒进程，以确保使用新的选择。

## 高级与实验性控件

> [!WARNING]
> Sandboxie 包含面向专家诊断与开发的低层 Win32k 钩子映射控件。它们可能禁用必需的中介，或强制安装 Sandboxie 出于稳定性考虑而刻意排除的钩子。项目元数据与源码注释警告：强制安装额外钩子可能导致系统不稳定或蓝屏。不建议把这些控件当作常规兼容性设置。

在内部，`EnableWin32Hook` 可以把具名调用加入钩子集合，`DisableWin32Hook` 可以移除调用，`IgnoreWin32HookBlacklist` 可以绕过内置的稳定性黑名单。本页有意不为它们提供配置配方。

实验性的 `UseWin32kFilterTable` 支持在内部同样存在。它不是通用的 Win32k 钩子设置：当前代码在加载 Windows 过滤服务表时、以及对于 Windows 已报告为受 Win32k 过滤的进程时，都会查询它。它本身不会为任意进程启用 Windows Win32k 过滤，此处也不把它作为受支持的兼容性控件来记录。

`AlwaysUseWin32kHooks` 已过时。它在 1.0.11 版中被移除，并由 `UseWin32kHooks` 取代；当前运行时没有读取方。

## 排查指引

- 确认 `EnableWin32kHooks` 未被全局禁用。
- 对于已确认的 Win32k 或 GPU 兼容问题，检查受影响可执行文件的生效 `UseWin32kHooks` 值。
- 优先使用当前模板与 Sandboxie 的映像归类，而不是强制个别 Win32k 钩子名称。
- 排查系统崩溃或回归时，移除自定义的钩子映射试验。
- 不要把绕过 Win32k 钩子黑名单或使用实验性过滤表支持当作常规排查步骤。

禁用 Win32k 钩子不会全局关闭 Sandboxie 的安全机制，启用它们也不应被描述为自动的安全改进。该机制主要解决选定被拦截调用的兼容性。

## 版本历史

| 设置或变更 | 版本 |
| --- | --- |
| `EnableWin32kHooks` 元数据 | AddedVersion 1.0.0 |
| 变更日志中描述的 Win32k 钩子功能 | Sandboxie Plus 1.0.3 / Classic 5.55.3 |
| `AlwaysUseWin32kHooks` | 1.0.3 引入；1.0.11 移除，由 `UseWin32kHooks` 取代 |
| `UseWin32kHooks` 元数据 | AddedVersion 1.0.11 |
| Win32k 钩子曾临时默认应用于所有进程 | Sandboxie Plus 1.16.6 / Classic 5.71.6 |
| 因兼容问题回退该宽泛默认 | Sandboxie Plus 1.16.7 / Classic 5.71.7 |

元数据把 `EnableWin32kHooks` 记为 1.0.0 添加，而 Win32k 钩子功能在 1.0.3 / 5.55.3 的发布说明中出现。该版本差异的原因尚未确定。现行的选择规则由当前的可执行行为决定，而不是历史默认值的描述。

## 相关页面

- [Sandboxie Ini](SandboxieIni.md)
- [特殊映像](SpecialImage.md)
- [令牌与系统调用内部机制](TokenMagic.md)
