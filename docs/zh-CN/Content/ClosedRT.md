# 关闭的 RT 接口

_ClosedRT_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置，自 v0.5.3a / 5.45.2 版本起可用。它指定了沙盒程序不应访问的有问题的 Windows RT 接口。

用法：
```
   .
   .
   .
   [DefaultBox]
   ClosedRT=ExampleRT
```

此示例使沙盒程序无法访问 _ExampleRT_ 接口。

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 关闭 RT 