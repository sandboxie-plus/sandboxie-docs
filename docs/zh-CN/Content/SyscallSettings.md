# 系统调用设置 {#system-call-settings}

<div id="overview"></div>

## 概述

Sandboxie 会对部分原生系统调用进行中介，作为其隔离与兼容性架构的一部分。这种中介既涉及 Sandboxie 为该调用提供的处理程序，也涉及在处理该调用期间临时选择的安全令牌。这是两个彼此独立的决定。

Sandboxie 并不拦截每一个 Windows 系统调用，系统调用中介也不是它唯一的隔离层。文件与注册表过滤、内核对象过滤、虚拟化、网络策略以及其他控制各自独立运作。关于 Sandboxie 令牌架构的背景知识，参见 [令牌与系统调用内部机制](TokenMagic.md)。

## SysCallLockDown

沙盒级设置是：

```ini
SysCallLockDown=y
```

`SysCallLockDown=y` 会把进程被拦截的系统调用置于锁定模式。`UseSecurityMode=y`（用于启用安全强化模式）也会使进程采用这种锁定行为。

未启用锁定时，Sandboxie 的中介路径在处理被拦截的调用时，可以按需临时使用原始令牌或完整令牌。启用锁定后：

- 已批准的拦截调用可以使用那条原始/完整令牌的执行路径；
- 未批准的拦截调用不会获得该路径，而是继续在受限的沙盒令牌下执行；
- 调用仍可执行，但如果受限令牌缺少所需的权限，它可能失败。

因此，`SysCallLockDown` 并不是一份阻止所有未批准系统调用的简单清单。它控制的是 Sandboxie 所中介的拦截路径内部的令牌选择决定。

安全强化模式以及直接使用 `SysCallLockDown` 都需要有效的 [支持者证书](../PlusContent/supporter-certificate.md)。

<div id="approved-system-calls"></div>

## 已批准的系统调用

批准会把某个被拦截的系统调用条目标记为在锁定生效期间有资格使用原始/完整令牌执行。它不会禁用 Sandboxie 的拦截，不会绕过与之关联的 Sandboxie 处理程序，也不会让该调用在沙盒之外执行。文件、注册表、对象以及其他独立过滤同样保持生效。

`ApproveWinNtSysCall` 与 `ApproveWin32SysCall` 填充的是全局批准映射；Sandboxie 不为单个沙盒维护单独的映射。内置批准来自 `Templates.ini` 中的 `[SysCallPresets]` 节。自定义批准可以直接写入 `[GlobalSettings]`，也可以由通过 `[GlobalSettings]` 启用的自定义模板提供。

构建这些全局映射时，不会参考单个沙盒节中、或仅在某个特定沙盒中启用的模板中的批准条目。因此，系统调用批准不是逐沙盒机制。请把自定义批准保持在最小范围：在锁定状态下，每一个被批准的条目都会为该调用恢复原始/完整令牌路径的资格。内置批准是为受支持的场景维护的，不应整体复制到自定义配置中。

<div id="nt-system-calls"></div>

### NT 系统调用

`ApproveWinNtSysCall` 把名称加入全局 NT 系统调用批准映射。名称使用驱动入口名，不带 `Nt` 或 `Zw` 前缀。直接的自定义批准使用 `[GlobalSettings]`，例如：

```ini
[GlobalSettings]
ApproveWinNtSysCall=OpenFile
ApproveWinNtSysCall=CreateFile
```

这些示例仅演示语法，并不构成一份通用的推荐批准清单。

<div id="win32k-system-calls"></div>

### Win32k 系统调用

`ApproveWin32SysCall` 是面向被拦截的 Win32k 系统调用的对应全局批准机制。直接的自定义批准可以使用匹配模式：

```ini
[GlobalSettings]
ApproveWin32SysCall=GdiDdDDI*
```

只有当 Sandboxie 的 Win32k 系统调用挂钩路径对该进程可用且已安装时，Win32k 批准才会生效。批准仍然控制锁定的令牌决定；它不会绕过为匹配调用安装的任何 Sandboxie 处理程序。

<div id="configuration-reload"></div>

## 配置重新加载

当前版本的 Sandboxie 会在驱动配置被重新配置时重新加载 NT 与 Win32k 批准映射。编辑批准条目后，请使用 **选项 > 重新加载配置文件**，使新的映射生效。通常不必仅为这些批准清单的改动而重启驱动。

这只会更新批准映射。它不会重建已分配给运行中进程的令牌，也不会改变进程启动时安装了哪些系统调用钩子。在测试范围更大的系统调用配置改动时，请重启受影响的沙盒化进程。

## OpenAllSysCalls

沙盒级调试设置是：

```ini
OpenAllSysCalls=y
```

尽管名称如此，`OpenAllSysCalls` 并不是简单地“允许每一个系统调用”，也不会禁用整个沙盒。`OpenAllSysCalls=y` 会使已安装 Sandboxie 第一阶段处理程序的 NT 系统调用条目绕过该处理程序，直接调用底层系统调用路径。Win32k 分派路径中存在同一个内部开关，但当前的 Win32k 表中并未在该路径安装第一阶段处理程序。

锁定的令牌决定是独立的，并且发生在这一处理程序决定之前。因此，`OpenAllSysCalls=y` 不会禁用 `SysCallLockDown`，也不会让每个调用都以原始令牌运行。如果进程处于锁定状态且某个被拦截的调用未获批准，受限令牌行为仍然适用；启用 `OpenAllSysCalls` 不会赋予该调用原始/完整令牌执行权限。

> [!WARNING]
> 本项目明确把 `OpenAllSysCalls` 归类为不安全的调试选项。它绕过为被挂钩条目提供安全、虚拟化、过滤或兼容性行为的已安装 Sandboxie 第一阶段处理程序，从而削弱系统调用层面的中介。它用于调试或非常特定的兼容性排查，而不是常规的沙盒配置。

该设置不会自动禁用无关的层，例如文件与注册表过滤、内核对象回调、网络策略或其他独立的 Sandboxie 控制。

<div id="security-considerations"></div>

## 安全考虑

- 只批准已确认的兼容性问题所必需的那些调用。
- 把内置的 `[SysCallPresets]` 批准视为受维护的实现策略，而不是一份可供复制的通用清单。
- 批准改变的是临时令牌上下文；它不会移除该调用的常规处理程序。
- `OpenAllSysCalls` 移除的中介比一次批准更多，不应把它当作常规的兼容性开关。
- 应用程序能正常工作，并不能证明宽泛的批准或调试绕过仍保留了预期的隔离边界。

<div id="version-history"></div>

## 版本历史

| 设置或变更 | 引入版本 |
| --- | --- |
| 安全强化模式、`SysCallLockDown`、`ApproveWinNtSysCall` 与 `ApproveWin32SysCall` | Sandboxie Plus 1.3.0 / Classic 5.58.0 |
| `OpenAllSysCalls` 不安全调试选项 | Sandboxie Plus 1.15.9 / Classic 5.70.9 |

<div id="related-pages"></div>

## 相关页面

- [安全强化模式](../PlusContent/security-mode.md)
- [令牌与系统调用内部机制](TokenMagic.md)
- [Sandboxie Ini](SandboxieIni.md)
