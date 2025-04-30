# 阻止网络参数

_BlockNetParam_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它指定 Sandboxie 是否允许在沙箱中的程序更改网络和防火墙参数。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockNetParam=n
```

指定 _n_ 表示应允许沙箱中的程序请求更改网络和防火墙参数
