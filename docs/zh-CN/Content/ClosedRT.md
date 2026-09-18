# 封禁 RT

_ClosedRT_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.5.3a / 5.45.2 起可用。它指定沙盒化程序不应访问的问题 Windows RT 接口。

用法：
```
   .
   .
   .
   [DefaultBox]
   ClosedRT=ExampleRT
```

此示例使 _ExampleRT_ 接口对沙盒化程序不可访问。

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 封禁 RT
