# 关闭的 CLSID

_ClosedClsid_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置，自 v0.5.3a / 5.45.2 版本起可用。它指定了沙盒程序不应访问的非沙盒 COM 对象的 COM 类标识符。

用法：
```
   .
   .
   .
   [DefaultBox]
   ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

此示例使沙盒程序无法访问 _Windows 管理和检测_。

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 关闭 