# 系统事件日志

系统事件日志是 Windows 的一个组件，收集 Windows 本身和其他第三方软件发出的信息性和错误消息。Sandboxie 会向系统事件日志发出一些消息。这些消息以 Source 值 SbieDrv 列出。要访问日志并查看消息，请使用事件查看器工具：

Windows 开始菜单 > 控制面板 > 管理工具 > 事件查看器

关于系统事件日志的更多信息，参见 [维基百科上的事件查看器](https://en.wikipedia.org/wiki/Event_Viewer)。

如果因阻止成功初始化的错误而发出任何 Sandboxie 消息，[沙盒管理器](SandboxieControl.md) 会显示一个闪烁的感叹号图标。右键点击闪烁的图标并选择 _显示错误_ 以查看相关消息。

_来自 Sandboxie 的消息_不存储在_Windows 事件日志_中，有一个变通办法可以 [把日志存储在平面文件中](MessagesFromSandboxie.md#将消息记录到文件)。

另请参阅：[SBIE 消息](SBIEMessages.md)。
