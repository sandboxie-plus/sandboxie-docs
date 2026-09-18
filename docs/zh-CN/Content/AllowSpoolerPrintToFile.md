# 允许后台打印程序打印到文件

`AllowSpoolerPrintToFile` 是一项沙盒设置，提供对沙盒化应用程序如何与打印后台处理程序服务交互的精细控制。

```
   .
   .
   .
   [DefaultBox]
   AllowSpoolerPrintToFile=n
```

此设置可用于阻止沙盒化应用程序打印到文件。默认情况下，Sandboxie 阻止沙盒化的 `spoolsv.exe` 发出所有请求写访问的 `CreateFile` 调用。
