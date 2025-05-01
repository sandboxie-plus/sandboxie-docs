# 分离用户文件夹

“分离用户文件夹”（SeparateUserFolders）是 [Sandboxie 配置文件](SandboxieIni.md) 中的一项沙箱设置，自 v0.2.2 / 5.41.2 版本起可用。它指定用户配置文件是否将在沙箱中单独存储。

```
   .
   .
   .
   [DefaultBox]
   SeparateUserFolders=n
```
此示例中的设置将导致用户配置文件不再在沙箱中单独存储。

相关的 Sandboxie Plus 设置：沙箱选项 > 文件选项 > 分离用户文件夹