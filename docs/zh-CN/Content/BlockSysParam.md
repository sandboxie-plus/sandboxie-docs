# 阻止 Sys 参数

**阻止 Sys 参数功能已在 SBIE 4.0 及更高版本中移除，不再可用。**

_BlockSysParam_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否应允许沙盒化程序更改各种系统参数。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockSysParam=n
```

指定 _n_ 表示应允许沙盒化程序发出更改各种系统参数（如桌面壁纸）的请求。

关于可更改系统参数的详尽讨论，请查阅 Microsoft MSDN 网站上关于 [SystemParametersInfo API](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa) 的讨论。

**技术说明：** 当 Sandboxie 阻止更改系统参数的请求时，这会在 [资源访问监视器](ResourceAccessMonitor.md) 中记录为操作 _(SystemParametersInfo:nnnnnnnn)_，其中 _nnnnnnnn_ 是对应于传递给 SystemParametersInfo API 的 _uiAction_ 参数的十六进制值。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#低级访问-已移除)
