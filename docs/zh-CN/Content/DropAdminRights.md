# 撤销管理员权限

_DropAdminRights_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否将剥夺在此沙盒中运行的程序的管理员权限。

用法：

```
   .
   .
   .
   [DefaultBox]
   DropAdminRights=y
```

此页中的设置会让 Sandboxie 剥夺在此沙盒中运行的程序的管理员权限。

具体来说，用于启动沙盒化程序的安全凭据将不包含管理员组和 Power Users 组的成员资格。

注意：如果你已经在非管理员用户帐户下运行，此设置几乎没有什么效果。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 放弃权限](RestrictionsSettings.md#放弃权限)
