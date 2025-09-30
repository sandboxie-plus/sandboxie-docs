# 标准注册表路径

_标准注册表路径_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它用于指定那些将被沙盘应用默认沙箱化策略的路径模式。该设置在与 [规则特定性](../PlusContent/RuleSpecificity.md) 配合使用时尤其有用，此时能够为父路径已被配置为开放、仅写甚至封禁的路径恢复到默认沙箱行为。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```ini
   .
   .
   .
   [DefaultBox]
   NormalIpcPath=*BaseNamedObjects*\__ComCatalogCache__
   NormalIpcPath=*BaseNamedObjects*\ComPlusCOMRegTable
   NormalIpcPath=*BaseNamedObjects*\RotHintTable
   NormalIpcPath=*BaseNamedObjects*\{A3BD3259-3E4F-428a-84C8-F0463A9D3EB5}
   NormalIpcPath=*BaseNamedObjects*\{A64C7F33-DA35-459b-96CA-63B51FB0CDB9}
   NormalIpcPath=\RPC Control\actkernel
   NormalIpcPath=\RPC Control\epmapper
   NormalIpcPath=\RPC Control\OLE*
   NormalIpcPath=\RPC Control\LRPC*
```

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 注册表 > 添加注册键 > 访问列 > 标准