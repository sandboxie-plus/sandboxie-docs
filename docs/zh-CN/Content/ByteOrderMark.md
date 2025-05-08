# 字节顺序标记

**此功能自 v0.6.5 / 5.47.0 版本起已移除。**

_ByteOrderMark_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的全局设置。它通常指定为 ByteOrderMark=y（参见 [是或否设置](YesOrNoSettings.md)），表示 [Sandboxie 控制器](SandboxieControl.md) 应在配置文件顶部插入 UTF-16 UNICODE 字节顺序标记（BOM）字符。

用法：

```
   .
   .
   .
   [GlobalSettings]
   ByteOrderMark=y
```

必须将此设置手动编辑到 [Sandboxie Ini](SandboxieIni.md) 中，然后手动[重新加载](ConfigureMenu.md#reload-configuration) Sandboxie 配置。之后，下次 [Sandboxie 控制器](SandboxieControl.md) 重写配置时，它将在 [Sandboxie Ini](SandboxieIni.md) 配置文件的最前面两个字节插入 UNICODE BOM 字符，即：（十六进制）FF FE。

只有当以下两个条件都成立时，您才需要关注此设置：

* 您计划手动编辑 [Sandboxie Ini](SandboxieIni.md) 文件；
* 您的文本编辑器无法识别 [Sandboxie Ini](SandboxieIni.md) 文件是 UNICODE 文本文件。 