# 放弃管理员权限

_DropAdminRights_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否将从此沙盒中运行的程序中移除管理员权限。

用法：

```
   .
   .
   .
   [DefaultBox]
   DropAdminRights=y
```

此页面中的设置使 Sandboxie 从此沙盒中运行的程序中移除管理员权限。

具体来说，用于启动沙盒程序的安全凭据将不包括管理员和高级用户组的成员身份。

请注意，如果您已经在非管理员用户账户下运行，这几乎没有效果。

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 放弃权限](RestrictionsSettings.md#drop-rights) 