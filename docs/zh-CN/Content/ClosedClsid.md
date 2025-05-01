# 关闭 Clsid

_ClosedClsid_ 是 [Sandboxie Ini](SandboxieIni.md) 配置文件中的一个沙箱设置，自 v0.5.3a / 5.45.2 版本起可用。该设置用于指定应禁止沙箱程序访问的非沙箱 COM 类标识符（CLSID）。

用法示例：
```
   .
   .
   .
   [DefaultBox]
   ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

此示例将使沙箱程序无法访问 _Windows Management and Instrumentation_。

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 封禁（关闭）
