# 仅限管理员监视

_MonitorAdminOnly_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。如果指定，在非管理员组成员用户帐户下运行的 [沙盒管理器](SandboxieControl.md) 将无法调用 [资源访问监视器](ResourceAccessMonitor.md) 功能。

理由：资源访问监视器在调用它的每个用户会话中消耗 64K 字节系统内存，因此网络管理员可能希望阻止其用户调用该功能。

用法：

```
   .
   .
   .
   [GlobalSettings]
   MonitorAdminOnly=y
```

此设置专为网络管理员使用而设计。
