# 启动服务

_StartService_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它允许在沙盒中运行服务程序。此设置需要一个服务名称（标识符），该名称在沙盒外部定义。例如：

```ini
   .
   .
   .
   [DefaultBox]
   StartService=Adguard Service
```

此示例指定服务名称 _Adguard Service_ 将被强制在沙盒 _DefaultBox_ 中以沙盒模式运行。

**技术细节**

_StartService_ 由 [SandboxieRpcSs](ServicePrograms.md#远程过程调用-rpc) 处理，该程序在每个沙盒中仅运行一次。与 [自动执行](AutoExec.md) 设置一样，它在沙盒中第一个程序开始运行时进行处理。

有关应用程序的内容，请参阅 [启动程序](StartProgram.md)。
