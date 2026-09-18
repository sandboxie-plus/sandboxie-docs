# 标准 IPC 路径

_NormalIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径应用默认沙盒化方案。此设置与 [规则特异性](../PlusContent/RuleSpecificity.md) 结合时最有用，它允许为父路径已被配置为开放、只写甚至封闭的路径恢复默认沙盒化行为。

示例：

```
   .
   .
   .
   [DefaultBox]
   NormalIpcPath=\RPC Control\AudioSrv
```

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 标准
