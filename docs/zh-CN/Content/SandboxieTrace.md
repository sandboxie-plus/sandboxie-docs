# Sandboxie 跟踪

Sandboxie 提供了若干相互独立的追踪机制，用于排查兼容性和隔离规则问题。它们的输出会被收集到一个按会话共享的监控缓冲区中，可通过以下界面查看：

* Sandboxie Plus 中的[跟踪日志](../PlusContent/TraceLog.md)；
* Sandboxie Control 经典版中的[资源访问监视器](ResourceAccessMonitor.md)。

打开任一查看器都会激活监控使用者。它**不会自动启用**下文描述的每个详细追踪选项。不做任何额外设置时可以获得一些基线资源活动；而 `ApiTrace`、`HookTrace`、`DebugTrace`、`ErrorTrace` 等选项会添加专用或更高数据量的诊断。

没有监控使用者处于活动状态时，共享监控缓冲区不会被维护，其消息也不会保留供以后显示。显式启用的追踪选项即使在查看器关闭时，仍可能安装钩子或在进程侧执行诊断工作。

监控与[日志消息事件](LogMessageEvents.md)相互独立，后者会把选定的 Sandboxie 消息发送到 Windows 事件日志。崩溃转储和进程启动暂停属于[崩溃与调试器诊断](CrashAndDebuggerDiagnostics.md)的范畴。

## 资源访问追踪

资源追踪设置有助于识别可能解释沙盒应用失败的文件、注册表、IPC 及相关操作。在具体设置支持的情况下，驱动资源过滤器使用以下实用取值：

| 取值 | 含义 |
| ----- | ------- |
| `A` | 成功或被允许的操作 |
| `D` | 失败或被拒绝的操作 |
| `I` | 被忽略设备的操作（在支持的情况下） |
| `*` | 广泛追踪 |

支持 `AD` 之类的组合；使用该过滤器的设置也接受 `ad` 之类的小写组合。这些字母并非由每个追踪选项统一实现。

### FileTrace

在资源模式下，`FileTrace` 记录文件、目录、卷和设备活动：

```ini
FileTrace=A
FileTrace=D
FileTrace=AD
FileTrace=I
FileTrace=*
```

`A` 选择成功或被允许的活动，`D` 选择失败或被拒绝的活动，`I` 选择被忽略的设备类。`*` 请求广泛的文件资源追踪。

同一个遗留设置名还有一项独立的 SbieDll 文件 API 追踪用途：

```ini
FileTrace=y
FileTrace=program.exe,y
```

这种形式会添加详细的文件 API 调用记录，并可限定到某个可执行文件。请把资源过滤器形式和映像限定的布尔形式视为同一遗留名的两种不同诊断用途，而非一种组合语法。

### KeyTrace、PipeTrace 与 IpcTrace

这些设置支持“允许/成功”和“拒绝/失败”资源过滤器：

```ini
KeyTrace=AD
PipeTrace=AD
IpcTrace=AD
```

* `KeyTrace` 记录注册表键操作。
* `PipeTrace` 记录命名管道和邮件槽操作。
* `IpcTrace` 记录对其他 IPC 对象和进程间操作的访问。

`I` 对这些设置目前没有实际作用。

### GuiTrace

`GuiTrace` 是一个遗留设置。它直接的 GUI 追踪实现属于旧版 Windows XP 时代的 Win32k 钩子路径；现代受支持的 Windows 版本不通过此选项提供等效实现。GUI 和窗口类相关事件仍可能通过其他监控机制出现，但在 Windows 10 或 Windows 11 上启用 `GuiTrace` 不应指望重现历史上的 GUI 追踪。

### ClsidTrace

`ClsidTrace` 添加详细的 COM 操作记录。当前运行时将显式的非空遗留值视为启用，而不是把 `A`、`D`、`I` 解释为资源过滤器。请使用 SandMan 中的复选框（如果有），或移除显式条目以手动关闭手工配置的追踪。

### NetFwTrace

`NetFwTrace` 在当前设置元数据中被标记为已禁用。仅存留有限的用户态网络诊断残余，旧的 WFP/防火墙日志路径并不是一个可用的、完整的防火墙追踪器。SandMan 中**可能仍可见“网络防火墙”追踪复选框**，但不应把它当作通用的 WFP 数据包或防火墙决策记录器。请移除显式条目，而不要依赖 `NetFwTrace=n` 作为手动禁用形式。

## 排查被拒资源

**被拒绝的追踪记录本身并不意味应该放行。** 许多被拒操作是预期之内且无害的。只有当事件与应用失败存在合理关联时才测试配置变更，并优先使用最窄的资源专用规则。开放主机资源会降低沙盒隔离强度。

用资源类型确定相关的配置族：

| 追踪资源 | 相关访问设置 |
| -------------- | ----------------------- |
| 文件、目录、卷和设备 | [打开文件路径](OpenFilePath.md)、[封闭文件路径](ClosedFilePath.md)、[只读文件路径](ReadFilePath.md) |
| 注册表键 | [打开键路径](OpenKeyPath.md)、[封闭键路径](ClosedKeyPath.md)、[只读键路径](ReadKeyPath.md) |
| 命名管道和邮件槽 | [打开管道路径](OpenPipePath.md) |
| IPC 和进程间对象 | [打开 IPC 路径](OpenIpcPath.md)、[封闭 IPC 路径](ClosedIpcPath.md) |
| GUI 和窗口类访问 | [打开窗口类](OpenWinClass.md) |
| COM 类 | [打开 Clsid](OpenClsid.md)、[封闭 Clsid 路径](ClosedClsidPath.md) |

例如，如果在可复现的失败时刻反复出现针对 `\BaseNamedObjects\Xyzzy` 的 IPC 拒绝事件，且有明确理由测试对该对象的访问：

```ini
[DefaultBox]
OpenIpcPath=\BaseNamedObjects\Xyzzy
```

一个实用的测试流程是：

1. 在跟踪日志处于活动状态时复现问题。
2. 在失败附近定位一个拒绝事件并确定其资源类型。
3. 判断该事件是否合理地解释了失败。
4. 如果是，临时添加最窄的相应规则。
5. 按需重新加载或应用配置，重启受影响的应用程序，并复现测试。
6. 对比行为；如果没有解决问题则移除该规则。

不要把宽泛的 `Open*` 通配符当作通用排查手段。某个追踪类别并不能机械地决定就需要某一条特定的访问规则。

## API 调用追踪

### ApiTrace

`ApiTrace` 记录经过 Sandboxie 通用 SbieDll 钩子机制的调用：

```ini
ApiTrace=y
ApiTrace=program.exe,y
```

它能感知映像名，但不会追踪应用使用的每个 Windows API。输出在监控中表现为 API 调用记录。由于此选项数据量大且侵入性强，请仅在排查期间启用，并在更改后重启受影响的进程。

### ApiTraceDll

`ApiTraceDll` 扩展 `ApiTrace`，为选定模块中的命名导出添加仅追踪用的钩子。支持多个条目：

```ini
ApiTraceDll=kernel32.dll
ApiTraceDll=user32.dll
```

请使用模块基名而非完整路径。模块匹配不区分大小写。并非每个导出都保证可追踪。

### ApiSkipTrace

`ApiSkipTrace` 排除匹配的函数名前缀，主要针对通过 `ApiTraceDll` 申请的额外导出覆盖：

```ini
ApiSkipTrace=Nt
```

支持多个条目。前缀匹配区分大小写。它不是 Sandboxie 常规钩子的通用抑制规则。

安装诊断（而非调用记录）请参阅[钩子追踪](HookTrace.md)。

## 系统调用与内部追踪

### CallTrace

`CallTrace` 是驱动系统调用追踪，而非通用的 Windows API 追踪：

```ini
CallTrace=A
CallTrace=D
CallTrace=AD
CallTrace=*
```

`A` 广泛记录到达追踪路径的被拦截调用，`D` 额外记录返回非成功 NTSTATUS 的调用。这些字母不应被解释为通用的“允许/拒绝”分类。SandMan 的**「系统调用追踪」**复选框会写入 `CallTrace=*`。

### CallTraceEx

`CallTraceEx` 请求一种独立的、基于 Windows 进程插桩回调的高级系统调用追踪机制。当前任何配置的非空值都会请求它。它面向现代 Windows，在所有架构和配置上并非都受支持，也没有专用的 SandMan 复选框。

### SbieTrace

`SbieTrace` 为 SbieDll 与其他 Sandboxie 核心组件之间的交互启用选定诊断。其输出表现为 Debug 类记录。它不是完整的内部执行追踪。

### DebugTrace

`DebugTrace` 将应用的 `OutputDebugString` 输出捕获进监控，同时保留应用正常的调试输出调用。不应把它当作对任意长字符串的无损捕获。

### ErrorTrace

`ErrorTrace` 记录通过当前钩子路径观察到的非零 Win32 last-error 赋值。它可能非常嘈杂，且不覆盖每个 Windows 错误或每个 NTSTATUS。

## DNS 追踪

`DnsTrace` 记录 Sandboxie DNS 兼容与过滤层所拦截的 Winsock 服务查找路径。它能显示请求名称、IPv4 和 IPv6 结果、查找错误或完成情况，以及在配置了 `NetworkDnsFilter` 时受其影响的响应。

它不追踪每个 DNS API、不捕获 DNS 数据包，也不覆盖使用自有直接解析器的应用。被查询的主机名和返回的地址可能出现在跟踪日志中——分享追踪输出前请先审阅。`DnsTrace` 不会启用 `NetworkDnsFilter`。

当前运行时将显式的非空遗留值视为启用。请使用 SandMan 中的控件（如果有），或移除该条目以手动关闭，而不要依赖 `DnsTrace=n`。

`DnsTrace` 引入于 Sandboxie Plus 1.14.0 和 Sandboxie Classic 5.69.0。

## 栈追踪

`MonitorStackTrace` 是一个实际上全局生效的监控选项，默认禁用。如果在监控缓冲区创建之前启用，通过通用监控路径的记录会附带栈地址：

```ini
[GlobalSettings]
MonitorStackTrace=y
```

并非每个诊断源都保证包含栈信息，且栈可能不完整或包含无法解析符号的帧。SandMan 异步解析符号，并可能使用或安装 DbgHelp 和符号支持。栈采集和符号解析带来诊断开销，符号下载可能涉及网络访问。

SandMan 通过跟踪日志中的**「显示栈追踪」**暴露此设置。更改它不会重建活动中的监控缓冲区。为可靠地启用或停用：

1. 更改**「显示栈追踪」**。
2. 停止跟踪日志。
3. 重新启动跟踪日志。

通常不需要重启服务或驱动。`MonitorStackTrace` 引入于 Sandboxie Plus 1.9.6 和 Sandboxie Classic 5.64.6。

## 监控缓冲区大小

`TraceBufferPages` 控制共享追踪/监控缓冲区的分配大小。当前配置的默认值为 `256`，该值在监控启动时读取：

```ini
[GlobalSettings]
TraceBufferPages=2560
```

此示例请求更大的缓冲区，不代表有文档依据的字节或 MiB 换算。更大的值可以减少溢出，代价是占用更多内存。如果缓冲区无法接受更多记录，事件可能被丢弃，Sandboxie 也会报告监控缓冲区溢出。

在监控活动期间更改该设置不会调整当前缓冲区。更改后请停止并重新启动跟踪日志或资源访问监视器。

## 相关监控控制

`DisableResourceMonitor=y` 会抑制受影响沙盒或进程的大量常规用户态和资源监控提交。它不保证每个显式启用的驱动追踪都被抑制。

`MonitorAdminOnly` 将共享监控的激活限制为管理员，对监控控制检查而言实际上是全局生效的。参见[仅监控管理员](MonitorAdminOnly.md)。

## SandMan 配置

通过**「视图(V)」→「跟踪日志记录」**打开实时查看器。每沙盒的追踪控件位于**「沙盒选项 → 高级选项 → 追踪」**，目前包括：

* 禁用资源监控；
* 系统调用、文件、管道、注册表键、IPC、GUI、COM 类、网络防火墙和 DNS 追踪；
* 钩子、API、调试输出和错误追踪。

没有专用控件的高级设置包括 `ApiTraceDll`、`ApiSkipTrace`、`CallTraceEx`、`SbieTrace` 和 `TraceBufferPages`。`MonitorStackTrace` 由跟踪日志中的**「显示栈追踪」**控制，而不是由每沙盒的追踪复选框组控制。

## 应用更改

许多追踪设置由每个沙盒进程初始化或缓存。更改后请重启受影响的进程。影响共享监控缓冲区的选项（包括 `MonitorStackTrace` 和 `TraceBufferPages`）需要停止并重新启动监控，以创建新的缓冲区。

即使没有打开查看器，显式启用的追踪选项也可能安装钩子或执行进程侧工作。活动监控的开销取决于启用的诊断项和事件量。

## 版本历史

* `ApiTrace`、`ApiTraceDll` 和 `ApiSkipTrace` 在 v1.13.0 时加入设置元数据。
* `DnsTrace` 引入于 Sandboxie Plus 1.14.0 和 Sandboxie Classic 5.69.0。
* `CallTraceEx` 在 v1.14.3 中加入。
* `HookTrace` 引入于 Sandboxie Plus 1.15.5 和 Sandboxie Classic 5.70.5。

## 相关页面

- [跟踪日志](../PlusContent/TraceLog.md)
- [实战追踪指南](../PlusContent/tracing-in-practice.md)
- [资源访问监视器](ResourceAccessMonitor.md)
- [钩子追踪](HookTrace.md)
- [崩溃与调试器诊断](CrashAndDebuggerDiagnostics.md)
- [Sandboxie Ini](SandboxieIni.md)
