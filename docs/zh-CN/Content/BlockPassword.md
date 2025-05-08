# 阻止密码

**此功能已过时。如果您使用 Windows 10 或更高版本，我们建议自 0.7.0 / 5.48.0 版本起使用 _OpenSamEndpoint_：[#938](https://github.com/sandboxie-plus/Sandboxie/issues/938)**

_BlockPassword_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否允许沙盒化程序更改用户账户的密码。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockPassword=n
```

指定 _n_ 表示应该允许沙盒化程序发出更改用户账户密码的请求。

~~相关 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed)~~ 