# 忘记密码

_ForgetPassword_ 是 [Sandboxie Ini](SandboxieIni.md) 中的全局设置。如果在 [沙盘控制](SandboxieControl.md) 或 [Sandman](PlusMigrationGuide.md) 中设置，当主窗口被隐藏时，配置密码会被清除 —— 之后需要重新输入密码才能修改配置设置。

用法如下：

```ini
   .
   .
   .
   [GlobalSettings]
   ForgetPassword=y
```

参见：[配置保护](ConfigurationProtection.md)

相关的 Sandboxie Plus 设置：选项菜单 > 全局设置 > 高级配置 > Sandboxie.ini 预设 > 当主窗口被隐藏时清除密码