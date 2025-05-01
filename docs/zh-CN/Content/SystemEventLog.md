# 系统事件日志

系统事件日志是一个 Windows 组件，用于收集 Windows 自身及其他第三方软件发出的信息和错误消息。Sandboxie 会向系统事件日志发送一些消息。这些消息的“来源”值为 SbieDrv。要访问日志并查看消息，请使用事件查看器工具：

Windows 开始菜单 > 控制面板 > 管理工具 > 事件查看器

有关系统事件日志的更多信息，请参阅 [维基百科上的事件查看器](https://en.wikipedia.org/wiki/Event_Viewer)。

如果由于导致初始化失败的错误而发出任何 Sandboxie 消息，[Sandboxie 控制](SandboxieControl.md) 将显示一个闪烁的感叹号图标。右键单击闪烁的图标并选择“显示错误”以查看任何相关消息。

_来自 Sandboxie 的消息_ 不会存储在 _Windows 事件日志_ 中，可以通过 [将日志存储在平面文件中](MessagesFromSandboxie.md#log-messages-to-a-file) 来解决这个问题。

另请参阅：[SBIE 消息](SBIEMessages.md)。