# 仅限管理员监视

_MonitorAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置项。如果启用该设置，则在非管理员组成员的用户帐户下运行的 [沙盘控制](SandboxieControl.md) 将无法调用 [资源访问监视器](ResourceAccessMonitor.md) 功能。

这样设计的主要原因是，资源访问监视器每次被调用时，会为每个用户会话消耗 64K 字节的系统内存，因此网络管理员可能希望防止普通用户调用该功能。

用法示例：

```
   .
   .
   .
   [GlobalSettings]
   MonitorAdminOnly=y
```

此设置项专为网络管理员使用而设计。