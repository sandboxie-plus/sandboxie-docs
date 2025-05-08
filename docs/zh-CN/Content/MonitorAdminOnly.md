# 仅管理员监视

_MonitorAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个全局设置。如果指定此设置，在非管理员组成员的用户账户下运行的 [Sandboxie 控制](SandboxieControl.md) 将无法调用[资源访问监视器](ResourceAccessMonitor.md)功能。

原因是资源访问监视器在每个调用它的用户会话中消耗 64K 字节的系统内存，因此网络管理员可能希望阻止其用户调用该功能。

用法：

```
   .
   .
   .
   [GlobalSettings]
   MonitorAdminOnly=y
```

此设置专为网络管理员使用而设计。 