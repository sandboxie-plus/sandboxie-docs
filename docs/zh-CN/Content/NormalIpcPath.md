# 标准 IPC 路径

_NormalIpcPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定路径模式，沙盘会针对这些路径应用默认的沙箱方案。该设置在配合 [规则特异性](../PlusContent/RuleSpecificity.md) 使用时尤为有用，可以让被配置为“开放”、“只写”甚至“关闭”的父路径下的某些路径恢复为默认的沙箱行为。

示例：

```ini
   .
   .
   .
   [DefaultBox]
   NormalIpcPath=\RPC Control\AudioSrv
```

相关的 Sandboxie Plus 设置：沙盘选项 > 资源访问 > IPC > 添加 IPC 路径 > 访问列 > 标准