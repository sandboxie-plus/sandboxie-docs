# 日志消息事件

_LogMessageEvents_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置，自 v1.15.2 / 5.70.2 起可用。它指示 Sandboxie 应把所有 Sandboxie 消息记录到 Windows [系统事件日志](SystemEventLog.md)。

## 用法

```ini
[GlobalSettings]

LogMessageEvents=y
```

## 概述

启用后，此设置会把所有 Sandboxie 消息（SBIE 代码）以 `SbieDrv`[^1] 作为来源写入 Windows 系统事件日志。这为查看和监视所有 Sandboxie 活动（包括通常只出现在弹出对话框或 Sandboxie 消息日志中的错误、警告和信息性消息）提供了集中位置。

## 行为

`LogMessageEvents` 设置影响 Sandboxie 在驱动程序层面处理消息日志的方式[^2]。当生成消息时：

1. 消息首先通过正常的 Sandboxie 消息系统处理[^3]。
2. 如果启用了 `LogMessageEvents`，消息还会作为信息性事件发送到 Windows 事件日志[^4]。
3. 事件包含格式化后的消息文本，并标记相应的 SBIE 消息代码[^5]。

## 使用场景

此设置特别适用于：

- **系统管理员**：通过集中式日志管理监视跨多个系统的 Sandboxie 活动。
- **调试**：为故障排除捕获 Sandboxie 操作的完整记录。
- **合规性**：维护沙盒化应用程序行为的审计日志。
- **自动化**：允许监视工具通过标准 Windows 事件日志 API 关注特定 Sandboxie 事件。

## 消息过滤

启用此设置后，并非所有 Sandboxie 消息都会记录到事件日志。以下消息类型被明确排除在事件日志之外[^6]：

- **MSG_2199**：自动恢复通知。
- **MSG_2198**：文件迁移进度通知。
- **MSG_1399**：进程启动通知。

这些排除可防止事件日志被正常 Sandboxie 运行期间频繁出现的常规操作消息淹没。

## 性能考虑

在正常情况下，启用 `LogMessageEvents` 对性能的影响很小。但在沙盒活动频繁的环境中，额外的事件日志写入可能增加系统开销。在性能至关重要的生产环境中应谨慎使用此设置。

## 实现说明

`LogMessageEvents` 功能在内核驱动层和服务层实现[^7]：

- 驱动组件（SbieDrv）在配置加载期间检查此设置[^8]
- 消息通过服务组件处理，由后者格式化并写入事件日志[^9]
- 该设置会被缓存以提高性能，并在配置重新加载时重新读取[^10]

## 故障排除

如果已启用 `LogMessageEvents`，但事件未出现在 Windows 事件日志中：

1. 确认设置已正确配置在 `[GlobalSettings]` 节中。
2. 检查 Sandboxie 服务是否有适当权限写入事件日志。
3. 更改设置后重启 Sandboxie 服务。
4. 确认 Windows 事件日志服务正在运行。

## 历史背景

此功能在 Sandboxie Plus 1.15.2 / 5.70.2 中作为增强的监视能力引入[^11]。使用此设置时可能导致系统崩溃（BSoD）的一个严重错误已在 1.15.4 中修复[^12]。

[^1]: 来源：`/Sandboxie/core/svc/main.cpp` 中的 `LogMessage_Event` 函数。
[^2]: 来源：`/Sandboxie/core/drv/log.c` 中的 `Log_LogMessageEvents` 布尔变量定义。
[^3]: 来源：`/Sandboxie/core/drv/log.c` 中的 `Log_Popup_Msg` 函数调用逻辑。
[^4]: 来源：`/Sandboxie/core/svc/main.cpp` 中的 `ReportEvent` 调用。
[^5]: 来源：`/Sandboxie/core/svc/main.cpp` 中 `SbieDll_FormatMessage2` 调用的消息格式化。
[^6]: 来源：`/Sandboxie/core/svc/DriverAssistLog.cpp` 中的消息过滤逻辑。
[^7]: 来源：`/Sandboxie/core/drv/log.c` 中通过 `Api_SendServiceMessage` 进行的数据通信。
[^8]: 来源：`/Sandboxie/core/drv/conf.c` 中 `Conf_Get_Boolean` 调用的配置加载。
[^9]: 来源：`/Sandboxie/core/svc/DriverAssistLog.cpp` 中的 `LogMessage` 函数。
[^10]: 来源：`/Sandboxie/core/drv/log.h` 中 `Log_LogMessageEvents` 全局变量的缓存。
[^11]: 来源：CHANGELOG.md 中 1.15.2 / 5.70.2 版本的条目
[^12]: 来源：CHANGELOG.md 中 1.15.4 / 5.70.4 版本 BSoD 修复条目
