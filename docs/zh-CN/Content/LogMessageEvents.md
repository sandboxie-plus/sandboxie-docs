# 日志消息事件

_LogMessageEvents_ 是自 v1.15.2 / 5.70.2 起在 [沙盘配置](SandboxieIni.md) 中提供的全局设置。该选项表示沙盘应将所有沙盘消息记录到 Windows [系统事件日志](SystemEventLog.md)

## 用法

```ini
[GlobalSettings]

LogMessageEvents=y
```

## 概述

启用该设置后，所有沙盘消息（SBIE 代码）都会以 `SbieDrv` 作为来源被写入 Windows 系统事件日志[^1]。这样可以为查看和监控所有沙盘活动提供一个集中的位置，包括原本只会出现在弹窗或沙盘消息日志中的错误、警告及信息性消息

## 行为说明

`LogMessageEvents` 设置会影响沙盘在驱动层面的消息日志处理方式[^2]。当产生消息时：

1. 消息首先会通过常规的沙盘消息系统进行处理[^3]
2. 如果启用了 `LogMessageEvents`，消息还会作为信息事件被额外发送到 Windows 事件日志中[^4]
3. 该事件包含格式化的消息文本，并标记有相应的 SBIE 消息码[^5]

## 使用场景

此设置特别适用于：

- **系统管理员**：通过集中日志管理，监控多台系统上的沙盘活动
- **调试排障**：完整捕获沙盘操作记录，便于故障排查
- **合规审计**：维护受沙箱隔离的应用程序行为审计日志
- **自动化监控**：允许监控工具通过标准 Windows 事件日志 API 关注特定沙盘事件

## 消息过滤

启用该设置后，并非所有沙盘消息都会被记录到事件日志。以下消息类型被明确排除在事件日志记录之外[^6]：

- **MSG_2199**：自动恢复通知
- **MSG_2198**：文件迁移进度通知
- **MSG_1399**：进程启动通知

这些排除措施防止在正常沙盘操作期间，常规操作性消息频繁发生而造成事件日志拥挤

## 性能考量

在正常情况下，启用 `LogMessageEvents` 对性能影响极小。但在沙箱活动频繁的环境中，额外的事件日志写入可能会带来系统开销。在对性能要求极高的生产环境下，请谨慎使用该设置

## 实现说明

`LogMessageEvents` 功能在内核驱动层和服务层均有实现[^7]：

- 驱动组件（SbieDrv）在加载配置时检查该设置[^8]
- 消息通过服务组件进行处理，格式化后写入事件日志[^9]
- 为提升性能，该设置被缓存，并在配置重新加载时重新读取[^10]

## 故障排查

如已启用 `LogMessageEvents`，但在 Windows 事件日志中没有相关事件，请按如下步骤排查：

1. 确认该设置已正确配置在 `[GlobalSettings]` 部分
2. 检查沙盘服务是否有写入事件日志的权限
3. 在更改设置后，重启沙盘服务
4. 确认 Windows 事件日志服务正在运行

## 历史背景

该功能是作为增强监控能力的一部分，在 Sandboxie Plus 版本 1.15.2 / 5.70.2 中引入的[^11]。曾存在一个关键性缺陷，在使用本设置时可能导致系统崩溃（蓝屏），该问题已在 1.15.4 版本修复[^12]

[^1]: 来源：`LogMessage_Event` 函数位于 `/Sandboxie/core/svc/main.cpp`
[^2]: 来源：`Log_LogMessageEvents` 布尔变量定义在 `/Sandboxie/core/drv/log.c`
[^3]: 来源：`Log_Popup_Msg` 函数调用逻辑位于 `/Sandboxie/core/drv/log.c`
[^4]: 来源：`ReportEvent` 调用位于 `/Sandboxie/core/svc/main.cpp`
[^5]: 来源：消息格式化见 `SbieDll_FormatMessage2` 调用于 `/Sandboxie/core/svc/main.cpp`
[^6]: 来源：消息过滤逻辑位于 `/Sandboxie/core/svc/DriverAssistLog.cpp`
[^7]: 来源：通过 `Api_SendServiceMessage` 进行数据通信，位于 `/Sandboxie/core/drv/log.c`
[^8]: 来源：配置加载见 `Conf_Get_Boolean` 调用位于 `/Sandboxie/core/drv/conf.c`
[^9]: 来源：`LogMessage` 函数位于 `/Sandboxie/core/svc/DriverAssistLog.cpp`
[^10]: 来源：`Log_LogMessageEvents` 全局变量缓存于 `/Sandboxie/core/drv/log.h`
[^11]: 来源：版本 1.15.2 / 5.70.2 的 CHANGELOG.md 条目
[^12]: 来源：版本 1.15.4 / 5.70.4 BSoD 修复的 CHANGELOG.md 条目