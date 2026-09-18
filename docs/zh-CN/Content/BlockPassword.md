# 阻止密码更改

**此功能已过时。如果你使用 Windows 10 或更高版本，自 0.7.0 / 5.48.0 起我们推荐使用 _OpenSamEndpoint_：[#938](https://github.com/sandboxie-plus/Sandboxie/issues/938)**

_BlockPassword_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否允许沙盒化程序更改用户帐户的密码。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockPassword=n
```

指定 _n_ 表示应允许沙盒化程序发出更改用户帐户密码的请求。

~~相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#低级访问-已移除)~~
