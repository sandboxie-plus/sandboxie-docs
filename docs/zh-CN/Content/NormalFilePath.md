# 标准文件路径

_NormalFilePath_ 是 [沙箱配置文件（Sandboxie Ini）](SandboxieIni.md) 中的一个沙箱设置项。它用于指定一系列路径模式，使得对于这些模式所匹配的路径，沙箱软件（Sandboxie）会对其应用默认的沙箱方案。该设置与 [规则特异性](../PlusContent/RuleSpecificity.md) 结合使用时最为有用，可用于为那些父路径已经被配置为开放、仅写或甚至封禁的路径恢复默认的沙箱行为。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：

```ini
   .
   .
   .
   [DefaultBox]
   NormalFilePath=C:\Downloads\
   NormalFilePath=*.eml
   NormalFilePath=iexplore.exe,%Favorites%
   NormalFilePath=msimn.exe,*.eml
```

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 标准