# 开放 Clsid

_OpenClsid_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它用于指定沙箱程序可以访问的、非沙箱的 COM 类标识符（CLSID）。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenClsid={D713F357-7920-4B91-9EB6-49054709EC7A}
```

此示例允许沙箱程序访问 HP 通用打印机状态监视器弹出组件。

相关的 [沙盒控制](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > COM 访问](ResourceAccessSettings.md#com-access)

相关的沙盒 Plus 设置：

沙箱选项 > 资源访问 > COM > 添加 COM 对象 > 访问列 > 开放

沙箱选项 > 资源访问 > COM > 不使用虚拟化 COM，向主机 COM 基础架构开放访问（不推荐）