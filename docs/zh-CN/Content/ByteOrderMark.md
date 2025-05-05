# 字节顺序标记

**此功能自 v0.6.5 / 5.47.0 起已移除。**

_ByteOrderMark_ 是 [沙盘配置文件](SandboxieIni.md) 中的一个全局设置。它通常指定为 ByteOrderMark=y（请参阅 [是或否设置](YesOrNoSettings.md)），表示 [沙盘控制](SandboxieControl.md) 应在配置文件的顶部插入一个 UTF-16 统一码字节顺序标记 (BOM) 字符。

用法：

```
   .
   .
   .
   [GlobalSettings]
   ByteOrderMark=y
```

此设置必须手动编辑到 [沙盘配置文件](SandboxieIni.md) 中，然后必须手动 [重新加载](ConfigureMenu.md#reload-configuration) 沙盘配置。此后，下次 [沙盘控制](SandboxieControl.md) 重写配置时，它将在 [沙盘配置文件](SandboxieIni.md) 的前两个字节中插入统一码 BOM 字符，即：（十六进制）FF FE。

只有在以下两个条件都满足时，你才需要关注此设置：

* 你计划手动编辑 [沙盘配置文件](SandboxieIni.md)；
* 你的文本编辑器无法识别 [沙盘配置文件](SandboxieIni.md) 是一个统一码文本文件。
