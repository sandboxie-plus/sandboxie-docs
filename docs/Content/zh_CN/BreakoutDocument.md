# 分离文档

_BreakoutDocument_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置项，自 v1.8.5 / 5.63.5 版本起可用。它用于指定从沙盒内部打开哪些文档时，应在非沙盒环境下打开这些文档。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BreakoutDocument=C:\path\*.txt
   BreakoutDocument=C:\path\*.jpg
```
