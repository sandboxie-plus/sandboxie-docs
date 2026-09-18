# MSI 安装程序豁免

_MsiInstallerExemptions_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.7.2 / 5.49.0 起可用。

```
   .
   .
   .
   [DefaultBox]
   MsiInstallerExemptions=y
```

使用“MsiInstallerExemptions=y”选项可让 MSIServer 以沙盒化的系统令牌运行并应用其他例外。此选项可能有助于安装 MSI 包。

相关 Sandboxie Plus 设置：沙盒选项 > 安全选项 > 安全加固 > 允许 MSIServer 以沙盒化的系统令牌运行，并在需要时应用其他例外
