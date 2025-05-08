# 阻止网络参数

_BlockNetParam_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否允许沙盒化程序更改网络和防火墙参数。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockNetParam=n
```

指定 _n_ 表示应该允许沙盒化程序发出更改网络和防火墙参数的请求。 