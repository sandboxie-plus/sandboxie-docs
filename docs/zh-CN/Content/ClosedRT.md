# 封禁 RT

_ClosedRT_ 是 [Sandboxie Ini](SandboxieIni.md) 中自 v0.5.3a / 5.45.2 版本起提供的沙箱设置。它用于指定不应被沙箱程序访问的有问题的 Windows RT 接口。

用法：
```
   .
   .
   .
   [DefaultBox]
   ClosedRT=ExampleRT
```

此示例使 _ExampleRT_ 接口对沙箱程序不可访问。

相关 Sandboxie Plus 设置：沙箱选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 封禁 RT
