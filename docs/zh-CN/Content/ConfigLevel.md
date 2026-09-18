# 配置等级

**注意：在 3.xx 之前的 Sandboxie 版本中，配置等级是 [GlobalSettings] 节中的全局设置。全局配置等级设置已不再使用，如果它存在于配置文件中会被忽略。**

_ConfigLevel_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。[沙盒管理器](SandboxieControl.md) 用它来管理沙盒的默认配置。

当配置等级缺失、不是数字或数字低于 9 时，沙盒管理器将向沙盒添加以下配置：

```
   .
   .
   .
   [DefaultBox]
   ConfigLevel=9
   Template=OpenSmartCard
   Template=OpenBluetooth
```
注意：配置等级的值在 Sandboxie v0.7.5 / 5.49.8 发布时从 8 改为 9。

将来，Sandboxie 的更高版本中可能会添加新的配置等级。
