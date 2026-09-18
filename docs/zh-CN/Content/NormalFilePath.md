# 标准文件路径

_NormalFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径应用默认沙盒化方案。此设置与 [规则特异性](../PlusContent/RuleSpecificity.md) 结合时最有用，它允许为父路径已被配置为开放、只写甚至封闭的路径恢复默认沙盒化行为。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```
   .
   .
   .
   [DefaultBox]
   NormalFilePath=C:\Downloads\
   NormalFilePath=*.eml
   NormalFilePath=iexplore.exe,%Favorites%
   NormalFilePath=msimn.exe,*.eml
```

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 标准
