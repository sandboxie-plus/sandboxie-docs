# 允许后台打印程序打印到文件

`AllowSpoolerPrintToFile` 是一个沙箱设置，用于细致地控制沙箱应用程序与打印后台处理程序的交互方式。

```
   .
   .
   .
   [DefaultBox]
   AllowSpoolerPrintToFile=n
```

此设置可用于防止沙箱应用程序进行文件打印。默认情况下，Sandboxie 会阻止沙箱中的 `spoolsv.exe` 发起的所有请求写入权限的 `CreateFile` 调用。
