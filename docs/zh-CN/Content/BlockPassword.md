# 阻止密码更改

**该功能已过时。如果你使用的是 Windows 10 或更高版本，建议从 0.7.0 / 5.48.0 版本起使用 _OpenSamEndpoint_：[ #938 ](https://github.com/sandboxie-plus/Sandboxie/issues/938)**

_BlockPassword_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置。它用于指定 Sandboxie 是否允许在沙箱中运行的程序修改用户帐户的密码。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BlockPassword=n
```

将 _n_ 设定为参数，表示允许沙箱中的程序请求更改用户帐户密码

~~相关的 [沙箱控制](SandboxieControl.md) 设置：[ 沙箱设置 > 限制 > 低级访问 ](RestrictionsSettings.md#low-level-access--removed)~~
