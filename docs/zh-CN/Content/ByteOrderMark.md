# 字节顺序标记

**此功能已自 v0.6.5 / 5.47.0 起移除。**

_ByteOrderMark_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。通常指定为 ByteOrderMark=y（参见 [是/否设置](YesOrNoSettings.md)），表示 [沙盒管理器](SandboxieControl.md) 应在配置文件顶部插入 UTF-16 UNICODE 字节顺序标记（BOM）字符。

用法：

```
   .
   .
   .
   [GlobalSettings]
   ByteOrderMark=y
```

必须把此设置编辑进 [Sandboxie Ini](SandboxieIni.md)，然后手动 [重新加载](ConfigureMenu.md#重新加载配置) Sandboxie 配置。之后，下一次 [沙盒管理器](SandboxieControl.md) 重写配置时，它会把 UNICODE BOM 字符插入 [Sandboxie Ini](SandboxieIni.md) 配置文件的头两个字节，即（十六进制）FF FE。

只有在以下两个条件都成立时才需要操心此设置：

*   你计划手动编辑 [Sandboxie Ini](SandboxieIni.md) 文件；
*   你的文本编辑器无法识别 [Sandboxie Ini](SandboxieIni.md) 文件是 UNICODE 文本文件。
