# 开放 CLSID

_OpenClsid_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定沙盒化程序应该可以访问的未沙盒化 COM 对象的 COM 类标识符。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenClsid={D713F357-7920-4B91-9EB6-49054709EC7A}
```

此示例使 HP 通用打印机状态监视器弹出组件可被沙盒化程序访问。

相关的 [Sandboxie 控制](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > COM 访问](ResourceAccessSettings.md#com-access)

相关的 Sandboxie Plus 设置：

沙盒选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 开放

沙盒选项 > 资源访问 > COM > 不使用虚拟化 COM，开放访问主机 COM 基础设施（不推荐） 