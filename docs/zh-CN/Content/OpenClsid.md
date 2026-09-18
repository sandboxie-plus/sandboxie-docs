# 开放 Clsid

_OpenClsid_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定非沙盒化 COM 对象的 COM 类标识符，这些对象应可供沙盒化程序访问。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenClsid={D713F357-7920-4B91-9EB6-49054709EC7A}
```

此示例让 HP 通用打印机状态监视器弹出组件可供沙盒化程序访问。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > COM 访问](ResourceAccessSettings.md#com-访问)

相关 Sandboxie Plus 设置：

沙盒选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 开放

沙盒选项 > 资源访问 > COM > 不使用虚拟化 COM，开放对宿主机 COM 基础设施的访问（不推荐）
