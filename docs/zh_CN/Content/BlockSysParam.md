# 阻止 Sys 参数

**BlockSysParam 功能已在 SBIE 4.+ 及更高版本中移除，不再可用**

_BlockSysParam_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱参数。该参数用于指定 Sandboxie 是否允许被沙箱化的程序更改多种系统参数。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BlockSysParam=n
```

指定 _n_ 表示允许被沙箱化的程序发出请求以更改多种系统参数，例如桌面壁纸。

关于可更改的系统参数的详细讨论，请参阅 Microsoft MSDN 网站上的 [SystemParametersInfo API](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa) 讨论。

**技术说明：** 当 Sandboxie 阻止更改系统参数的请求时，该操作会在 [Resource Access Monitor](ResourceAccessMonitor.md) 中以操作 _(SystemParametersInfo:nnnnnnnn)_ 进行记录，这里的 _nnnnnnnn_ 是对应传递给 SystemParametersInfo API 的 _uiAction_ 参数的十六进制值。

相关的 [沙箱控制](SandboxieControl.md) 设置：[沙箱设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed)
