# 阻止系统参数修改

**BlockSysParam 功能已在 SBIE 4.+ 及更高版本中移除。不再可用。**

_BlockSysParam_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否允许沙盒程序更改各种系统参数。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockSysParam=n
```

指定 _n_ 表示允许沙盒程序发出更改各种系统参数的请求，例如桌面壁纸。

关于可以更改的系统参数的详细讨论，请参阅 Microsoft MSDN 网站上的 [SystemParametersInfo API](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa) 说明。

**技术说明：** 当 Sandboxie 阻止更改系统参数的请求时，这将在[资源访问监视器](ResourceAccessMonitor.md)中记录为操作 _(SystemParametersInfo:nnnnnnnn)_，其中 _nnnnnnnn_ 是一个十六进制值，对应于传递给 SystemParametersInfo API 的 _uiAction_ 参数。

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed) 