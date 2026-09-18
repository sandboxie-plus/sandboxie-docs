# 关闭 Clsid

_ClosedClsid_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.5.3a / 5.45.2 起可用。它指定沙盒化程序不应访问的非沙盒化 COM 对象的 COM 类标识符。

用法：
```
   .
   .
   .
   [DefaultBox]
   ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

此示例使 _Windows Management and Instrumentation_ 对沙盒化程序不可访问。

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 封闭
