# 撤销管理员权限

_DropAdminRights_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置项。它指定沙盒是否会为在该沙箱中运行的程序撤销管理员权限。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   DropAdminRights=y
```

本页面的设置会导致沙盒去除在该沙箱中运行的程序的管理员权限。

具体而言，启动沙箱程序时所使用的安全凭据将不会包含 Administrators 和 Power Users 组的账户权限。

请注意，如果你本身就是以非管理员用户账户运行，该设置影响很小。

相关的 [沙盒控制](SandboxieControl.md) 设置：[沙箱设置 > 限制 > 撤销权限](RestrictionsSettings.md#drop-rights)。