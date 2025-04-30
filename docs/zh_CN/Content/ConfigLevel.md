# 配置等级

**注意：在 Sandboxie 3.xx 版本之前，ConfigLevel 是 [GlobalSettings] 部分的全局设置。全局 ConfigLevel 设置现已不再使用，如果配置文件中存在则会被忽略。**

_ConfigLevel_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙箱设置，由 [沙箱控制](SandboxieControl.md) 用于管理沙箱的默认配置。

当 ConfigLevel 缺失、不是数字或数字低于 9 时，沙箱控制 会向沙箱添加以下配置：

```
   .
   .
   .
   [DefaultBox]
   ConfigLevel=9
   Template=OpenSmartCard
   Template=OpenBluetooth
```

请注意，ConfigLevel 的值在 Sandboxie v0.7.5 / 5.49.8 版本发布时由 8 更改为 9。

将来，Sandboxie 的后续版本可能会增加新的配置等级。
