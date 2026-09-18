# 标准注册表路径

_NormalKeyPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径应用默认沙盒化方案。此设置与 [规则特异性](../PlusContent/RuleSpecificity.md) 结合时最有用，它允许为父路径已被配置为开放、只写甚至封闭的路径恢复默认沙盒化行为。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
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

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 标准
