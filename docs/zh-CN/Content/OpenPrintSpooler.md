# 开放打印后台处理程序

_OpenPrintSpooler_ 是一项沙盒设置，提供对沙盒化应用程序如何与打印后台处理程序服务交互的精细控制。

```
   .
   .
   .
   [DefaultBox]
   OpenPrintSpooler=n
```

此设置阻止沙盒化应用程序在沙盒外设置打印机。

可以通过设置 `OpenPrintSpooler=y` 禁用此过滤器。

作为 0.5.4 / 5.46.0 版本的一部分添加。

_另请参阅 [封禁打印后台处理服务](ClosePrintSpooler.md)_。
