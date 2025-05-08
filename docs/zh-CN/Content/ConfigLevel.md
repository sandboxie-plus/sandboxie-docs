# 配置级别

**注意：在 Sandboxie 3.xx 版本之前，ConfigLevel 是 [GlobalSettings] 部分中的全局设置。全局 ConfigLevel 设置不再使用，如果它存在于配置文件中也会被忽略。**

_ConfigLevel_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它被 [Sandboxie 控制器](SandboxieControl.md) 用来管理沙盒的默认配置。

当 ConfigLevel 缺失、不是数字或数字小于 9 时，Sandboxie 控制器将向沙盒添加以下配置：

```
   .
   .
   .
   [DefaultBox]
   ConfigLevel=9
   Template=OpenSmartCard
   Template=OpenBluetooth
```

请注意，ConfigLevel 值在 Sandboxie v0.7.5 / 5.49.8 版本发布时从 8 更改为 9。

在未来，可能会在 Sandboxie 的后续版本中添加新的配置级别。 