# Hook 跟踪

_HookTrace_ 是自 v1.15.5 / 5.70.5 版本起在 [Sandboxie Ini](SandboxieIni.md) 中提供的一项沙盒设置。启用后，将对 [SbieDll](SBIEDLLAPI.md) 组件执行的所有函数挂钩活动进行详细日志记录。

## 用法

```
[DefaultBox]

HookTrace=y
```

## 概述

函数挂钩是 Sandboxie 用于拦截并重定向来自沙盒内进程系统调用的核心机制。`HookTrace` 设置为此过程提供了详尽的可见性，记录每一次挂钩尝试、成功、失败及相关元数据。该功能主要用于排查沙盒相关问题，以及理解 Sandboxie 如何对应用程序进行插桩。

## 工作原理

当启用 `HookTrace` 时：

1. **挂钩检测**：SbieDll 记录对已加载模块中函数的所有挂钩尝试[^1]
2. **状态跟踪**：每一个挂钩操作都带有状态标识，指示其成功、失败原因或特殊情况[^2]
3. **模块解析**：系统将利用地址查找确定每个被挂钩函数的来源模块[^3]
4. **监控输出**：挂钩信息通过 MONITOR_HOOK 标识发送到监控系统[^4]

## 输出格式

挂钩日志条目格式如下：

```
Hooking: module!function
FAILED Hooking: module!function
Skipped Hooking: module!function  
Hooking (trace): module!function
```

可能还会附加其他状态信息：

- `(Chrome Hook Hooked)` —— 成功应用 Chrome 专用挂钩[^5]
- `(Chrome Hook Unresolved)` —— Chrome 专用挂钩解析失败[^6]
- `FFS Target not found, hooked x86 code instead` —— 使用 ARM64 回退方案[^7]

## 挂钩状态类型

挂钩跟踪系统通过多种状态标识对挂钩操作进行分类：

- **HOOK_STAT_CHROME**：处理 Chrome 浏览器专用挂钩[^8]
- **HOOK_STAT_CHROME_FAIL**：Chrome 挂钩解析失败[^9]
- **HOOK_STAT_NO_FFS**：未找到 ARM64 架构特定的 Fast Forward Sequence[^10]
- **HOOK_STAT_SKIPPED**：根据配置有意跳过挂钩[^11]
- **HOOK_STAT_TRACE**：用于 API 跟踪的挂钩[^12]
- **HOOK_STAT_SYSCALL**：ARM64 架构系统调用挂钩（仅限 ARM64 EC）[^13]

## 应用程序挂钩检测

启用 `HookTrace` 后，系统还会监控尝试修改其他进程内存的应用程序行为，这通常表明存在应用级挂钩尝试。此项特性有助于识别与 Sandboxie 自身挂钩机制可能存在的冲突[^14]

## 性能注意事项

- **日志量增加**：启用 Hook 跟踪后，尤其在进程启动期间（加载并挂钩大量模块），将产生大量日志输出
- **仅用于调试**：此设置仅推荐用于调试和排查，不适合生产环境
- **存储影响**：大量详细日志输出会快速占用日志存储空间

## 相关设置

- [ApiTrace](SandboxieTrace.md) —— 在挂钩建立后跟踪实际 API 调用
- [DebugTrace](SandboxieTrace.md) —— Sandboxie 组件的通用调试输出
- [跳过函数钩子](SandboxieTrace.md) —— 控制不应被挂钩的函数
- [跳过钩子](SandboxieTrace.md) —— 按模块粒度配置跳过挂钩

[^1]: 挂钩初始化发生在 `SbieDll_HookInit()`，此处 `Dll_HookTrace = SbieApi_QueryConfBool(NULL, L"HookTrace", FALSE)`
[^2]: 挂钩状态跟踪由一系列 `HOOK_STAT_*` 常量标识，包括 `HOOK_STAT_CHROME`、`HOOK_STAT_CHROME_FAIL`、`HOOK_STAT_NO_FFS`、`HOOK_STAT_SKIPPED`、`HOOK_STAT_TRACE` 和 `HOOK_STAT_SYSCALL`
[^3]: 通过 `Trace_FindModuleByAddress((void*)module)` 查找每个被挂钩函数的来源模块
[^4]: 挂钩日志通过 `SbieApi_MonitorPutMsg(MONITOR_HOOK | MONITOR_TRACE | ((HookStats & HOOK_STAT_SKIPPED) ? MONITOR_OPEN : 0), dbg)` 发送到监控系统
[^5]: Chrome 挂钩成功由 `HookStats & HOOK_STAT_CHROME` 标识，以 "Chrome Hook Hooked" 记录
[^6]: Chrome 挂钩失败由 `HookStats & HOOK_STAT_CHROME_FAIL` 标识，以 "Chrome Hook Unresolved" 记录
[^7]: ARM64 回退方案由 `HookStats & HOOK_STAT_NO_FFS` 标识，以 "FFS Target not found, hooked x86 code instead" 记录
[^8]: `HOOK_STAT_CHROME` 标识值 `0x00000001`，表示成功处理 Chrome 专用挂钩
[^9]: `HOOK_STAT_CHROME_FAIL` 标识值 `0x00000002`，表示 Chrome 挂钩解析失败
[^10]: `HOOK_STAT_NO_FFS` 标识值 `0x00000004`，表示未找到 ARM64 Fast Forward Sequence 目标
[^11]: `HOOK_STAT_SKIPPED` 标识值 `0x00000008`，表示有意跳过挂钩
[^12]: `HOOK_STAT_TRACE` 标识值 `0x00000100`，表示用于 API 跟踪
[^13]: `HOOK_STAT_SYSCALL` 标识值 `0x00000200`，仅 ARM64 EC 模式用于 ARM64 系统调用挂钩
[^14]: 应用程序挂钩检测实现于 `file_misc.c`，当 `Dll_HookTrace` 启用时，会监控可能标志应用级挂钩尝试的 `WriteProcessMemory` 调用