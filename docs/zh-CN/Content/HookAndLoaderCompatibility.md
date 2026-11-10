# 钩子与加载器兼容性

这些高级设置会改变 Sandboxie 选定的钩子或 Windows 加载器初始化路径。它们面向有针对性的兼容性排查，不是用来关闭沙盒的通用开关。跳过某条拦截路径，同样会改变依赖该路径的中介或兼容行为。

## 钩子层次

Sandboxie 并不使用统一的单一钩子。驱动维护关于选定原生系统调用的信息；一条注入的低层路径可以在新启动的进程中准备系统调用桩。SbieDll 另外安装 Nt 与 Win32 API 钩子，其加载器回调为特定已加载模块初始化钩子与变通方案。跳过其中某一条路径的设置，不一定跳过其他路径。

## NoSysCallHooks

```ini
[DefaultBox]
NoSysCallHooks=y
```

`NoSysCallHooks` 是盒级布尔选项，默认禁用。启用后，Sandboxie 会跳过该盒中新启动进程的低层系统调用桩初始化。它还会跳过 `NtOpenProcess`、`NtOpenThread` 与 `NtDuplicateObject` 上选定的 SbieDll 安全钩子，以及相关的 WoW64 系统调用修补。应用程序隔离模式会独立地跳过低层路径和这些选定的安全钩子。

这**不会**禁用 Sandboxie 的所有钩子，也不会禁用进程注入的其余部分。其他 SbieDll 钩子与独立的驱动控件仍各有自己的初始化路径。仅对已诊断出的兼容问题使用该选项；它不是“关掉所有 API 拦截、其余沙盒行为保持不变”的手段。

## DisableWinNtHook

`DisableWinNtHook` 是驱动 NT 系统调用映射的可重复模式设置。映射加载器从 `[SysCallPresets]` 读取条目，因此该设置是全局的，而不是按盒或按可执行文件分别选择。底层配置查找对 `[GlobalSettings]` 有回退行为，但不应把这两个来源描述为可自由合并的两个列表。随附的预设已经提供了条目。写入系统调用条目名时不要带 `Nt` 或 `Zw` 前缀。当前某个预设示范了该语法：

```ini
[SysCallPresets]
DisableWinNtHook=MapViewOfSection
```

驱动扫描 `Zw` 导出，去掉 `Zw` 前缀，并把匹配的映射条目标记为禁用。被如此标记的条目，在 Sandboxie 为其低层钩子路径复制系统调用信息时会被略过。解析器接受多个条目，其模式匹配支持 `*` 与 `?`；匹配使用导出名的拼写，区分大小写。不匹配任何已知条目的名称或模式不产生效果。这不是映像感知规则：此处不解析程序选择器、进程组与取反选择器。

该设置不会普遍禁用 Win32 API 钩子，也不保证使用某个具名系统调用的每个更高层 API 都会变为未被挂钩。`DisableWin32Hook` 是另一项 Win32k 映射控制，见 [Win32k 钩子](Win32kHooks.md)。

### 两个系统调用设置的区别

`NoSysCallHooks=y` 为盒中的进程跳过一条更宽泛的低层系统调用桩初始化路径。`DisableWinNtHook` 则在该路径所用的、驱动范围的 NT 系统调用映射中选定具名条目。前者是盒级布尔值；后者是可重复的映射模式。两者都不会禁用 Sandboxie 的全部钩子。

## NoParallelLoading

```ini
[DefaultBox]
NoParallelLoading=y
```

`NoParallelLoading` 是盒级布尔选项，默认禁用。在新启动的沙盒进程中，SbieDll 加载器初始化期间会把该进程的 `LoaderThreads` 参数设为 `0`。这针对的是 Windows 加载器的并行加载行为，用于排查加载器兼容问题。它不会禁用应用程序的多线程，也不会把所有进程活动串行化。

## DllSkipHook

`DllSkipHook` 是生效盒配置中的可重复 DLL 名称设置。例如，当前的 Proxifier 兼容模板包含：

```ini
DllSkipHook=ws2_32.dll
```

在 SbieDll 加载器初始化时，每个值都会与 Sandboxie 已知模块初始化表中的确切 DLL 基名做不区分大小写的比较。匹配时，该 DLL 加载时会跳过其模块的 Sandboxie 专用初始化回调。它**不会**阻止 Windows 加载该 DLL。其他独立的跟踪或钩子路径不会被该设置普遍禁用。

未知名称、完整路径或通配符模式都不会匹配该表，因而没有效果。这些值没有可执行文件选择器、进程组或取反解析器。与 [跳过钩子](SkipHook.md) 和 [跳过函数钩子](FuncSkipHook.md) 不同，该选项选择的是已知模块回调，而不是单个钩子标识或导出函数。

`NoParallelLoading` 与 `DllSkipHook` 解决的是不同问题：前者改变某个进程的加载器并发行为，后者为已知模块跳过选定的 Sandboxie 回调。两者都不是通用的 DLL 阻止机制或关闭沙盒的机制。

## 模板与预设

Sandboxie 当前的 `[SysCallPresets]` 包含若干为其系统调用映射维护的 `DisableWinNtHook` 条目。Proxifier 模板提供了上面那个 `DllSkipHook=ws2_32.dll` 兼容示例。这些是当前维护的预设，不是“照抄每个条目”的建议，也不承诺模板内容保持不变。`DllSkipHook` 也可以来自生效沙盒配置中适用的已启用模板。

## 应用更改

`NoSysCallHooks`、`NoParallelLoading` 与 `DllSkipHook` 在进程或 SbieDll 初始化期间读取。更改后请启动新的沙盒进程；既有进程不会重建已安装的钩子或加载器状态。驱动在其配置重载时可以刷新 `DisableWinNtHook` 的映射标志，但已初始化的进程桩不会被追溯重建。测试映射更改时，请重载配置并重启受影响的沙盒进程。该更新通常不需要重启驱动或重启 Windows。

当前 SandMan 的选项来源没有针对这四个设置的专门控件。请在 [Sandboxie Ini](SandboxieIni.md) 中或通过适用的预设或模板配置它们。

## 版本历史

变更日志记录了 `NoSysCallHooks` 于 Sandboxie Plus 0.4.5 / Classic 5.44.1 引入，`DllSkipHook` 于 Plus 0.9.1 / Classic 5.51.1，`DisableWinNtHook` 于 Plus 1.3.0 / Classic 5.58.0，`NoParallelLoading` 于 Plus 1.7.0 / Classic 5.62.0。它还记录了 Plus 1.15.9 / Classic 5.70.9 起支持无需重载驱动即可更改 `DisableWinNtHook`。

## 相关设置

- [系统调用设置](SyscallSettings.md) 单独说明系统调用中介、批准与锁定，区别于钩子映射排除。
- [Win32k 钩子](Win32kHooks.md) 涵盖另一条独立的 Win32k 钩子路径。
- [高级加载器与 SxS 兼容性](AdvancedLoaderCompatibility.md) 涵盖其他加载器与进程启动变通方案。
