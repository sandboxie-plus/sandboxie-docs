# 开放打印后台处理程序

_OpenPrintSpooler_ 是一个沙箱设置，用于细致地控制沙箱内的应用程序与打印后台处理程序服务的交互方式。

```
   .
   .
   .
   [DefaultBox]
   OpenPrintSpooler=n
```

该设置会阻止沙箱内的应用程序在沙箱外部配置打印机。

通过将 `OpenPrintSpooler=y`，可以禁用此限制。

此设置自 0.5.4 / 5.46.0 版本起添加。

_另见 [ClosePrintSpooler](ClosePrintSpooler.md)_。