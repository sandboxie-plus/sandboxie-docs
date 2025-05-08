# 允许打印机打印到文件

`AllowSpoolerPrintToFile` 是一个沙盒设置，用于对沙盒化应用程序如何与打印后台处理程序服务交互进行精细控制。

```
   .
   .
   .
   [DefaultBox]
   AllowSpoolerPrintToFile=n
```

此设置可用于阻止沙盒化应用程序打印到文件。默认情况下，Sandboxie 会阻止所有请求写入访问权限的沙盒化 `spoolsv.exe` 的 `CreateFile` 调用。 